from typing import Dict, Any
from graph.chains.retrieval_grader import retrieval_grader
from graph.state import GraphState


def grade_documents_node(state: GraphState) -> Dict[str, Any]:
    """
    Determines whether the retrieved documents are relevant to the question.
    If any document is irrelevant, we set a flag to run web search.
    """
    print("--- CHECKING DOCUMENT RELEVANCE TO QUESTION ---")

    question = state["question"]
    documents = state["documents"]

    print(f"--- RETRIEVED DOCS COUNT: {len(documents) if documents else 0} ---")

    if not documents:
        print("--- NO DOCUMENTS RETRIEVED -> FORCE WEB SEARCH ---")
        return {"documents": [], "question": question, "web_search": True}

    filtered_docs = []
    web_search = False  # Varsayılan olarak kapalı

    for d in documents:
        # LLM'e soruyoruz: Bu döküman soruyla alakalı mı?
        score = retrieval_grader.invoke(
            {"question": question, "document": d.page_content}
        )

        grade = score.binary_score

        # Terminalde ne karar verdiğini görelim
        if grade == "yes":
            print(f"--- GRADE: DOCUMENT RELEVANT ---")
            filtered_docs.append(d)
        else:
            print(f"--- GRADE: DOCUMENT NOT RELEVANT ---")
            # Eğer bir tane bile alakasız çıkarsa veya hiç alakalı kalmazsa web search açılabilir
            # Ama biz burada sadece alakalıları listeye ekliyoruz.

            continue
    if not filtered_docs:
        print("--- ALL DOCUMENTS WERE IRRELEVANT -> FORCE WEB SEARCH ---")
        web_search = True
    else:
        # En az bir relevant döküman varsa web search yapma, generate et
        web_search = False

    return {"documents": filtered_docs, "question": question, "web_search": web_search}