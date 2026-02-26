import os
from dotenv import load_dotenv
load_dotenv()

from langchain_community.document_loaders import PyPDFLoader
from crewai.tools import tool


@tool("Read Financial PDF")
def read_data_tool(path: str) -> str:
    """
    Reads a financial PDF file and returns its full text content.
    """
    loader = PyPDFLoader(path)
    docs = loader.load()

    full_report = "\n".join([doc.page_content for doc in docs])
    return full_report