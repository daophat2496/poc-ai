from vanna.openai.openai_chat import OpenAI_Chat
from vanna.qdrant.qdrant import Qdrant_VectorStore
from qdrant_client import QdrantClient
import pandas as pd
from dotenv import load_dotenv
import os
from src.database2.database_helpers import DB_CONFIG, get_column_name_and_description
from src.core.vanna_pre_post_process import preprocess_chain, postprocess_chain

load_dotenv()

class MyVanna(Qdrant_VectorStore, OpenAI_Chat):
    def __init__(self, config=None):
        Qdrant_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, config=config)

qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URL")
    , api_key=os.getenv("QDRANT_API_KEY")
)

def get_vanna():
    vn = MyVanna(config={
        'client': qdrant_client
        , 'api_key': os.getenv("OPENAI_API_KEY")
        , 'model': "gpt-4o",
    })

    # vn.connect_to_sqlite('./db/financial_statement.db')
    vn.connect_to_postgres(
        host=DB_CONFIG["host"]
        , dbname=DB_CONFIG["database_name"]
        , user=DB_CONFIG["username"]
        , password=DB_CONFIG["password"]
        , port=DB_CONFIG["port"]
    )

    return vn