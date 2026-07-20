#passes real documents in, embeds, then stores in vector store
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

from typing import List
from langchain_core.documents import Document
import json
import os
import shutil


class VectorStore:
    '''
    Storage database for embeddings for only HR policy documents, not records
    Includes methods to add documents to vector store and get retriever to retrieve most relevant context
    '''
    def __init__(self, embedding_model = "text-embedding-3-small", 
                 collection_name: str = "hr-policies", storage_path: str = "./chroma_db",
                 chunk_size = 1000, chunk_overlap = 200):
        self.embedding_model = embedding_model
        self.collection_name = collection_name
        self.storage_path = storage_path
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        self.embeddings = OpenAIEmbeddings(model = embedding_model, dimensions = 1536) #embedding tool
        self.db = None #gets created after adding documents
    
    def add_documents(self, documents: List[Document]):
        #chunk documents, embed and add to database using chroma
        splitter = RecursiveCharacterTextSplitter(chunk_size = self.chunk_size, chunk_overlap = self.chunk_overlap)
        chunks = splitter.split_documents(documents)
        if self.db == None:
            self.db = Chroma(collection_name = self.collection_name, embedding_function = self.embeddings, 
                             persist_directory = self.storage_path)
        self.db.add_documents(chunks)

    def get_retriever(self, k: int = 4, filter: dict = None):
        if not self.db: #if you havent connected to chroma database, connect now
            self.db = Chroma(collection_name = self.collection_name, embedding_function = self.embeddings, 
                             persist_directory = self.storage_path)
        search_kwargs = {"k": k} #how many results should come up
        if filter:
            search_kwargs["filter"] = filter
        retriever = self.db.as_retriever(search_kwargs = search_kwargs)
        return retriever

class RecordStore:
    '''
    Storage database for dictionary types containing metdata about record-type documents, writes documents to json file
    '''
    def __init__(self, file_path: str = "./record_database.json", key_field: str = "employee_id", records: dict = {}):
        self.file_path = file_path
        self.key_field = key_field
        self.records = records
        self.load()
    
    def save(self):
        with open(self.file_path, "w") as f: #"w" signifies write, so we are opening with the intention to write
            json.dump(self.records, f, indent = 2) #serializes records into json format, then dumps into file f
    
    def load(self):
        if os.path.exists(self.file_path): #checking wher file has been created yet
            with open(self.file_path, "r") as f: #"r" signifies read so we open just to get information not change it
                self.records = json.load(f)

    def add_records(self, record_list: List[dict]):
        for r in record_list: #r is a dictionary of one employee's info
            if self.key_field not in r:
                raise KeyError("Key field not found as category in record")
            key = r[self.key_field] #set key in record to be corresponding key_field, e.g. EMP-1001
            self.records[key] = r #set value of key in record to be indi employee dictionary r
        self.save()

    def get_record(self, key: str) -> dict:
        '''
        Returns a dictionary of all info for the relevant key, ex: given "EMP-1001", returns a dictionary of info for EMP-1001.
        If EMP-1001 does not exist as a key (does not match key_field, or is simply not in the database), errors.
        '''
        if key not in self.records:
            raise KeyError(f"{key} not found in records.")
        else:
            return self.records.get(key)

    def get_record_by_field(self, field: str, specific_value: str) -> dict:
        '''
        Returns a dictionary of all info for field differing from default key_field, ex: given "name" and "John Smith", 
        returns a dictionary of info for John Smith if John Smith exists as a value.
        '''
        for record in self.records:
            record_dict = self.records[record]
            if str(record_dict["field", ""]).lower() == str(specific_value).lower(): #e.g., if record_dict["name"] == "John Smith"
                return record_dict
        return None #if not found, return None
    


