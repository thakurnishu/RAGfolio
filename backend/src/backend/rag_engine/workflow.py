from langgraph.graph.state import CompiledStateGraph
from backend.rag_engine.state import AgentState
from langgraph.graph import StateGraph, END, START
from backend.rag_engine.nodes import main_node
from langgraph.prebuilt import ToolNode
from backend.rag_engine.tools import tools as tools_list


def compile_graph_state() -> CompiledStateGraph:
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
