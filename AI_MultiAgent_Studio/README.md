# AI Multi-Agent Studio

AI Multi-Agent Studio is a production-ready Streamlit application that brings together three CrewAI-based workflows:

- Social Content Planner
- AI Book Writer
- Research & Fact Checker

## Features

- Modern multipage Streamlit UI
- Sidebar navigation and dark theme
- Structured service layer for orchestration and persistence
- Logging, exception handling, and Pydantic-based state models
- Docker and Docker Compose support

## Installation

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## Run locally

```bash
streamlit run app.py
```

## Docker

```bash
docker compose up --build
```
