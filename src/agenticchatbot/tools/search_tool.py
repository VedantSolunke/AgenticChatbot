from langchain_community.tools.tavily_search import TavilySearchResults

from langgraph.prebuilt import ToolNode

def get_tools():
    """
    Returns a list of tools available for the chatbot.
    """
    tools = [TavilySearchResults(max_results=3)]
    return tools


def create_tool_node(tool):
    """
    Creates a ToolNode for the given tool.
    """
    return ToolNode(tools=tool)