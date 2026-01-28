from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from graph.nodes import generation_node
from graph.state import GraphState
from graph.node_constants import * # All constants imported
from graph.chains.hallucination_grader import hallucination_grader
from graph.chains.answer_grader import answer_grader



# Nodes import
from graph.nodes.retrieve_node import retrieve_node
from graph.nodes.grade_documents_node import grade_documents_node
from graph.nodes.generation_node import generate
from graph.nodes.web_search_node import web_search_node
from graph.nodes.airtable_node import airtable_node
from graph.nodes.direct_llm_node import direct_llm_node


from graph.chains.router import question_router

def route_question(state: GraphState):
    print("---DECIDING TO ROUTE QUESTION---")
    question=state["question"]
    source= question_router.invoke({"question":question})
    state["product_name"] = source.product_name

    print(f"--- ROUTER KARARI: {source.datasource} | ÜRÜN: {source.product_name}")

    if source.datasource.lower() == "airtable":
        print("---Route Airtable---")
        return AIRTABLE
    elif source.datasource.lower() == "direct_response":
        print("---Route LLM---")
        return DIRECT_LLM
    elif source.datasource.lower() == "chat_history":
        print("---Route Chat-History in Generate node---")
        return GENERATE
    else:
        print("---RAG---")
        return RETRIEVE

def decide_to_generate(state: GraphState):
    """
        Dökümanlar kontrol edildikten sonra (Grade),
        cevap mı üretilecek yoksa Web Search mü yapılacak karar verir.
    """
    print("---ASSESING GRADED DOCUMENT---")
    web_search= state.get("web_search",False)

    if web_search:
        print("---DECISION TO WEB-SEARCH---")
        return WEBSEARCH
    else:
        print("---DECISION TO GENERATE---")
        return GENERATE


def grade_generation_grounded_in_documents_and_questions(state: GraphState):
    print("----CHECK HALLUCINATION----")
    question=state["question"]
    documents= state["documents"]
    generation= state["generation"]

    score = hallucination_grader.invoke(
        {"documents": documents, "generation": generation}
    )

    if hallucation_grader:= score.binary_score:
        print("GENERATION IS GROUNDED IN DOCUMENTS")
        score = answer_grader.invoke({"question":question,"generation":generation})
        if answer_grade := score.binary_score:
            print("GENERATION ADDRESSES QUESTION")
            return "useful"
        else:
            print("GENERATION DOES NOT ADDRESSES QUESTION")
            return "not useful"
    else:
        print("GENERATION IS NOT GROUNDED IN DOCUMENTS")
        return "not supported"

workflow=StateGraph(GraphState)

workflow.add_node(RETRIEVE, retrieve_node)
workflow.add_node(GRADE_DOCUMENTS, grade_documents_node)
workflow.add_node(GENERATE, generate)
workflow.add_node(WEBSEARCH, web_search_node)
workflow.add_node(AIRTABLE, airtable_node)
workflow.add_node(DIRECT_LLM, direct_llm_node)


(workflow.set_conditional_entry_point
    (
    route_question,
    {
        AIRTABLE:AIRTABLE,
        DIRECT_LLM:DIRECT_LLM,
        WEBSEARCH:WEBSEARCH,
        RETRIEVE: RETRIEVE,
        #chat_hist routing
        GENERATE:GENERATE,

    }
))

workflow.add_edge(RETRIEVE, GRADE_DOCUMENTS)

workflow.add_conditional_edges(GRADE_DOCUMENTS, decide_to_generate,
                               {
                                   WEBSEARCH:WEBSEARCH,
                                   GENERATE:GENERATE,
                               })

workflow.add_conditional_edges(
    GENERATE,
    grade_generation_grounded_in_documents_and_questions,
    {
        "useful": END,               # Her şey yolunda, cevabı ver.
        "not supported": GENERATE,   # Uydurma varsa tekrar dene.
        "not useful": WEBSEARCH,  # Cevap dökümanda var ama yetersizse Web'e git.
    },
)
workflow.add_edge(WEBSEARCH,GENERATE)


workflow.add_edge(AIRTABLE, GENERATE)
workflow.add_edge(DIRECT_LLM, END)

memory = MemorySaver()

app = workflow.compile(checkpointer=memory)
app.get_graph().draw_mermaid_png(output_file_path="graph.png")