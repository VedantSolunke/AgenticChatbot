import streamlit as st
from .UI.streamlitUI.loadUI import LoadStreamlitUI
from .LLMs.groqllm import GroqLLM
from .graph.graph_builder import GraphBuilder
from .UI.streamlitUI.display_result import DisplayResultStreamlit

def load_langgraph_agentic_app():
    ''''
    Load the LangGraph Agentic Chatbot application using Streamlit.
    '''
    
    ## load the UI
    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()
    
    if not user_input:
        st.error("Error : Failed to load user input. Please check the configuration.")
        return
    
    if st.session_state.IsFetchButtonClicked:
        user_message = st.session_state.timeframe
    else:
        user_message = st.chat_input("Enter your message here...")
    

    if user_message:
        try:
            ## configure the llm
            
            obj_llm_config = GroqLLM(user_controls_input=user_input)
            model = obj_llm_config.get_llm_model()
            
            if not model:
                st.error("Error: Failed to initialize the LLM model. Please check your API key and model selection.")
                return
            
            # Initialize and setup up the graph based on the selected usecase
            
            usecase = user_input['selected_usecase']
            
            if not usecase:
                st.error("Error: No usecase selected. Please select a usecase from the sidebar.")
                return
            
            ## Graph Builder
            
            graph_builder = GraphBuilder(model)
            
            try:
                graph = graph_builder.setup_graph(usecase)
                DisplayResultStreamlit(usecase, graph, user_message).display_result_on_ui()
                
            except Exception as e:
                st.error(f"Error setting up the graph for usecase '{usecase}': {e}")
                return
        except Exception as e:
            st.error(f"Error initializing the LLM model: {e}")
            return