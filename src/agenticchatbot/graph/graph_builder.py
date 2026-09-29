from langgraph.graph import StateGraph
from ..state.state import State
from langgraph.graph import START, END
from ..nodes.basic_chatbot_node import BasicChatbotNode
from ..tools.search_tool import get_tools, create_tool_node
from langgraph.prebuilt import tools_condition, ToolNode
from ..nodes.chatbot_with_Tool_node import ChatbotWithToolNode
from src.agenticchatbot.nodes.ai_news_node import AINewsNode

class GraphBuilder:
    def __init__(self, model):
       self.llm = model
       self.graph_builder = StateGraph(State)
       
    
    def basic_chatbot_build_graph(self):
        """
        Builds a basic chatbot graph with a single node that uses the provided LLM.
        """
        
        self.basic_chatbot_node = BasicChatbotNode(self.llm)
        
        self.graph_builder.add_node("chatbot", self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_edge("chatbot", END)
        
        
    def chatbot_with_web_build_graph(self):
        """
        Builds a chatbot graph that can interact with web data.
        """
        ## define the tool and tool node
        tools = get_tools()
        tool_node = create_tool_node(tools) 
        
        ## define the llm
        llm = self.llm
        
        ## define the chatbot node
        obj_chatbot_with_node = ChatbotWithToolNode(llm)
        chatbot_node = obj_chatbot_with_node.create_chatbot(tools)
        ## add nodes
        
        self.graph_builder.add_node("chatbot", chatbot_node)
        self.graph_builder.add_node("tools", tool_node)
        
        ## define conditional and direct edges
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_conditional_edges("chatbot", tools_condition )
        self.graph_builder.add_edge("tools", "chatbot")                                                 
    
    
    def ai_news_builder_graph(self):
        
        ai_news_node = AINewsNode(self.llm)
        
        ## added the nodes
        self.graph_builder.add_node("fetch_news", ai_news_node.fetch_news)
        self.graph_builder.add_node("summarize_news", ai_news_node.summarize_news)
        self.graph_builder.add_node("save_result", ai_news_node.save_result)
        
        #added the edges
        self.graph_builder.add_edge(START, "fetch_news")
        self.graph_builder.add_edge("fetch_news", "summarize_news")
        self.graph_builder.add_edge("summarize_news", "save_result")
        self.graph_builder.add_edge("save_result", END)
        

    
    def setup_graph(self, usecase: str):
        """
        Sets up the graph based on the selected usecase.
        """
        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()
        
        elif usecase == "Chatbot with Web":
            self.chatbot_with_web_build_graph()
        elif usecase == "AI News":
            self.ai_news_builder_graph()
            
        return self.graph_builder.compile()