from langchain_core.runnables import RunnableSequence
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from dotenv import load_dotenv


load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",temperature=0)

class GradeHallucination(BaseModel):
    """Binary score for hallucination present in generated answer"""
    binary_score: str= Field(
    description="Answer is grounded in the facts, 'yes' or 'no' .",
    )

structured_llm_grader =llm.with_structured_output(GradeHallucination)

system_prompt= """
You are a grader assessing whether an LLM generation is grounded in / supported by a set of retrieved facts.
\nGive a binary score 'yes' or 'no'. 
\n'Yes' means that the answer is grounded in / supported by the set of facts.
"""

hallucination_prompt =(
    [
        ("system", system_prompt),
        ("human", "Set of facts: \n\n {documents} \n\n LLM generation: {generation}"),
    ]
)

hallucination_grader: RunnableSequence = hallucination_prompt | structured_llm_grader