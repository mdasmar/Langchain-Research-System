# LangChain Research System

An AI-powered research assistant built with **LangChain**, **Azure OpenAI**, **Tavily Search**, and **Streamlit**. It searches the web for a topic, extracts content from a relevant page, drafts a structured research report, and asks a critic chain to evaluate the report.
 

## Features

- **Web search:** Uses Tavily to retrieve search results for a research query.
- **Content extraction:** Fetches a selected URL and extracts readable text using Trafilatura, with Readability and BeautifulSoup.
- **Report generation:** Uses an Azure OpenAI deployment through LangChain to draft a report with an introduction, key findings, conclusion, and source URLs.
- **Critic review:** Evaluates the generated report and returns a score, strengths, improvement areas, and a verdict.
- **Streamlit UI:** Submit a topic, view the outputs in separate tabs, and download search results, extracted content, the report, and critic feedback.
- **Recent topics:** Keeps a short history of research topics in the current Streamlit session.

## How it works

The application runs the following workflow:

1. **Search agent** — calls the `web_search` tool to find relevant information and URLs.
2. **Reader agent** — selects a relevant URL from the search output and calls `scrape_url` to extract page content.
3. **Writer chain** — combines search results and extracted content into a structured research report.
4. **Critic chain** — reviews the report and returns a score and actionable feedback.
5. **Streamlit interface** — displays each stage's output and offers downloads.

The agents and chains are defined in `src/agents/agents.py`; the tools are in `src/tools/tools.py`; and the workflow is orchestrated by `src/pipelines/pipeline.py`.

## Project structure

```text
Langchain-Research-System/
├── app.py                    # Streamlit user interface
├── requirements.txt           # Python dependencies
├── .env_example               # Example environment-variable template
├── .gitignore                 # Files excluded from version control
├── test.py                    # Example script for testing backend components
└── src/
    ├── __init__.py
    ├── agents/
    │   ├── __init__.py
    │   └── agents.py          # Azure OpenAI model, agents, writer and critic chains
    ├── pipelines/
    │   ├── __init__.py
    │   └── pipeline.py        # End-to-end research workflow
    └── tools/
        ├── __init__.py
        └── tools.py           # Tavily search and web-page extraction tools
```

## Requirements

- Python **3.11** (the recommended version for this project)
- An Azure OpenAI resource and a deployed chat model compatible with the configured API endpoint
- A Tavily API key
- Internet access for Tavily searches and fetching web pages

Python dependencies are listed in `requirements.txt`, including LangChain, `langchain-openai`, Streamlit, Tavily, Requests, BeautifulSoup, Readability, Trafilatura, and `python-dotenv`.

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/mdasmar/Langchain-Research-System.git
cd Langchain-Research-System
```

### 2. Create and activate a Conda environment

```bash
conda create -n research python=3.11 -y
conda activate research
```

If you do not use Conda, create a virtual environment with Python 3.11 instead:

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a local `.env` file in the project root, next to `app.py`, using `.env_example` as a reference. Add your own credentials and deployment details; do not commit the `.env` file.

## Environment variables

The backend reads the following environment variables:

| Variable | Purpose |
|---|---|
| `AZURE_OPENAI_ENDPOINT` | Base endpoint for your Azure OpenAI resource |
| `AZURE_OPENAI_API_KEY` | API key for the Azure OpenAI resource |
| `AZURE_OPENAI_DEPLOYMENT_NAME` | Name of the deployed model used by the application |
| `TAVILY_API_KEY` | API key used by Tavily web search |

Example `.env` format (replace the placeholder values with your own):

```dotenv
AZURE_OPENAI_ENDPOINT=https://YOUR-RESOURCE.openai.azure.com
AZURE_OPENAI_API_KEY=your-azure-openai-api-key
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
TAVILY_API_KEY=your-tavily-api-key
```


## Run the application

From the project root, with your environment activated and `.env` configured:

```bash
streamlit run app.py
```

Streamlit will print a local URL (usually `http://localhost:8501`). Open that URL in your browser.

To stop the app, press `Ctrl+C` in the terminal.

## Use the Streamlit interface

1. Enter a focused research question or topic in the **Research topic** field.
2. Select **Start Research**.
3. Wait while the backend runs the search, extraction, report-writing, and critic stages.
4. Review the output in the **Search Results**, **Extracted Content**, **Final Report**, and **Critic Review** tabs.
5. Use the download buttons to save the outputs. The final report is downloadable as Markdown (`.md`).
6. Use **Clear current results** in the sidebar to clear the displayed result and topic.

Research runs synchronously, so the interface waits for the pipeline to finish. The recent-topic list is stored in Streamlit session state and is not a persistent database.

## Run the backend from Python

You can call the pipeline directly without the Streamlit UI:

```python
from src.pipelines.pipeline import research_pipeline

topic = "How generative AI is changing education"
result = research_pipeline(topic)

print(result["report"])
print(result["feedback"])
```

Run this from the project root so Python can resolve the `src` package.

## Pipeline output

`research_pipeline(topic)` returns a dictionary with these keys:

| Key | Description |
|---|---|
| `search_result` | Text returned by the search agent |
| `scrape_content` | Extracted page content returned by the reader agent |
| `report` | Final research report generated by the writer chain |
| `feedback` | Critic's evaluation of the report |

The Streamlit interface expects all four keys to be present.




