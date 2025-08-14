from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages

class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

class InitialScreeningModelResponse(TypedDict):
    """The initial screening result response for the candidate based on candidate's CV and
    company skills requirements that should also display the skills extracted from the CV and the
    percentage match with the company skills"""
    name: str
    candidate_cv_summary: str
    matched_skills: list[str]
    non_matched_skills: list[str]
    matched_skills_percentage: int