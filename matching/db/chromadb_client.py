## main.py 실행시 연결되는 chromadb

import os
from dotenv import load_dotenv, find_dotenv
from chromadb.utils import embedding_functions
from chromadb import HttpClient

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)



def get_chroma_client():
    return HttpClient(
        host = os.getenv("CHROMA_HOST"),
        port = os.getenv("CHROMA_PORT"),
    )
    

def get_user_latest_collection():
    return get_chroma_client().get_or_create_collection(
        name="user_latest", embedding_function=None
    )

def get_user_history_collection():
    return get_chroma_client().get_or_create_collection(
        name="user_history", embedding_function=None
    )