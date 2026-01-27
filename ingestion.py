from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader,OnlinePDFLoader,PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
import shutil

load_dotenv()

pdf_paths=[
    "data/GokcenTarım.pdf",
]

web_urls = [



]

pdf_urls = [

    "https://www.highmowingseeds.com/pub/media/wysiwyg/pdf/2018_Planting_Chart.pdf",
    "https://seedcogroup.com/wp-content/uploads/2022/11/Agronomy-Manual.pdf"
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db_store")

all_documents = []

def ingest_docs():






    # ingest local pdf
    for path in pdf_paths:
        if os.path.exists(path):
            loader = PyPDFLoader(path)
            docs= loader.load()
            all_documents.extend(docs)
            print("Locals uploaded...")

    #online pdfs

    for url in pdf_urls:
        try:
            loader= PyMuPDFLoader(url)
            docs= loader.load()
            all_documents.extend(docs)
            print(f"{url} uploaded...")
        except:
            print(f"{url} not found...")

    #web
    for url in web_urls:
        try:
            loader= WebBaseLoader(url)
            docs= loader.load()
            all_documents.extend(docs)
            print(f"{url} uploaded...")
        except:
            print(f"{url} not found...")



    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=25,
        separators=["\n\n", "\n", " ", ""])
    chunks = text_splitter.split_documents(all_documents)

    embedding =GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")

    Chroma.from_documents(
        documents=chunks,
        embedding=embedding,
        collection_name="rag-chroma",
        persist_directory=CHROMA_PATH,

    )
    print("Done!")

retriever = Chroma(
    collection_name="rag-chroma",
    persist_directory=CHROMA_PATH,
    embedding_function=GoogleGenerativeAIEmbeddings(model="gemini-embedding-001"), # Veya GoogleGenerativeAIEmbeddings()
).as_retriever()


if __name__ == "__main__":
    ingest_docs()
    print(all_documents)