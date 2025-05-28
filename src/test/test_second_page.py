from src.core.balance_sheet import model, encode_image, query_model_with_image_b64
from src.prompts.balance_sheet import PROMPT_IS_BALANCE_SHEET_CONT, PROMPT_IS_BALANCE_SHEET_FIRST
from langchain_core.messages import HumanMessage

prompt = f"""
I am giving you below REFERENCE QUESTION with 2 images. Explain (not answer the below REFERENCE QUESTION) why you say the second one is not a balance sheet:
- Review the REFERENCE QUESTION below to know what I ask you to do
- The result you give for that REFERENCE QUESTION was "No" (I tried to ask many time)
- Explain why you answered "No"
- Advice how I can improve the question (with the same template), this second image IS a part of balance sheet

==== REFERENCE QUESTION ====
{PROMPT_IS_BALANCE_SHEET_CONT}
"""

image1 = ".\image\page_009.jpg"
image2 = ".\image\page_010.jpg"

message = HumanMessage(
    content=[
        {"type": "text", "text": prompt}
        , {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encode_image(image1)}"}}
        , {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encode_image(image2)}"}}
    ]
)

response = model.invoke([message])
print(response.content)