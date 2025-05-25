from langchain_openai import ChatOpenAI
from langchain_openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

model = ChatOpenAI(
    base_url="http://220.130.209.122:38058/v1"
    , api_key="token-abc123"
    , model="Qwen/Qwen2.5-VL-7B-Instruct"
    # api_key=os.getenv('OPENAI_API_KEY')
    # , model="gpt-4o"
)