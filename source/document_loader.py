#loads/parses HR documents
#assigns metadata, chunks
# for table structures like employee database, turn each row into a sentence for easier semantic search (in diff function)
# for access checking in access policy document, handle through table search for that page
from pathlib import Path
from typing import List
import fitz
from langchain_core.documents import Document
import pdfplumber
import re



class PDFLoader:
    # loads standard pdf text using fitz, splits into documents based on page number
    def __init__(self, filepath: str, doc_type: str = "generic", access_role: str = "employee", 
             department: str = "general", location: str = "universal") -> List[Document]:
        self.filepath = Path(filepath)
        self.doc_type = doc_type
        self.access_role = access_role
        self.department = department
        self.location = location

        if not self.filepath.exists():
            raise FileNotFoundError("File does not exist")
    
    def create_documents(self) -> List[Document]:
        doc = fitz.open(self.filepath)
        documents = []
        for page_num, page in enumerate(doc):
            text = page.get_text()
            text = " ".join(text.split())
            metadata = {
                "page_number": page_num + 1,
                "doc_type": self.doc_type,
                "access_role": self.access_role,
                "department": self.department,
                "location": self.location
            }
            content = text
            documents.append(Document(page_content = content, metadata = metadata))
        return documents

class TableLoader:
    #loads table pdf text like employee, compensation tables
    def __init__(self, filepath: str, doc_type: str = "generic", access_role: str = "employee", sorting_categories: list = None):
        self.filepath = Path(filepath)
        self.doc_type = doc_type
        self.access_role = access_role
        self.sorting_categories = sorting_categories
        if not self.filepath.exists():
            raise FileNotFoundError("File does not exist")
    
    def create_documents(self) -> List[dict]:
        doc = fitz.open(self.filepath)
        documents = []
        first_page = doc[0].get_text()
        first_line_stripped = first_page.splitlines()[0].strip()
        categories = [c.strip() for c in first_line_stripped.split(",")]
        self.sorting_categories = categories
        for page in doc:
            text = page.get_text()
            split_by_id = re.split(r'(?=EMP)', text)
            employees = split_by_id[1:]
            for employee in employees:
                emp = " ".join(employee.split())
                employee_info = [data.strip() for data in emp.split(",")]
                if len(employee_info) != len(self.sorting_categories):
                    print(f"Length mismatch: expected {len(categories)} categories but received {len(employee_info)} categories.")
                employee_dict = dict(zip(self.sorting_categories, employee_info))
                documents.append(employee_dict)
        return documents







