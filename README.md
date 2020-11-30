# TINART-finetuning
The data collection and preprocessing, as well as model fine-tuning pipeline to the CODE project ThisIsNotARealTalkshow

## Getting started

### Prerequisites

There should be a recent [Python](https://www.python.org/downloads/) version (3.x) installed on your computer. 

### Setting up an environment

First, navigate to the local directory you would like to place the project code in. 
Then, clone the TINART repository.

```s
cd <PATH_TO_DIRECTORY>
git clone https://github.com/JokusPokus/TINART-finetuning.git
```

Create a virtual environment. The first command is only required if the virtualenv package is not yet installed on your machine.

```s
pip install virtualenv
virtualenv venv
```

Activate the virtual environment.

For Linux users:

```s
source venv/bin/activate
```

For Windows users:

```s
.\venv\Scripts\activate
```

Alternatively, you can use your preferred Python IDE and select the venv there. This project was created using [PyCharm](https://www.jetbrains.com/pycharm/).

Next, install all required packages.

```s
pip install -r requirements.txt
```

Note that iOS users need to replace the `pip` and `python` commands
with `pip3` and `python3`, respectively.

## Bundestag
This directory contains some crawler classes to obtain all parliament speeches of a certain German politician from the current legislative period.

### Get speech links
The `link_crawler.py` file uses HTTP requests to collect all relevant hyperlinks to parliament proceeding protocols and writes them into a text file. 
This text file is then stored in the `resource_links` directory.

To execute the link crawler:

```s
python bundestag/link_crawler.py
```

Note that this code should only run once and doesn't have to be called for each politician separately.

### Scrape speeches
The `speech_crawler.py` file reads in the collected hyperlinks, scrapes the relevant speeches of a given politician, and writes them
to a txt file `speech_collection.txt` in the directory `bundestag/input_data/<POLITICIAN>/`, where `<POLITICIAN>` is the politician's last name (e.g., "merkel").

To execute the speech crawler:
```s
python bundestag/speech_crawler.py <FULL_NAME>
```

For example:
```s
python bundestag/link_crawler.py "Angela Merkel"
```

## Preprocessing
In this directory, you can find functionality to preprocess the raw text data so that it can be used for model fine-tuning.

### Usage
First, the pre-tagged talk show data needs to be provided as a text file in the `raw_data` directory. The parliament speeches are
automatically accessed from the `bundestag` folder.

Now run the following command:

```s
python create_training_file.py <FULL_NAME>
```

For example:

```s
python create_training_file.py "Angela Merkel"
```

This will automatically preprocess all the training data and write them to training and validation text files. The files are saved in the `finetuning/input_data` directory for further usage.

## Finetuning
Here, the transformers library is used to fine-tune pre-trained GPT-2 models.

After completing all previous steps, the training and validation should already be present in the `finetuning/input_data` directory.

Hence, it will suffice to just run the following command:

```s
python create_training_file.py <POLITICIAN>
```

For example:

```s
python create_training_file.py "merkel"
```