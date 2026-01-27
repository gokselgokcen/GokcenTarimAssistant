from graph.state import GraphState
from utils.airtable_client import get_product_price, create_lead
from graph.chains.router import question_router  # Router'ı içeri aktar


def airtable_node(state: GraphState):
    print("----AirTable Connection----")
    question = state.get("question", "")
    message = state.get("messages", [])


    source = question_router.invoke({"question": question})
    product_name = source.product_name

    print(f"--- AIRTABLE NODE'DA YAKALANAN ÜRÜN: '{product_name}' ---")

    # 2. Ürün ismi bulunduysa sorgula
    if product_name:

        search_term = "Üre" if "üre" in product_name.lower() else product_name

        print(f"--- Searching {search_term} in table ---")
        results = get_product_price(search_term)

        print(f"--- DEBUG: AIRTABLE SORGUSU SONUCU: {results} ---")

        # return içinde 'product_name' döndürerek artık State'e KALICI olarak yazıyoruz
        return {"tool_output": results, "product_name": search_term, "messages": message}

    # 3. Eğer ürün değil de müşteri kaydıysa
    customer_info = source.customer_info
    if customer_info:
        print("-- Customer card is creating --")
        results = create_lead(**source.customer_info)
        return {"tool_output": results, "messages": message}

    return {"tool_output": "Ürün veya müşteri bilgisi tespit edilemedi.", "messages": message}