#ingests all the documents into vector store using document_loader
import os
from pathlib import Path
from typing import List
from langchain_core.documents import Document
from dotenv import load_dotenv
result = load_dotenv()

from document_loader import PDFLoader
from document_loader import TableLoader

from vector_store import VectorStore
from vector_store import RecordStore

BASE_DIR = Path(__file__).resolve().parent   # folder containing ingest.py
DATA_DIR = BASE_DIR.parent / "Documents"      # go up one level, then into Documents/



def load_policy_documents() -> List[Document]: # load only the policy documents 
    docs = []
    docs += PDFLoader(filepath = DATA_DIR/"california-hr-policies.pdf", 
                       doc_type = "california-hr-policies").create_documents()
    docs += PDFLoader(filepath = DATA_DIR/"employee-benefits.pdf", 
                       doc_type = "employee-benefits").create_documents()
    docs += PDFLoader(filepath = DATA_DIR/"newyork-hr-policies.pdf", 
                       doc_type = "newyork-hr-policies").create_documents()
    docs += PDFLoader(filepath = DATA_DIR/"onboarding-policy.pdf", 
                       doc_type = "onboarding-policy").create_documents()
    docs += PDFLoader(filepath = DATA_DIR/"past-cases.pdf", 
                       doc_type = "past-cases").create_documents()
    docs += PDFLoader(filepath = DATA_DIR/"recruitment-hiring-policy.pdf", 
                       doc_type = "recruitment-policy").create_documents()
    docs += PDFLoader(filepath = DATA_DIR/"workplace-investigation-guide.pdf", 
                       doc_type = "workplace-investigation").create_documents()
    return docs

def load_employee_data() -> List[dict]: # load only the employee data into list of dictionaries
    employee_documents = TableLoader(filepath = DATA_DIR/"employee-data.pdf",
                        doc_type = "employee-data").create_documents()
    return employee_documents 

def load_compensation_data() -> List[dict]: #load only the compensation data into list of dictionaries:
        compensation_documents = TableLoader(filepath = DATA_DIR/"compensation-records.pdf",
                        doc_type = "compensation-records").create_documents()
        return compensation_documents

def main():
     policy_store = VectorStore()
     policy_docs = load_policy_documents()
     policy_store.add_documents(documents = policy_docs)

     employee_store = RecordStore(file_path = "./employee-database.json")
     employee_data = load_employee_data()
     employee_store.add_records(employee_data)

     compensation_store = RecordStore(file_path ="./compensation-database.json")
     compensation_data = load_compensation_data()
     compensation_store.add_records(compensation_data)
     print("Completed ingestion.")

if __name__ == "__main__": # signifies to only run main if file is being directly executed, not imported
    main()