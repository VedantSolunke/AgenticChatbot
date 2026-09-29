
from ..state.state import State


class BasicChatbotNode:
    """
    A basic chatbot node that processes user input and generates responses.
    """

    def __init__(self, model):
        self.llm = model
        
    def process(self, state:State)-> dict:
        """
        Processes the user input from the state and generates a response using the LLM.
        """

        return {"messages" : self.llm.invoke(state['messages'])}