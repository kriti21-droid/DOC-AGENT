# DOC-AGENT

A CLI-based tool that analyzes MoEngage documentation articles by extracting article content from a given URL, computing readability scores, and generating feedback on structure, completeness, and style using an LLM via OpenRouter. The analysis is saved as a structured JSON report.

---

## Setup & Installation

1. **Clone the repository and navigate into it:**

```bash
git clone https://github.com/yourusername/doc-analyzer.git
cd doc-analyzer
```
2. **Create and activate a virtual environment:**
```
bash
Copy
Edit
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

