
from graph.chains.generation import generation_chain
from graph.state import GraphState
from typing import Any, Dict

def generate(state: GraphState) -> Dict[str, Any]:
    print("---GENERATING---")
    question = state["question"]
    document = state["documents"]
    tool_output = state.get("tool_output", "")

    generation =generation_chain.invoke(
        {"context": document,"question":question,"tool_output":tool_output}
    )
    return {"generation":generation}