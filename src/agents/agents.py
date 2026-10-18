from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.tools.tools import web_search, scrape_url
from dotenv import load_dotenv
load_dotenv()

llm=ChatOllama(model="qwen3:8B",temperature=0)

def search_agent():
    return create_agent(model=llm,tools=[web_search])

def scrape_agent():
    return create_agent(model=llm,tools=[scrape_url])

writer_prompt=ChatPromptTemplate.from_messages([
    ("system","You are a expert research writer.write clear ,structured insightful reports."),
    ("human",""""write a detailed research report on topic below
    Topic:{topic}
    
    Research gathered
    {research}
    
    structure the report as:
    -Introduction
    -Key findings(minimun 3 well explained points)
    -Conclusion
    -Sources(URLs found in research)
    
    be detailed,factual and professional.
    """),
])

writer_chain=writer_prompt | llm | StrOutputParser()

critic_prompt=ChatPromptTemplate.from_messages([
    ("system","You are a sharp and constructive research critic.Be honest and specific."),
    ("human","""review the research report below and evaluate it strictly.
    Report:{report}
    
    Respond in this exact format:
    Score: X/10
    
    Strengths:
    - ...
    - ...

    Areas to improve:
    - ...
    - ...

    One line verdict:
    - ...
    """),
])

critic_chain=critic_prompt | llm | StrOutputParser()