import os
import argparse
import re
from datetime import datetime
import streamlit as st
from langchain.schema import Document
# from tqdm import tqdm
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
# from langchain.vectorstores import ElasticVectorSearch, Pinecone, Weaviate
parser = argparse.ArgumentParser()

def load_api_key(filepath='/Users/simranmasand/Downloads/openapi_key.txt'):
    '''
    This module looks for a locally saved api text file or asks user to input their key as a string literal
    :return: api_key <str>
    '''
    api_key = None
    try:
        with open(filepath, 'r') as file:
            api_key = file.read()
    except:
        api_key = None
        print("No .txt file found. Please provide string literal input.")

    if not api_key:
        api_key=input("Please provide your OpenAI API key or else provide saved .txt file")
    return api_key




#api_key = os.environ.get('OPENAI_API_KEY')
#
# print(key_q)
# print(api_key)

def list_pdf_files(directory):
    '''
    Takes a directory and returns the list of pdfs in it
    :param directory: directory path for files you want to search
    :return: returns a list of all files names that are pdfs
    '''
    pdf_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".pdf"):
                pdf_files.append(os.path.join(root, file))

    return pdf_files



def process_documents(pdf_files_list):
    '''
    This function uses the CharacterTextSplitter to make documents into smaller chunks admissible into LLMs

    :param pdf_files_list: this is the list of files from the directory
    :return: returns a doc list of processed documents
    '''
    docs = []
    for i, file in enumerate(pdf_files_list):
        reader = PdfReader(file)

        raw_text = ''
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                raw_text += text
        text_splitter = CharacterTextSplitter(separator='\n', chunk_size=1000, chunk_overlap=200, length_function=len)
        texts = text_splitter.split_text(raw_text)
        docs.append(Document(page_content="".join(texts), metadata=metadata_generator(file)))

    return docs


def metadata_generator(pdf_file):
    '''
    This generates metadata for documents stored in a Vectordb
    :param pdf_file pdf_file name
    :return: returns a dictionary of the metadata
    '''
    temp = {"date_created": datetime.fromtimestamp(os.stat(pdf_file).st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
            "file_name": re.search(r"/([^/]+)\.pdf$", pdf_file).group(1),
           "date_modified":datetime.fromtimestamp(os.stat(pdf_file).st_mtime).strftime('%Y-%m-%d %H:%M:%S')}
    return temp

def process_file_st(file_st):
    '''
        This function uses the CharacterTextSplitter to make documents into smaller chunks admissible into LLMs for streamlit documents

        :param pdf_files_list: this is file input into streamlit
        :return: returns a doc list of processed documents
        '''
    docs = []
    reader = PdfReader(file_st)

    raw_text = ''
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            raw_text += text
    text_splitter = CharacterTextSplitter(separator='\n', chunk_size=1000, chunk_overlap=200, length_function=len)
    texts = text_splitter.split_text(raw_text)
    docs.append(Document(page_content="".join(texts)))#, metadata=metadata_generator(file_st)))

    return docs

def set_openai_api_key(api_key: str):
    st.session_state["OPENAI_API_KEY"] = api_key

def api_sidebar():
    '''
    This module looks for a locally saved api text file or asks user to input their key as a string literal
    :return: api_key <str>
    '''

    with st.sidebar:
        st.markdown(
            "## How to use\n"
            "1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) below🔑\n"  # noqa: E501
            "2. Upload a pdf, docx, or txt file📄\n"
            "3. Ask a question about the document💬\n"
        )
        api_key_input = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="Paste your OpenAI API key here (sk-...)",
            help="You can get your API key from https://platform.openai.com/account/api-keys.",  # noqa: E501
            value=st.session_state.get("OPENAI_API_KEY", ""),
        )

        if api_key_input:
            set_openai_api_key(api_key_input)
            # st.session_state["OPENAI_API_KEY"] = api_key_input
    #
    # api_key = None
    # try:
    #     with open(filepath, 'r') as file:
    #         api_key = file.read()
    # except:
    #     api_key = None
    #     print("No .txt file found. Please provide string literal input.")
    #
    # if not api_key:
    #     api_key=input("Please provide your OpenAI API key or else provide saved .txt file")
    # return api_key


def clear_submit():
    st.session_state["submit"] = False