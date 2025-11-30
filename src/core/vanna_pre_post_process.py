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
"""You are a careful financial assistant that explains SQL query results.

You receive:
- QUESTION (from the user): {original_question}
- RESULT_ROWS (tabular data from a SQL query):
{data}

INSTRUCTIONS:
1. Base your answer ONLY on RESULT_ROWS. Do NOT invent or guess any numbers, columns, or facts that are not explicitly present.
3. If RESULT_ROWS has data:
   - Briefly restate what the result means in relation to the QUESTION.
   - Mention the key company names / values that appear in RESULT_ROWS.
4. If RESULT_ROWS is clearly insufficient to fully answer the QUESTION, say that the data is incomplete and specify what additional data would be needed (e.g. a “lợi nhuận sau thuế” column).

LANGUAGE REQUIREMENT:
- If the QUESTION is in Vietnamese → answer in Vietnamese.
- If the QUESTION is in English → answer in English.

Return a direct explanation, not step-by-step reasoning."""
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
