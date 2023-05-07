# PDFNinja

PdfNinja is a Python App that leverages the power of Large Language Models to deal with your documents. Have a large pile of PDFs? Us this tool to simplify your workflow. PDFNinja leverages the chain capabilities of Langchain to create a powerful tool for you to simplify search of pdfs and querying them. 

## Installation

PDFNinja has certain dependencies and was compiled in Python3.9 but shoudl have backward and forward compatibility. The other dependencies are listed in requirements.csv
```bash
$ pip install -r requirements.txt
```

## Usage
You can call pdfninja right from terminal or command line interface. 

### Pre-processing
Obtain an API key from OpenAI. This is parsed to the program using the --apikey_filepath argument.
Have the folder where you want to search for pdf documents as a directory path as well. This will be parsed to the program using --documents_path argument.

### Run from terminal

```bash
python main.py
# returns the workflow with default args
python main.py --apikey_filepath ./userx/Downloads/apikey.txt
# returns the workflow with api_key path but default documents folder

python main.py --apikey_filepath ./userx/Downloads/apikey.txt   
 --documents_path ./userx/PDFFolder/
# returns the workflow with api_key path but default documents folder

```

### See an interactive of this below
[![asciicast](https://asciinema.org/a/8RLOcIgrJ61pXeqnD4EZY6Zrx.svg)](https://asciinema.org/a/8RLOcIgrJ61pXeqnD4EZY6Zrx)

