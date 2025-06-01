# DOC-AGENT

A CLI-based tool that analyzes MoEngage documentation articles by extracting article content from a given URL, computing readability scores, and generating feedback on structure, completeness, and style using an LLM via OpenRouter. The analysis is saved as a structured JSON report.
---

## Features

- Fetches article text content using Playwright and BeautifulSoup.
- Performs readability analysis with multiple metrics using textstat.
- Provides feedback on article structure, completeness, and style.
- Saves analysis results to uniquely named JSON files based on the URL.
- Modular design with separate scripts for fetching, analyzing, and main execution.

---
## Project Structure

- *agent1_analyzer.py*: Contains the first agent's logic that analyzes documentation and provides suggestions.
- *doc_revision_agent.py*: Implements the second agent that revises documentation using suggestions from the first agent.
- *run_revision_agent.py*: Script to run the end-to-end process of document analysis and revision.
- *utils/*
  - *fetcher.py*: Contains functionality to fetch article or documentation text.
  - *readability.py*: Handles readability scoring and related text analysis.
- *outputs/*: Directory where output results (like revised docs or analysis JSONs) are saved.
- *.env*: Stores environment variables such as API keys and configurations.
- *requirements.txt*: Lists all required Python packages.
- *venv/*: Python virtual environment directory.
---
## Requirements
- Python 3.8+
- Playwright
- BeautifulSoup4
- textstat
- playwright-stealth (optional for stealth browsing)
- openai (if integrating with OpenAI API for future tasks)
---

## Setup & Installation

1. **Clone the repository and navigate into it:**

```bash
git clone https://github.com/yourusername/doc-analyzer.git
cd doc-analyzer
```
2. **Create and activate a virtual environment:**
```
python -m venv venv
source venv/bin/activate    # Linux/macOS
.\venv\Scripts\activate     # Windows
```
3. **Install Python dependencies:**
```
pip install -r requirements.txt
```
4. **Install Playwright browsers:**
```
playwright install
```
**USAGE**
```
python test.py
```

