from langchain_openai import ChatOpenAI
from langchain_openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

model = ChatOpenAI(
    base_url=os.getenv('MODEL_BASE_URL')
    , api_key=os.getenv('MODEL_API_KEY')
    , model=os.getenv('MODEL_VLM_NAME')
)