import os
from dotenv import load_dotenv
from newsapi import NewsApiClient
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

def initialize_apis():
    """Initialize API clients with API keys from environment variables."""
    news_api_key = os.getenv("0f912b6d3e8d4dce900cb30b6478f6dc")
    groq_api_key = os.getenv("Groq_api_KEY")

    if not news_api_key:
        raise ValueError("NewsAPI key is missing. Please set it in the .env file.")

    if not groq_api_key:
        raise ValueError("Groq API key is missing. Please set it in the .env file.")

    newsapi = NewsApiClient(api_key=news_api_key)
    groq_llm = ChatGroq(
        temperature=0,
        model='mixtral-8x7b-32768',
        groq_api_key=groq_api_key
    )
    return newsapi, groq_llm

load_dotenv()

news_api_key = os.getenv("NEWSAPI_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

print(f"NewsAPI Key: {"0f912b6d3e8d4dce900cb30b6478f6dc"}")
print(f"Groq API Key: {"Groq_api_KEY"}")