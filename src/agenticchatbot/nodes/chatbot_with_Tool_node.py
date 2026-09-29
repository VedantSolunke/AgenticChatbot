from src.agenticchatbot.state.state import State

class ChatbotWithToolNode:
    """
    A chatbot node that can interact with web data using tools.
    """

    def __init__(self, model):
        self.llm = model
        
    def process(self, state: State) -> dict:
        """
        Processes the user input from the state and generates a response using the LLM and tools.
        """
        
        user_input = state['messages'][-1] if state['messages'] else ""
        llm_response = self.llm.invoke([{"role": "user", "content": user_input}])
        
        # simulate tool-specific logic
        tools_response = f"Tool response based on user input: {user_input}"
        
        return {"messages" : [llm_response, tools_response]}
    
    
    def create_chatbot(self, tools):
        """
        Returns a chatbot node function
        """
        
        llm_with_tools = self.llm.bind_tools(tools)
        
        def chatbot_node(state: State) -> dict:
            """ 
            Chatbot logic for processing the input state and returning a response
            """
            
            return {"messages" : [llm_with_tools.invoke(state['messages'])]}
        
        return chatbot_node