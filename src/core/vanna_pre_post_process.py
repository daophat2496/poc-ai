from langchain.prompts import PromptTemplate
from src.core.model import model

# Pre-process question
pre_prompt = PromptTemplate.from_template(
"""
You are a financial assistant. Convert the following question into a more formal and precise query suitable for querying a balance sheet database.

The database contains these columns with their description:
{column_list}

Question:
{question}

Return only the normalized version of the question.
"""
)
preprocess_chain = pre_prompt | model

# Post-process response
post_prompt = PromptTemplate.from_template(
"""
Provide a clear and concise explanation of the results in natural language. Result must be in original question language.

Given the original question:
{original_question}

normalized question:
{normalized_question}

And the resulting data:
{data}
"""
)
# post_prompt_template = PromptTemplate(
#     input_variables=["original_question", "normalized_question", "data"]
#     , template=post_prompt,
# )
postprocess_chain = post_prompt | model
