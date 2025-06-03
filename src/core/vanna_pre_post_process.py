from langchain.prompts import PromptTemplate
from src.core.model import model

# Pre-process question
pre_prompt = PromptTemplate.from_template(
"""
You are a financial assistant. Convert the following question into a more formal and precise question suitable for querying a balance sheet database.

Question:
{question}

The database contains these columns with their description:
{column_list}

Return only the normalized version of the question."""
)
preprocess_chain = pre_prompt | model

post_prompt = PromptTemplate.from_template(
"""Analyze the data below and explain the results in clear language.

**LANGUAGE REQUIREMENT:** Match the language of your response to the language of the QUESTION.
- If the QUESTION is in Vietnamese → respond in Vietnamese
- If the QUESTION is in English → respond in English

QUESTION: {original_question}

DATA TO ANALYZE: {data}

Provide an explanation of what the data shows in relation to the question."""
)
# post_prompt = PromptTemplate.from_template(
# """Provide a clear and concise explanation of the results in natural language.
# **IMPORTANT** Result must be in language of QUESTION: if the QUESTION is in Vietnamese, you must answer in Vietnamese. If the QUESTION is in English, you must answer in English
# Given the QUESTION:
# {original_question}
# And the resulting data:
# {data}"""
# )
# post_prompt = PromptTemplate.from_template(
# """
# Provide a clear and concise explanation of the results in natural language. Result must be in language of original question.
# - If the original question is in Vietnamese, you must answer in Vietnamese
# - If the original question is in English, you must answer in English

# Given the original question:
# {original_question}

# normalized question:
# {normalized_question}

# And the resulting data:
# {data}
# """
# )

postprocess_chain = post_prompt | model
