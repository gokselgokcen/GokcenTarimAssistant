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

    filtered_docs = []
    web_search = False  # Varsayılan olarak kapalı

    if not documents:
        print("--- NO DOCUMENTS RETRIEVED: FORCING WEB SEARCH ---")
        return {"documents": [], "question": question, "web_search": True}

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

    # Eğer filtrelenmiş liste boş kaldıysa (hiç alakalı döküman yoksa)
    if not filtered_docs:
        print("--- ALL DOCUMENTS WERE IRRELEVANT: FORCING WEB SEARCH ---")
        web_search = True
    else:
        # Listede eleman var ama acaba yeterli mi?
        # Şimdilik en az 1 tane alakalı varsa web search yapma diyoruz.
        print(f"--- {len(filtered_docs)} DOCUMENTS KEPT ---")
        web_search = False

    return {"documents": filtered_docs, "question": question, "web_search": web_search}