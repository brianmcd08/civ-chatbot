# Civilization 6 BBG Chatbot

A RAG-based chatbot that answers questions about the Better Game Balance (BBG) mod for Civilization VI. Ask it about unit stats, leader abilities, balance changes across versions, wonders, policies, and more — with full awareness of which BBG version introduced or changed something.

---

## How it works

1. **Scraping** — BeautifulSoup scrapers pull data from the BBG patch notes pages across 14 versions (`base_game` through `v7.4`), covering units, leaders, buildings, wonders, policies, great people, changelogs, and more.
2. **Ingestion** — Scraped entries are embedded with OpenAI's `text-embedding-3-small` model and stored in a local Chroma vector database.
3. **Retrieval** — At query time, a version extractor (Claude) parses the user's question to determine which BBG version they're asking about and which section of data is most relevant. The retriever then performs a filtered similarity search.
4. **Generation** — Retrieved documents are passed to Claude along with the original question to generate a response.
5. **UI** — A Streamlit app serves the chatbot with session-based conversation history.

---

## Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip
- An **Anthropic API key**
- An **OpenAI API key** (used only for embeddings)

---

## Setup

**1. Clone the repo**

```bash
git clone https://github.com/brianmcd08/civilization-chatbot.git
cd civilization-chatbot
```

**2. Install dependencies**

```bash
uv sync
```

Or with pip:

```bash
pip install -r requirements.txt
```

**3. Configure environment variables**

Copy the example env file and fill in your API keys:

```bash
cp example.env .env
```

The required keys are:

```
ANTHROPIC_API_KEY=""
ANTHROPIC_MODEL=""
OPENAI_API_KEY=""
```

The remaining keys in `example.env` (LangSmith, Tavily, Pinecone) are optional and unused by default.

**4. Build the vector database**

This scrapes all BBG patch note pages and embeds them into a local Chroma database. It makes a large number of HTTP requests to the BBG site and calls the OpenAI embeddings API — expect it to take several minutes.

```bash
python -m src.ingestion.ingester
```

The database will be saved to `./chroma_langchain_db/`.

**5. Run the app**

```bash
streamlit run app.py
```

---

## Project structure

```
src/
├── scraping/           # One scraper per BBG data section
│   ├── scrape_orchestrator.py  # Runs all scrapers
│   ├── scrape_units.py
│   ├── scrape_leaders.py
│   ├── scrape_changelogs.py
│   └── ...
├── ingestion/
│   └── ingester.py     # Embeds scraped data into Chroma
├── retrieval/
│   └── retriever.py    # Version- and section-aware similarity search
├── chains/
│   ├── version_extractor.py    # Parses version and section from query
│   ├── rag_pipeline.py         # Wires extractor → retriever
│   └── response_generator.py  # Final LLM call with retrieved context
├── schema.py           # UnifiedEntry and ParsedInput data models
└── config.py           # Version and Section enums
app.py                  # Streamlit UI
```

---

## Querying

The chatbot understands version-specific and cross-version questions:

| Query | Behaviour |
|---|---|
| "What does the Eagle Warrior do?" | Searches BBG v7.4 (latest) |
| "What did the Knight cost in v6.5?" | Filters to v6.5 |
| "Which versions have the Eagle Warrior?" | Searches across all versions |
| "What are the ranged unit promotions?" | Targets the promotions section |

---

## Re-ingestion

If you modify any scraper or the `generate_embedding_text()` method in `schema.py`, delete the existing database before re-running the ingester to avoid stale embeddings:

```bash
rm -rf ./chroma_langchain_db
python -m src.ingestion.ingester
```

---

## Running tests

```bash
pytest
```

---

## BBG versions covered

`base_game`, `5.6`, `5.7`, `5.8`, `6.0`, `6.1`, `6.2`, `6.3`, `6.4`, `6.5`, `7.1`, `7.2`, `7.3`, `7.4`

---

## Limitations

- **Base game reference data** (promotion trees, vanilla unit stats) is not included — the chatbot covers BBG balance changes only. For base game lookups, refer to the [Civilization Wiki](https://civilization.fandom.com/wiki/Civilization_VI).
- The Chroma database is local only. There is no hosted version of this chatbot.
