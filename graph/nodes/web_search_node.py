from typing import Dict,Any
from graph.chains import retrieval_grader
from graph.state import GraphState
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.documents import Document
from dotenv import load_dotenv
load_dotenv()

web_search_tool = TavilySearchResults(k=3)

def web_search_node(state: GraphState) -> Dict[str, Any]:
    print("---WEB SEARCH---")

    question = state["question"]
    documents = state["documents"]

    docs = web_search_tool.invoke({"query": question})
    web_results = "\n".join([d["content"] for d in docs])
    web_results = Document(page_content=web_results)

    if documents is not None:
        documents.append(web_results)
    else:
        documents = [web_results]

    return {"question": question, "documents": documents}