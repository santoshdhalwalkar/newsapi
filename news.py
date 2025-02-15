import streamlit as st
import os
from newsapi import NewsApiClient
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(page_title="AI News Research Tool", layout="wide")

def initialize_apis():
    """Initialize API clients with keys from environment or user input"""
    news_api_key = os.getenv("0f912b6d3e8d4dce900cb30b6478f6dc") or st.text_input("Enter your NewsAPI Key:", type="password")
    groq_api_key = os.getenv("Groq_api_KEY") or st.text_input("Enter your Groq API Key:", type="password")
    
    if news_api_key and groq_api_key:
        newsapi = NewsApiClient(api_key=news_api_key)
        groq_llm = ChatGroq(
            temperature=0,
            model='mixtral-8x7b-32768',
            groq_api_key=groq_api_key
        )
        return newsapi, groq_llm
    return None, None

def get_news_articles(newsapi, query, days_ago=7):
    """Fetch news articles from NewsAPI"""
    if not newsapi:
        st.error("Please enter your API keys first.")
        return []
    
    from_date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
    
    try:
        response = newsapi.get_everything(
            q=query,
            language='en',
            sort_by='relevancy',
            from_param=from_date
        )
        return response['articles']
    except Exception as e:
        st.error(f"Error fetching news: {str(e)}")
        return []

def summarize_articles(articles):
    """Extract summaries from articles"""
    summaries = []
    for article in articles[:5]:  # Limit to top 5 articles
        summary = article.get("description") or "No description available"
        summaries.append(f"Title: {article['title']}\nSummary: {summary}")
    return "\n\n".join(summaries)

def get_analysis(groq_llm, query, articles):
    """Generate analysis using Groq LLM"""
    if not groq_llm:
        st.error("Please enter your API keys first.")
        return "API keys required."
    
    if not articles:
        return "No articles found for the given query."
    
    template = """You are an AI assistant helping an equity research analyst. Analyze the following news articles and provide a comprehensive summary.

Query: {query}

Articles:
{summaries}

Please provide:
1. Key Points: Main findings and important facts
2. Trends: Identify patterns and market trends
3. Implications: Potential impact on markets and investments
4. Recommendations: Suggested actions or areas to monitor
"""
    
    prompt = PromptTemplate.from_template(template)
    pipeline = prompt | groq_llm
    
    try:
        article_summaries = summarize_articles(articles)
        response = pipeline.invoke({
            "query": query,
            "summaries": article_summaries
        })
        return response.content
    except Exception as e:
        st.error(f"Error generating analysis: {str(e)}")
        return "Error generating analysis. Please try again."

def display_articles(articles):
    """Display news articles in a clean format"""
    for article in articles:
        st.markdown("---")
        st.markdown(f"### {article['title']}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.caption(f"Source: {article['source']['name']}")
        with col2:
            st.caption(f"Published: {article['publishedAt'][:10]}")
        
        if article.get('urlToImage'):
            st.image(article['urlToImage'], use_column_width=True)
        
        st.markdown(article.get('description', 'No description available'))
        st.markdown(f"[Read full article]({article['url']})")

# Main UI
st.title("🔍 AI News Research Tool")
st.markdown("""
This tool helps equity research analysts gather and analyze news articles using AI.
Enter your API keys (if not set in environment variables) and a search query to begin.
""")

# Initialize APIs
newsapi_client, groq_llm = initialize_apis()

# Search interface
query = st.text_input("Enter your search query:")
days = st.slider("Days to look back:", 1, 30, 7)

col1, col2 = st.columns([1, 4])
with col1:
    search_button = st.button("Search & Analyze")

if search_button and query:
    if not newsapi_client or not groq_llm:
        st.error("Please enter both API keys before searching.")
    else:
        with st.spinner("Fetching and analyzing news..."):
            # Get news articles
            articles = get_news_articles(newsapi_client, query, days)
            
            if articles:
                # Display AI analysis
                st.markdown("## 🤖 AI Analysis")
                analysis = get_analysis(groq_llm, query, articles)
                st.markdown(analysis)
                
                # Display articles
                st.markdown("## 📰 News Articles")
                display_articles(articles)
            else:
                st.warning("No articles found for your query.")
