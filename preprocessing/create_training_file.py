"""
Iteratively reads all the tagged input_data sets corresponding to one particular politician.
Creates one clean and correctly tagged training and validation text file
as an input to the model fine tuning.

To be called like this:
python create_training_file.py <FULL_NAME_OF_POLITICIAN>
"""

import os
import sys
import random
import nltk.data

nltk.download('punkt')


def get_clean_content(filename: str,
                      input_dir: str,
                      politician: str) -> str:
    """
    Goes through a text file and extracts the relevant information.
    Formats the politician's responses.

    :param filename: name of the tagged subtitle file
    :param input_dir: directory of input file
    :param politician: name of politician (e.g., "Christian Lindner")
    :return: string that cleanly represents the relevant content
    """
    with open(input_dir + "\\" + filename, encoding="utf-8") as raw:
        lines = raw.readlines()
        clean_content = []
        current_utterance = ""
        recording = False

        for line in lines:
            if line.strip() == f"[{politician}]":
                recording = True
                current_utterance += "<BOS> "

            elif recording:
                if not line.strip():
                    current_utterance += "<EOS>\n"
                    clean_content.append(current_utterance)
                    current_utterance = ""
                    recording = False

                else:
                    current_utterance += line.strip() + " "

        return "".join(clean_content)


def append_talk_show_snippets(input_dir, temp_storage_dir, politician):
    """
    Appends snippets from talk show to the temporary storage file.
    """
    with open(temp_storage_dir, "w+", encoding="utf-8") as output:
        for filename in os.listdir(input_dir):
            content = get_clean_content(filename, input_dir, politician)
            output.write(content)


def append_speech_snippets(alias, temp_storage_dir, max_chars_per_utterance):
    """
    Breaks up the parliament speeches contained in the raw_data directory
    into smaller chunks, formats them, and writes them to the temporary storage
    file.
    """
    def read_speeches():
        with open(filename, "r", encoding="utf-8") as speeches:
            return speeches.readlines()

    def process_sentences():
        while sentences:
            part = "<BOS> "

            while len(part) < max_chars_per_utterance:
                try:
                    part += sentences.pop(0) + " "
                except IndexError:
                    break

            td.write(part + "<EOS>\n")

    filename = os.path.join(".", "raw_data", alias, "speech_collection.txt")

    content = read_speeches()

    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    with open(temp_storage_dir, "w+", encoding="utf-8") as td:

        for speech in content:
            sentences = tokenizer.tokenize(speech)
            process_sentences()


def write_to_training_files(temp_storage_dir: str,
                            output_dir_train: str,
                            output_dir_valid: str,
                            train_split: float = 0.8):
    """
    Takes the direction to a txt file with all pre-processed sentence snippets
    and splits them into test and validation data.

    Both are written to a txt file in the output directory.
    """
    with open(temp_storage_dir, "r", encoding="utf-8") as f:
        samples = f.readlines()

    random.shuffle(samples)
    cutoff = int(len(samples) * train_split)

    with open(output_dir_train, "w", encoding="utf-8") as td:
        td.write("\n".join(samples[:cutoff]))

    with open(output_dir_valid, "w", encoding="utf-8") as vd:
        vd.write("\n".join(samples[cutoff:]))


def create_temporary_storage(temp_storage_dir: str,
                             politician: str,
                             input_dir: str,
                             max_chars_per_utterance: int = 250):
    """
    Creates a txt file with all preprocessed training snippets,
    including data from both the parliament speeches and talk shows.

    :param temp_storage_dir: Direction of the temporary storage txt file
    :param politician: Full name of the politician of interest
    :param input_dir: Direction where raw input data is stored
    :param max_chars_per_utterance: Number of maximum characters per training sample
    """
    append_talk_show_snippets(input_dir, temp_storage_dir, politician)

    append_speech_snippets(alias, temp_storage_dir, max_chars_per_utterance)


def main(output_dir: str, politician: str, alias: str, input_dir: str):

    temp_storage_dir = os.path.join(output_dir, alias + ".txt")

    output_dir_train = os.path.join("..", "finetuning", "input_data", alias, "training_data.txt")

    output_dir_valid = os.path.join("..", "finetuning", "input_data", alias, "validation_data.txt")

    create_temporary_storage(temp_storage_dir, politician, input_dir)
    write_to_training_files(temp_storage_dir, output_dir_train, output_dir_valid)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("To be called like this:")
        print("python create_training_file <FULL_NAME_OF_POLITICIAN>")
        sys.exit()

    politician = sys.argv[1]
    alias = politician.split()[1].lower()

    INPUT_DIR = os.path.join(".", "raw_data", alias)

    OUTPUT_DIR = os.path.join(".", "training_files")

    main(output_dir=OUTPUT_DIR, politician=politician, alias=alias, input_dir=INPUT_DIR)
