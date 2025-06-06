from langchain_openai import ChatOpenAI
from langchain_openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv(override=True)

model = ChatOpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
    , model=os.getenv('MODEL_NAME')
    , base_url=os.getenv('OPENAI_BASE_URL')
    , temperature=0.6
    , top_p=0.95
)