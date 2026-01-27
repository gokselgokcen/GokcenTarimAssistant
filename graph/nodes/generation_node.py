
from graph.chains.generation import generation_chain
from graph.state import GraphState
from typing import Any, Dict


def generate(state: GraphState) -> Dict[str, Any]:
    print("---GENERATING---")
    question = state["question"]
    document = state.get("documents", [])
    tool_output = state.get("tool_output", "")
    messages = state.get("messages", [])
    chat_history_str = ""

    for m in messages[:-1]:
        role = "User" if m.type == "human" else "Assistant"
        chat_history_str += f"{role}: {m.content}\n"

    generation =generation_chain.invoke(
        {"context": document,"question":question,"tool_output":tool_output,"chat_history": chat_history_str}
    )


    return {"generation":generation}