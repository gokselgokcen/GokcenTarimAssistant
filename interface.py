import uuid
from graph.graph import app

def launch_app():
    """
    Chat loop for testing

    """
    print("Welcome to Gokcen Tarım ChatBot")
    print(" 'q' for exit ")

    thread_id= str(uuid.uuid4())
    config = {"configurable":{"thread_id":thread_id}}

    while True:
        try:
            user_input = input(f"\nSiz ({thread_id[:4]}...): ")

            if user_input.lower() == "q":
                print("Goodbye")
                break

            print(" ...", end="", flush=True)

            inputs = {"question": user_input}
            final_response = ""

            for event in app.stream(inputs, config=config, stream_mode="values"):
                if "generation" in event and event["generation"]:
                    final_response = event["generation"]

            print(f"\rAgent: {final_response}")

        except Exception as e:
            print(f"\n❌ Hata: {e}")
