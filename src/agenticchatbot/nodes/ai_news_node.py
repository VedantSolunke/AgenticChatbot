from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate
from pathlib import Path

class AINewsNode:
    def __init__(self, llm):
        """ 
        Initializes the AINewsNode with a language model (LLM). and TavilyClient for fetching news.
        """
        self.llm = llm
        self.tavily = TavilyClient()
        self.state = {}
        
        
        
    def fetch_news(self, state: dict)-> dict:
        """
        Fetch AI news based on the specified time frequency
        
        Args:
            state (dict): The state dictionary containing the time frequency for fetching news.
        Returns:
            dict: Updated state with 'news_data' key containing the fetched news data.
        """
        
        frequency = state['messages'][0].content.lower()  # Assuming the first message contains the time frequency
        state['frequency'] = frequency
        self.state['frequency'] = frequency
        time_range_map = {'daily': 'd', 'weekly': 'w', 'monthly': 'm'}
        days_map = {'daily': 1, 'weekly': 7, 'monthly': 30}
        
        
        response = self.tavily.search(
            query="TOP AI technology news",
            topic="news",
            time_range=time_range_map[frequency],
            include_answer ="advanced",
            max_results=10,
            days=days_map[frequency],
            # include_domains=["techcrunch.com", "venturebeat.com", "thenextweb.com", "theverge.com", "wired.com"]
        )
        
        state['news_data'] = response.get('results', [])
        self.state['news_data'] = state['news_data']
        return state
    
    
    def summarize_news(self, state: dict) -> dict:
        """
        Summarizes the fetched AI news using the LLM.
        
        Args:
            state (dict): The state dictionary containing the fetched news data.
        Returns:
            dict: Updated state with 'summary' key containing the summarized news.
        """
        
        news_items = state.get('news_data', [])
        # Create a prompt for summarization
        prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", """You are an AI assistant that summarizes news articles into markdown format. For each item include:
                 
                 - Date in YYYY-MM-DD format in IST time zone
                 - Concise sentence summary of the news article
                 - Sort news by date in descending order (latest news first)
                 - Source of the news article as URL link
                 Use the following format for each news item:
                 #### [Date] - [Summary] ([Source URL])
                 """),
                
                ("user", "Articles:\n {articles}"),
            ]
        )
        
        articles_str = "\n\n".join(
            [
                (
                    f"Title: {item.get('title', '')}\n"
                    f"Content: {item.get('content', '')}\n"
                    f"URL: {item.get('url', '')}\n"
                    f"Date: {item.get('published_date', '')}"
                )
                for item in news_items
            ]
        )
        
        response = self.llm.invoke(prompt_template.format(articles=articles_str))
        state['summary'] = response.content
        self.state['summary'] = state['summary']
        return state
    
    
    
    def save_result(self, state):
        frequency = state['frequency']
        summary = state['summary']
        output_directory = Path('./AINews')
        output_directory.mkdir(parents=True, exist_ok=True)
        filename = output_directory / f"{frequency}_ai_news_summary.md"
        with filename.open('w', encoding='utf-8') as file:
            file.write(f"# AI News Summary ({frequency.capitalize()})\n\n")
            file.write(summary)
        state['filename'] = str(filename)
        state['saved'] = True
        self.state.update(state)
        return state