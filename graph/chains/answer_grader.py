from langchain_core.runnables import RunnableSequence
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field




class answer_grader(BaseModel):

    binary_score: bool = Field(
        description="Answer addresses the question 'yes' or 'no'"
    )

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",temperature=0)
structured_llm_grader=llm.with_structured_output(answer_grader)

system_prompt="""
You are a grader assessing whether an answer addresses / resolves a question 
\n Give a binary score 'yes' or 'no'. Yes' means that the answer resolves the question.
"""
answer_prompt=ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "User question: \n\n {question} \n\n LLM generation: {generation}")
    ]
)
answer_grader: RunnableSequence = answer_prompt | structured_llm_grader