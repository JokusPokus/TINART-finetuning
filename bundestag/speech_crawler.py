"""
Crawls parliament speeches held by a certain politician.

To be called like this:
python speech_crawler.py <FULL_NAME_OF_POLITICIAN>

e.g.,
python speech_crawler.py "Angela Merkel"
"""

import requests
import sys

from bs4 import BeautifulSoup
from typing import List


OUTPUT_DIRECTORY = "./input_data/{}/"

LINKS_SOURCE = "./bundestag/resource_links/resource_links.txt"


class XMLParser:
    parser_type = "xml"

    def __init__(self, politician, output_directory=OUTPUT_DIRECTORY, source=LINKS_SOURCE):
        self.politician = politician.capitalize()
        self.first_name = POLITICIAN.split()[0]
        self.last_name = POLITICIAN.split()[1]
        self.output_directory = output_directory.format(self.last_name)
        self.source = source

    def _is_authored_by_target(self, speech):
        """
        Takes a BeautifulSoup tag representing a parliament speech
        and checks whether the speech was authored by the
        targeted politician.

        :param speech: BeautifulSoup tag
        :return: True if authored by targeted politician, else False
        """
        speaker = speech.find("p", klasse="redner").redner.find("name")

        if not speaker.vorname or not speaker.nachname:
            return False

        first_name = str(speaker.vorname.string)
        last_name = str(speaker.nachname.string)

        return first_name == self.first_name and last_name == self.last_name

    @classmethod
    def _get_tops(cls, doc):
        soup = BeautifulSoup(doc, features=cls.parser_type)
        return soup.sitzungsverlauf.find_all("tagesordnungspunkt")

    @staticmethod
    def _get_speeches(top):
        return top.find_all("rede")

    @staticmethod
    def _get_parts(speech):
        return speech.find_all("p", klasse=["J", "O"])

    def _parse_xml(self, doc):
        """
        Takes an xml string and searches for politician speech.

        :param doc: xml string
        :return: The speech as a string if found, else None.
        """
        target_speech = []
        tops = self._get_tops(doc)

        for top in tops:
            speeches = self._get_speeches(top)

            for speech in speeches:
                if self._is_authored_by_target(speech):
                    parts = self._get_parts(speech)

                    for part in parts:
                        if str(part.string) != "None":
                            target_speech.append(str(part.string))

        if not target_speech:
            return None

        return " ".join(target_speech)

    def _get_speech(self, source):
        """
        Takes a source link as a string, performs an HTTP request,
        and returns a coherent parliament speech.
        If the politician didn't speak, None is returned.

        :return: A parliament speech as a string.
        If politician didn't speak, None is returned.
        """
        response = requests.get(source)
        xml = response.content

        speech = self._parse_xml(xml)
        return speech

    def _append_speech(self, speech):
        """
        Takes a speech as a big string and appends it to the ouput text file.

        :param speech: speech as a unicode string
        """
        with open(self.output_directory + "speech_collection.txt", "a+", encoding="utf-8") as sp_coll:
            sp_coll.write(speech + "\n")

    def _get_links(self):
        """
        Returns a list of links, read from the specified text file in self.source.
        """
        with open(self.source, "r", encoding="utf-8") as link_doc:
            return link_doc.readlines()

    def write_speeches_to_file(self):
        links = self._get_links()
        for link in links:
            speech = self._get_speech("https://" + link.strip())
            if speech:
                self._append_speech(speech)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("""To be called like this:
python speech_crawler.py <FULL_NAME_OF_POLITICIAN>

e.g.,
python speech_crawler.py 'Angela Merkel'""")
        sys.exit()

    politician = sys.argv[1]
    parser = XMLParser(politician)
    parser.write_speeches_to_file()
