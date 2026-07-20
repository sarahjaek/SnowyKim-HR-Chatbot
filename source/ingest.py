#ingests all the documents into vector store using document_loader
import os
from pathlib import Path
from typing import List
from langchain_core.documents import Document

from document_loader import PDFLoader
from document_loader import TableLoader

from vector_store import VectorStore
from vector_store import RecordStore

'''TODO:
1. Store file names from Documents - Done
2. Define access dictionary - Done
3. Function to load policy documents, returns one list for all
4. Function to load tables, returns one list for all
5. Main, create vector and record store from lists of policy and tables
'''
BASE_DIR = Path(__file__).resolve().parent   # folder containing ingest.py
DATA_DIR = BASE_DIR.parent / "Documents"      # go up one level, then into Documents/

cal_access = {
    "compensation-records": 
        {"employee": "own_only",
         "manager": "own_only",
         "hr_staff": "own_only",
         "hr_admin": "all",
         "it_admin": "own_only", 
         "executive": "own_only"},
    "employee-benefits":
        {"employee": "all",
         "manager": "all",
         "hr_staff": "all",
         "hr_admin": "all",
         "it_admin": "all",
         "executive": "all"},
    "employee-data": 
        {"employee": "all",
         "manager": "all",
         "hr_staff": "all",
         "hr_admin": "all",
         "it_admin": "all",
         "executive": "all"},
    "california-hr-policies":
        {"employee": "all",
         "manager": "all",
         "hr_staff": "all",
         "hr_admin": "all",
         "it_admin": "all",
         "executive": "all"},
    "newyork-hr-policies":
        {"employee": "all",
         "manager": "all",
         "hr_staff": "all",
         "hr_admin": "all",
         "it_admin": "all",
         "executive": "all"},
    "onboarding-policy":
        {"employee": "none",
         "manager": "none",
         "hr_staff": "all",
         "hr_admin": "all",
         "it_admin": "none",
         "executive": "all"},
    "past-cases":
        {"employee": "none",
         "manager": "none",
         "hr_staff": "all",
         "hr_admin": "all",
         "it_admin": "none",
         "executive": "none"},
    "recruitment-policy":
        {"employee": "none",
         "manager": "none",
         "hr_staff": "all",
         "hr_admin": "all",
         "it_admin": "none",
         "executive": "all"},
    "workplace-investigation":
        {"employee": "none",
         "manager": "none",
         "hr_staff": "none",
         "hr_admin": "all",
         "it_admin": "none",
         "executive": "none"}
}

ny_access = cal_access # new york access is the same as california access, except for the fields below.
ny_access["onboarding-policy"]["executive"] = "none"
ny_access["recruitment-policy"]["executive"] = "none"
ny_access["workplace-investigation"]["executive"] = "all"

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

def load_table_documents() -> List[dict]: # load only the table information
    docs = []
    docs += TableLoader(filepath = DATA_DIR/"employee-data.pdf",
                        doc_type = "employee-data").create_documents()
    docs += TableLoader(filepath = DATA_DIR/"compensation-records.pdf",
                        doc_type = "compensation-records").create_documents()
    return docs

    
    


