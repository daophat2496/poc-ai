from pydantic import BaseModel, Field
from typing import List

class CatalogSelection(BaseModel):
    """
    Structured decision from LLM:
    - relevant_doc_names: list of doc_name values from catalog that are relevant
      to answer the question. Empty list => no RAG.
    """
    relevant_doc_names: List[str] = Field(
        default_factory=list,
        description="List of doc_name values from the catalog that are relevant to answer the question.",
    )