import uuid
from graph.graph import app  # LangGraph workflow'unuzu içeren dosya


def run_chat_loop():
    print("\n--- GÖKCEN TARIM AI ASİSTANINA HOŞ GELDİNİZ ---")
    print("(Çıkmak için 'exit' veya 'quit' yazabilirsiniz)\n")

    # Her kullanıcı için benzersiz bir session ID (İleride veritabanı için lazım olur)
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}

    # Hafızayı (Memory) state içinde tutmak için boş başlatıyoruz
    # GraphState içindeki 'messages' listesini burada yöneteceğiz
    state = {
        "messages": [],
        "documents": [],
        "product_name": None,
        "tool_output": ""
    }

    while True:
        user_input = input("Siz: ")

        if user_input.lower() in ["exit", "quit", "çıkış"]:
            print("Gökcen Tarım: İyi günler dileriz!")
            break

        # State'e soruyu ekle
        state["question"] = user_input

        # Graph'ı çalıştır
        try:
            # stream veya invoke kullanabilirsin.
            # stream her adımı terminalde görmeni sağlar.
            for output in app.stream(state, config):
                for key, value in output.items():
                    # Adım isimlerini takip et (Opsiyonel: Debug için)
                    print(f"--- Biten Adım: [{key}] ---")

                    # Eğer state güncelleniyorsa, yerel state'i güncelle
                    # Bu sayede 'messages' listesi her adımda dolar
                    state.update(value)

            # En son üretilen cevabı yazdır
            print(f"\nASİSTAN: {state.get('generation')}\n")

        except Exception as e:
            print(f"Bir hata oluştu: {e}")


if __name__ == "__main__":
    run_chat_loop()