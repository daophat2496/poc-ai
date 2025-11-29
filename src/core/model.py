from langchain_openai import ChatOpenAI
from langchain_openai import OpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams
from qdrant_client.http import models as rest
from dotenv import load_dotenv
import os
from io import BytesIO
import shutil

load_dotenv(override=True)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
MODEL_NAME = os.getenv('MODEL_NAME')
OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL')

EMBED_DIM = 1536  # openai embedding dimension

model = ChatOpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
    , model=os.getenv('MODEL_NAME')
    , base_url=os.getenv('OPENAI_BASE_URL')
    , temperature=0.6
    , top_p=0.95
)

model_temp_0 = ChatOpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
    , model=os.getenv('MODEL_NAME')
    , base_url=os.getenv('OPENAI_BASE_URL')
    , temperature=0.0
    , top_p=0.95
)

qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URL")
    , api_key=os.getenv("QDRANT_API_KEY")
)

collections = qdrant_client.get_collections().collections
print(f"List of Qdrant collection: {collections}")

if not any(c.name == "rag_docs" for c in collections):
    qdrant_client.create_collection(
        collection_name="rag_docs",
        vectors_config=VectorParams(size=EMBED_DIM, distance="Cosine"),
    )

if not any(c.name == "rag_docs_catalog" for c in collections):
    qdrant_client.create_collection(
        collection_name="rag_docs_catalog",
        vectors_config=VectorParams(size=EMBED_DIM, distance="Cosine"),
    )

qdrant_client.create_payload_index(
    collection_name="rag_docs",
    field_name="doc_type",
    field_schema=rest.PayloadSchemaType.KEYWORD,
)