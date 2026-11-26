# 🔬 ResearchAI — AI Research Assistant

An intelligent research workspace powered by a multi-agent AI pipeline. Give it a topic and it automatically searches the web, scrapes relevant sources, writes a structured report, and critiques it — all in one click.

---

## 🤖 How It Works

The pipeline runs four AI components in sequence:

| Step | Component | Role |
|------|-----------|------|
| 1 | **Search Agent** | Searches the web for relevant sources using Tavily |
| 2 | **Reader Agent** | Scrapes and extracts content from the top URLs |
| 3 | **Writer Chain** | Generates a structured research report |
| 4 | **Critic Chain** | Reviews and scores the report out of 10 |

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| [Streamlit](https://streamlit.io/) | Web UI framework |
| [LangChain](https://www.langchain.com/) | Agent and chain orchestration |
| [OpenRouter](https://openrouter.ai/) | LLM API provider (NVIDIA Nemotron) |
| [Tavily](https://tavily.com/) | AI-powered web search API |
| [Trafilatura](https://trafilatura.readthedocs.io/) | Web content extraction |
| [Readability-lxml](https://github.com/buriy/python-readability) | HTML article extraction |
| [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) | HTML parsing |
| [Requests](https://requests.readthedocs.io/) | HTTP client |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | Environment variable management |
| [Rich](https://rich.readthedocs.io/) | Terminal output formatting |
| [uv](https://docs.astral.sh/uv/) | Python package and project manager |

---

## ⚙️ Local Setup

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) installed
- A free [Tavily API key](https://tavily.com/)
- A free [OpenRouter API key](https://openrouter.ai/keys)

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ai-research-assistant.git
cd ai-research-assistant
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
TAVILY_API_KEY=your_tavily_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### 4. Run the Streamlit app

```bash
uv run streamlit run app.py
```

The app will open at `http://localhost:8501`.

### 5. (Optional) Run the pipeline directly

```bash
uv run python main.py
```

---

## 📁 Project Structure

```
ai-research-assistant/
├── app.py                  # Streamlit UI
├── main.py                 # CLI entry point
├── pyproject.toml          # Project config & dependencies
├── .env                    # API keys (not committed)
└── src/
    ├── agents/
    │   └── agents.py       # Search agent, Reader agent, Writer & Critic chains
    ├── pipelines/
    │   └── pipeline.py     # Orchestrates the full research pipeline
    └── tools/
        └── tools.py        # web_search and scrape_url tools
```

---

## 🔑 Getting API Keys

- **Tavily** — Sign up at [tavily.com](https://tavily.com/) → free tier includes 1,000 searches/month
- **OpenRouter** — Sign up at [openrouter.ai](https://openrouter.ai/) → free tier available with several free models
