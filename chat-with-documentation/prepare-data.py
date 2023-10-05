
from langchain.embeddings import GPT4AllEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import PyPDFLoader
import markdown,os,pathlib
from langchain.document_loaders import BSHTMLLoader

DOC_DIR="./docs"
DATA_DIR="./data"
def indexMarkdown(file):
    OUT_FILE="output.html"
  12.0"
        #raw_document[0].metadata = raw_document[0].metadata | m
        #raw_document[0].metadata["source"] = str(raw_document[0].metadata["source"])
        #    docs = docs + raw_document
        documents = text_splitter.split_documents(raw_document)
        vectorstore = Chroma.from_documents(documents=documents, embedding=GPT4AllEmbeddings(), persist_directory=DATA_DIR)
        vectorstore.persist()
        


def indexPDF(pdf):
    # Indexing the Info Center documentation 
    print("Found file : "+os.path.abspath(pdf)+" - Processing as PDF file")
    pdf_loader = PyPDFLoader(pdf)
    document=pdf_loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    all_splits = text_splitter.split_documents(document)
    vectorstore = Chroma.from_documents(documents=all_splits, embedding=GPT4AllEmbeddings(), persist_directory=DATA_DIR)
    vectorstore.persist()

# find readme url (case senitive)
desktop = pathlib.Path(DOC_DIR)
# indexing README files
for item in desktop.rglob("**/*"):
     if item.is_file():
        file_name, file_extension = os.path.splitext(item)
        
        if(file_extension==".md"):
            indexMarkdown(item)
        elif(file_extension==".pdf"):
            indexPDF(os.path.abspath(item))






