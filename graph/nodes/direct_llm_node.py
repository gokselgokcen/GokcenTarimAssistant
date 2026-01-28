import os
from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from graph.state import GraphState
from dotenv import load_dotenv

load_dotenv()


def direct_llm_node(state: GraphState) -> Dict[str, Any]:
    """
    Handles general conversation and greetings without using any external tools or RAG.
    """
    print("--- DIRECT LLM NODE (CHITCHAT) ---")

    question = state["question"]

    # We use gemini-1.5-flash for fast conversational responses
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=1  # Higher temperature for a more natural and friendly tone
    )

    # Custom prompt for Gökcen Tarım's assistant persona
    prompt = ChatPromptTemplate.from_template(
        """You are the friendly and professional AI assistant of 'Gökcen Tarım', an agricultural supply store.

        The user says: {question}

        Instructions:
        1. Respond politely and briefly.
        2. If it's a greeting, greet them back warmly in User's Language.
        3. If they ask who you are, explain that you are the Gökcen Tarım AI Assistant.
        4. Do not provide technical agricultural advice here; just handle the conversation.
        5. Always answer in User's Language.

        Answer:"""
    )

    # Simple chain execution
    chain = prompt | llm | StrOutputParser()

    response = chain.invoke({"question": question})

    # We store the final answer in the 'generation' key of our state
    return {"generation": response}