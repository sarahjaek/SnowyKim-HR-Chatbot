from document_loader import PDFLoader
from vector_store import VectorStore
from vector_store import RecordStore
from document_loader import TableLoader

from pathlib import Path

from dotenv import load_dotenv
result = load_dotenv()

BASE_DIR = Path(__file__).resolve().parent   # folder containing ingest.py
DATA_DIR = BASE_DIR.parent / "Documents"      # go up one level, then into Documents/

'''
Log: added employee-handbook, executive-strategy, reloaded updated employee-data
    handbook = PDFLoader(
        filepath=DATA_DIR/"employee-handbook.pdf",
        doc_type="employee-handbook",
    ).create_documents()
    vs = VectorStore()
    vs.add_documents(handbook)  

    print("Added new documents.")

    employee = TableLoader(filepath = DATA_DIR/"employee-data2.pdf",
                doc_type = "employee-data").create_documents()
    employee_store = RecordStore(file_path = "./employee-database.json")
    employee_store.add_records(employee)

'''
def main():

    compensation = TableLoader(filepath = DATA_DIR/"compensation-records4.pdf",
                doc_type = "compensation-records").create_documents()
    compensation_store = RecordStore(file_path = "./compensation-database.json")
    compensation_store.add_records(compensation)


if __name__ == "__main__":
    main()