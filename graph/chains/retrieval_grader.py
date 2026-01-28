from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from sympy.physics.units import temperature
from ingestion import retriever




load_dotenv()

llm= ChatGoogleGenerativeAI(model="gemini-2.5-flash",temperature=0)

class GradeDocuments(BaseModel):
    """
    Binary score for relevance check on retrieved documents.
    """
    binary_score: str= Field(
    description="Documents are relevant  to the question 'yes' or 'no' ",
    )

structured_llm_grader = llm.with_structured_output(GradeDocuments)

system_prompt="""
    You are a grader assessing relevance of a retrieved document to a user question. 
    If the document contains keyword(s) or semantic meaning related to the user question, grade it as relevant. 
    It does not need to be a stringent test. The goal is to filter out erroneous retrievals.

    Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question.
"""

grade_prompt = ChatPromptTemplate(
    [
        ("system", system_prompt),
        ("human", "Retrieved document :{document} User {question}")
    ]
)

retrieval_grader = grade_prompt | structured_llm_grader
"""
if __name__ == "__main__":

    user_question = "what is the stock market  ? "


    docs = retriever.invoke(user_question)

retrieved_document_content = docs[0].page_content
print(retrieval_grader.invoke(
    {"question": user_question, "document": retrieved_document_content}
))
"""
