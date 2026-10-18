from langchain.tools import tool
import requests
from dotenv import load_dotenv
import os
from tavily import TavilyClient
from bs4 import BeautifulSoup
from readability import Document
import trafilatura
import re

load_dotenv()

tavily=TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query):
    """
    Search the web for the latest information. 
    """
    results=tavily.search(query=query,max_results=5)
    out=[]
    for res in results['results']:
        out.append(f"Title:{res['title']}\nURL:{res['url']}\nContent:{res['content'][:300]}\n")

    return "\n-----\n".join(out)

@tool
def scrape_url(url):
    """
    Scrape and extract clean readable content from URL.
    """
    response=requests.get(url,timeout=15)
    html=response.text

    extracted=trafilatura.extract(html,include_comments=False,include_tables=False)
    if extracted:
        cleaned=re.sub(r"\s+"," ",extracted)
        return cleaned[:5000]

    doc=Document(html)
    doc_clean=doc.summary()

    soup=BeautifulSoup(doc_clean,"html.parser")
    for tag in soup(["script","style","nav","footer","header","aside","form"]):
        tag.decompose()

    text=soup.get_text(separator=" ",strip=True)

    if text:
        cleaned=re.sub(r"\s+"," ",text)
        return cleaned[:5000]

    return "Could not extract content from the page"
