# from vanna.openai.openai_chat import OpenAI_Chat
from vanna.google.gemini_chat import GoogleGeminiChat
from vanna.qdrant.qdrant import Qdrant_VectorStore
from qdrant_client import QdrantClient
import pandas as pd
from dotenv import load_dotenv
import os
from src.database2.database_helpers import DB_CONFIG, get_column_name_and_description
from src.core.vanna_pre_post_process import preprocess_chain, postprocess_chain
from src.core.model import qdrant_client

load_dotenv(override=True)

class MyVanna(Qdrant_VectorStore, GoogleGeminiChat):
    def __init__(self, config=None):
        Qdrant_VectorStore.__init__(self, config={
            "client": qdrant_client,
        })

        # --- Gemini config (NO OPENAI_* HERE) ---
        gemini_model = os.getenv("ADVANCED_MODEL_NAME") or  os.getenv("MODEL_NAME") or "gemini-2.5-flash"
        gemini_api_key = os.getenv("OPENAI_API_KEY")

        print("MyVanna -> Using Gemini model:", gemini_model)

        GoogleGeminiChat.__init__(self, config={
            "api_key": gemini_api_key,
            "model_name": gemini_model,
            # you can add other Gemini-specific keys if the class supports them
            # e.g. "max_output_tokens": 8192
        })

def get_vanna():
    # vn = MyVanna(config={
    #     'client': qdrant_client
    #     , 'api_key': os.getenv("OPENAI_API_KEY")
    #     , 'model': "gemini-2.5-flash"
    #     , 'base_api_url': os.getenv("OPENAI_BASE_URL")
    #     , 'max_tokens': 10000
    # })
    vn = MyVanna()

    # vn.connect_to_sqlite('./db/financial_statement.db')
    vn.connect_to_postgres(
        host=DB_CONFIG["host"]
        , dbname=DB_CONFIG["database_name"]
        , user=DB_CONFIG["username"]
        , password=DB_CONFIG["password"]
        , port=DB_CONFIG["port"]
    )

    return vn