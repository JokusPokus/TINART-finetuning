"""
Crawls links to parliament proceeding protocols for the current voting period.
"""

import requests
from bs4 import BeautifulSoup
from typing import Dict, List


# metadata for the HTTP requests
HEADERS = {
    'authority': 'www.bundestag.de',
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.bundestag.de/services/opendata',
    'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7,nl;q=0.6,es;q=0.5',
    'cookie': 'INGRESSCOOKIE=1602572682.198.40.821660; CM_SESSIONID=4A5EDDBABCC058A39020EBCA61518DB9.cae-live-1',
    'dnt': '1',
    'sec-gpc': '1',
}

# Link to the web page where XML protocols can be accessed.
# Note that this link might change in the future.
SOURCE = 'https://www.bundestag.de/ajax/filterlist/de/services/opendata/543410-543410'

OUTPUT_DIRECTORY = ".\\bundestag\\resource_links\\"


class Params:
    """
    Defines the parameters passed to the HTTP request
    """

    limit = ("limit", "10")
    noFilterSet = ("noFilterSet", "true")

    def __init__(self, offset):
        self.offset = ("offset", str(offset))

    def to_tuple(self):
        return (
            self.limit,
            self.noFilterSet,
            self.offset
        )


class HTMLParser:
    """
    Crawls the links to the XML files containing the parliament protocols
    of the current legislative period.

    Stores the links in a txt file in the output directory.
    """

    def __init__(self,
                 headers: Dict = HEADERS,
                 source: str = SOURCE,
                 output_directory: str = OUTPUT_DIRECTORY):
        """
        :param headers: metadata passed to the HTTP request
        :param source: link to the web page where the XML protocols can be accessed
        :param output_directory: directory where the list of links shall be stored
        """
        self.headers = headers
        self.source = source
        self.output_directory = output_directory

    @staticmethod
    def _get_links(doc_string: str) -> List[str]:
        """
        Takes an html string and returns a list with links to XML resources.

        :param doc_string: the HTML content of an HTTP response in string format
        :return: a list of strings, each representing a link to an XML resource
        """
        soup = BeautifulSoup(doc_string, features="html.parser")
        links = []

        for a in soup.find_all("a"):
            new_link = "bundestag.de" + a.get("href")
            links.append(new_link)

        return links

    @staticmethod
    def _has_link(doc_string: str) -> bool:
        """
        Checks whether given html string contains an "a" element.
        """
        soup = BeautifulSoup(doc_string, features="html.parser")
        has_link = bool(soup.a and soup.a["href"])

        return has_link

    def _append_links(self, links: List[str]):
        """
        Takes a list of links in string format and appends them to a text file,
        each link in a new line.

        The text file is saved into the parser's output directory.

        :param links: list of links in string format
        """
        with open(self.output_directory + "resource_links.txt", "a+") as links_file:
            for link in links:
                links_file.write(link + "\n")

    def write_links_to_file(self):
        """
        Crawls the whole source website for links to xml resources
        and writes the links to a text file stored in the output directory.
        """
        offset = 0
        while True:
            params = Params(offset).to_tuple()
            response = requests.get(self.source, headers=self.headers, params=params)

            if not self._has_link(response.content):
                break

            links = self._get_links(response.content)
            self._append_links(links)

            offset += 10


if __name__ == "__main__":
    parser = HTMLParser()
    parser.write_links_to_file()
