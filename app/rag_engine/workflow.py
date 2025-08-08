from langgraph.graph.state import CompiledStateGraph
from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode
from rag_engine.nodes import main_node
from rag_engine.state import AgentState


def compile_graph_state(tools_list) -> CompiledStateGraph:
    graph = StateGraph(AgentState)

    # Nodes
    main_node_name = "llm"
    tools_node_name="tools_node"

    graph.add_node(main_node_name, main_node)
    graph.add_node(tools_node_name, ToolNode(tools=tools_list))

    graph.add_conditional_edges(
        "llm",
        lambda state: state["next_step"],
        {
            "tool": tools_node_name,
            "end": END
        }
    )
    graph.add_edge(tools_node_name, main_node_name)
    graph.add_edge(START, main_node_name)

    agent = graph.compile()

    return agent
