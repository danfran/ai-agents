from IPython.display import display
from langgraph.graph import StateGraph
from model import State
from recruiting_agent import recruiter_control


def build_graph():
    graph_builder = StateGraph(State)
    graph_builder.add_node('recruiter_control', recruiter_control)
    graph_builder.set_entry_point('recruiter_control')
    graph_builder.set_finish_point('recruiter_control')
    graph = graph_builder.compile()

    display(graph.get_graph().draw_ascii())

    return graph