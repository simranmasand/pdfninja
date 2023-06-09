from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
import argparse
import pprint
import random
from tqdm import tqdm
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
import os
from utils import *
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import ElasticVectorSearch, Pinecone, Weaviate
'----------- load the api key'
parser = argparse.ArgumentParser()

parser.add_argument("--apikey_filepath",default='openapi_key.txt',type=str,help="This is where the api_key is stored as .txt file.")
parser.add_argument("--documents_path",default="./sample_pdfs",type=str,help="This is where the pdf documents are stored.")
args = parser.parse_args()
os.environ["OPENAI_API_KEY"]=load_api_key(filepath=args.apikey_filepath) #load the api key into session


# print(os.environ["OPENAI_API_KEY"])

embeddings = OpenAIEmbeddings()
llm = OpenAI(model_name="text-davinci-003") #This is the generative model we are using. We can switch this out with an argparser agument


'''
The directory we want to search through
'''
directory_path = args.documents_path
if not directory_path:
    directory_path = "../simpossum/"

# Call the function to get the list of PDF files in the directory
pdf_files_list = list_pdf_files(directory_path)
print('-----------------------------------')
print('These are the files in this folder:')
print('-----------------------------------')

# Print the list of PDF files
for pdf_file in pdf_files_list:
    print(pdf_file)

print('-----------------------------------')

'''
This codeblock processes the documents and adds them to a vectordb
'''

docsall = process_documents(pdf_files_list) #process documents into a Document schema
vector_store=FAISS.from_documents(docsall,embeddings) #using openai schema, we process documents into vector database
retriever = vector_store.as_retriever(search_kwargs={"k": 1}) #get top k docs # this can be an argaparser requirement
query = input("What file are you looking for? For example: you can ask get me the invoice for flower bulbs. Or get me Simran's resume. Just press enter for a random prompt \n >> ")
if not query:
    query = random.choice(["get me the invoice for garden gnomes","get me Simran's CV"])
    print("\nWe chose the prompt: ", query)

'''
Get the relevant document from search query
'''
docs = retriever.get_relevant_documents(query)

pp = pprint.PrettyPrinter()
print('-----------------------------------')
pp.pprint("Here is a peek at the document (first 1000 characters).")
print('-----------------------------------')

pp.pprint("".join(docs[0].page_content[:1000].replace("\n"," ")))

"""
Query loop that checks for prompts.
"""
chain = load_qa_chain(OpenAI(),chain_type='stuff')
query = None
end = "END"
while query != end:
    query = input("Ask your questions here. If you are done, just type END. \n > ")
    if query == "END":
        break
    if not query:
        query="Why is Simran amazing?"
    docs_focus = vector_store.similarity_search(query) #we can use the entire docs base but I am focussing the QA on the document in question
    print(chain.run(input_documents = docs,question=query))






