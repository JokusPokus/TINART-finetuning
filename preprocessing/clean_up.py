"""
Cleans up Anne Will subtitles so that they can be manually tagged
in a comfortable way.

To be called like this:
python clean_up.py <INPUT_DIRECTORY>
"""

import os
import re
import sys


def delete_timestamps(filename):
    """
    Deletes timestamps to make tagging more convenient
    """
    pattern = re.compile("\d\d:\d\d:\d\d")
    with open(filename, 'r') as f:
        lines = f.readlines()
    with open(filename, 'w') as f:
        for line in lines:
            if not re.match(pattern, line):
                f.write(line)


def main(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        delete_timestamps(file_path)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("""
To be called like this:
python clean_up.py <INPUT_DIRECTORY>""")
        sys.exit()

    directory = sys.argv[1]

    main(directory)