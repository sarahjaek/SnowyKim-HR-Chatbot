#passes real documents in, embeds, then stores in vector store
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

from typing import List
from langchain_core.documents import Document


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

        self.embeddings = OpenAIEmbeddings(embedding_model, dimensions = 1536) #embedding tool
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
    Storage database for dictionary types containing metdata about record-type documents
    '''
    def __init__(self, )