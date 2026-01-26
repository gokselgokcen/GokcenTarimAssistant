from typing import Any, Dict
from graph.state import GraphState
# We use the retriever you already defined in your ingestion file
from ingestion import retriever


def retrieve_node(state: GraphState) -> Dict[str, Any]:
    """
    Retrieves relevant documents from the vectorstore based on the user's question.
    It does NOT generate an answer; it only populates the 'documents' field in the state.
    """
    print("--- RETRIEVING DOCUMENTS ---")

    # Extract the question from the current state
    question = state["question"]

    # Fetch relevant document chunks from ChromaDB
    # Using the 'retriever' object imported from ingestion.py
    documents = retriever.invoke(question)

    # Update the state with the retrieved documents.
    # The 'generation' will be handled by the next node in the graph.
    return {
        "documents": documents,
        "question": question
    }