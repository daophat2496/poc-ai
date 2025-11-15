from langchain_openai import ChatOpenAI
from langchain_openai import OpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv
import os

load_dotenv(override=True)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
MODEL_NAME = os.getenv('MODEL_NAME')
OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL')

model = ChatOpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
    , model=os.getenv('MODEL_NAME')
    , base_url=os.getenv('OPENAI_BASE_URL')
    , temperature=0.6
    , top_p=0.95
)


def stream_translate_live(text: str):
    text = text.strip()
    if not text:
        yield ""
        return

    messages = [
        SystemMessage(
            content=(
                "You are a translation engine. "
                "Translate from Vietnamese to English. "
                "Return only the translation, no explanations."
            )
        ),
        HumanMessage(content=text),
    ]

    partial = ""
    for chunk in model.stream(messages):
        if chunk.content:
            partial += chunk.content
            yield partial