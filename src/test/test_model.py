from langchain_core.messages import HumanMessage
from src.core.model import model

# Testing API
prompt = "what is your name?"
messages = [HumanMessage(content=prompt)]
result = model.invoke(messages)
print(result.content)