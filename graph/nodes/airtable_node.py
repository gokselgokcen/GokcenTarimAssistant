from langchain_core.messages import AIMessage

from graph.state import GraphState
from utils.airtable_client import get_product_price, create_lead, get_all_products ,get_product_search_pool
from graph.chains.router import question_router
from rapidfuzz import process, fuzz


def airtable_node(state: GraphState):
    print("----AirTable Connection----")
    question = state.get("question", "")
    message = state.get("messages", [])


    source = question_router.invoke({"question": question})
    product_name = source.product_name

    print(f"--- AIRTABLE NODE'DA YAKALANAN ÜRÜN: '{product_name}' ---")

    # 3. Eğer ürün değil de müşteri kaydıysa
    customer_info = source.customer_info
    if customer_info:
        print("-- Customer card is creating --")
        results = create_lead(**source.customer_info)
        return {"tool_output": results, "messages": message}

    if not source.product_name:
        print("--- Ürün Listesi Hazırlanıyor ---")
        # Airtable'dan tüm kayıtları çek (get_all_products_with_prices fonksiyonunu yazmalısın)
        all_data = get_all_products()

        output_text = ", ".join(all_data) if isinstance(all_data, list) else str(all_data)
        return {"tool_output": output_text, "messages": state.get("messages", [])}

    # 2. Ürün ismi bulunduysa sorgula
    if product_name:

        search_pool = get_product_search_pool()

        candidates = list(search_pool.keys())
        match = process.extractOne(product_name.lower(), candidates, scorer=fuzz.token_set_ratio)

        search_term = None

        if match and match[1] > 60:
            matched_alias = match[0]  # Örn: "şeker" veya "3 15"
            search_term = search_pool[matched_alias]  # Örn: "AS" veya "15.15.15" (RESMİ AD)

            print(
                f"--- EŞLEŞME BAŞARILI: '{product_name}' -> '{matched_alias}' -> Asıl: '{search_term}' (Skor: {match[1]}) ---")
        else:
            print(f"--- EŞLEŞME BULUNAMADI: {product_name} ---")

        if search_term:
            results = get_product_price(search_term)
            # Yapılan işlemi hafızaya ekle
            log_msg = AIMessage(content=f"Veritabanında '{search_term}' ({product_name}) sorgusu yapıldı.")
        else:
            # Bulunamadıysa net cevap ver, Web Search'e gitmesin
            results = "STOKTA_YOK: Aradığınız ürün veritabanımızda bulunamadı."
            log_msg = AIMessage(content=f"'{product_name}' ürünü stokta yok.")

        return {"tool_output": results, "product_name": search_term, "messages": [log_msg]}






    return {"tool_output": "Ürün veya müşteri bilgisi tespit edilemedi.", "messages": message}