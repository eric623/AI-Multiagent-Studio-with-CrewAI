from __future__ import annotations

import json
import os
import urllib.request
from pathlib import Path
from typing import Any

import requests
import yaml

from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / ".env")


class FactCheckerRealAdapter:
    """Real adapter for the existing fact-checking workflow using Ollama."""

    def run(self, question: str, topic: str, text: str) -> dict[str, Any]:
        from_part = "question" if question else "topic"
        tools_used = ["ollama.generate"]
        search_results = self._search_web(topic or question)
        if os.getenv("SERPER_API_KEY"):
            tools_used.append("serper.search")
        project_root = Path(__file__).resolve().parents[3]
        original_config_dir = project_root / "Partie1" / "Agentic_system101" / "config"
        if not original_config_dir.exists():
            original_config_dir = Path(__file__).resolve().parent / "agentic"
        with (original_config_dir / "agents.yaml").open("r", encoding="utf-8") as fh:
            agents_config = yaml.safe_load(fh)
        with (original_config_dir / "tasks.yaml").open("r", encoding="utf-8") as fh:
            tasks_config = yaml.safe_load(fh)

        research_prompt = (
            f"Research the topic '{topic}'. Question: {question}. "
            f"Use the following web research snippets as grounding: {search_results}. "
            f"Additional context: {text[:3000]}"
        )
        research_report = self._call_ollama(research_prompt)

        summary_prompt = (
            f"Summarize the following research findings into a concise report.\n\nResearch:\n{research_report}"
        )
        summary = self._call_ollama(summary_prompt)

        fact_check_prompt = (
            f"Verify the accuracy of the following summary and produce a final fact-checked report.\n\nSummary:\n{summary}"
        )
        report = self._call_ollama(fact_check_prompt)

        return {
            "question": question,
            "topic": topic,
            "text": text,
            "mode": from_part,
            "source": "agentic_system101+ollama+serper",
            "report": report,
            "search_results": search_results,
            "research_report": research_report,
            "summary": summary,
            "tools_used": tools_used,
            "tool_status": {
                "serper": bool(os.getenv("SERPER_API_KEY")),
                "ollama": True,
            },
            "workflow_steps": [
                {"task": "research_task", "agent": "research_agent", "output": research_report},
                {"task": "summarization_task", "agent": "summarization_agent", "output": summary},
                {"task": "fact_checking_task", "agent": "fact_checker_agent", "output": report},
            ],
            "agent_config": {
                "agents": agents_config,
                "tasks": tasks_config,
            },
            "source_config": {
                "agents_path": str((original_config_dir / "agents.yaml").resolve()),
                "tasks_path": str((original_config_dir / "tasks.yaml").resolve()),
            },
            "llm": {
                "provider": "ollama",
                "model": os.getenv("DEFAULT_LLM_MODEL", "ollama/llama3.2:3b"),
                "base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            },
        }

    def _search_web(self, query: str) -> str:
        api_key = os.getenv("SERPER_API_KEY")
        if not api_key:
            return "No Serper API key configured."

        try:
            response = requests.post(
                "https://google.serper.dev/search",
                headers={"X-API-KEY": api_key, "Content-Type": "application/json"},
                json={"q": query, "num": 5},
                timeout=30,
            )
            response.raise_for_status()
            payload = response.json()
            organic_results = payload.get("organic", [])[:3]
            snippets = []
            for item in organic_results:
                title = item.get("title", "")
                snippet = item.get("snippet", "")
                link = item.get("link", "")
                snippets.append(f"- {title}: {snippet} ({link})")
            return "\n".join(snippets) if snippets else "No web results found."
        except Exception:
            return "Serper search failed or returned no results."

    def _call_ollama(self, prompt: str) -> str:
        model = os.getenv("DEFAULT_LLM_MODEL", "ollama/llama3.2:1b").replace("ollama/", "")
        payload = {"model": model, "prompt": prompt, "stream": False}
        request = urllib.request.Request(
            f"{os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434').rstrip('/')}/api/generate",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(request, timeout=300) as response:
                data = json.loads(response.read().decode("utf-8"))
            return data.get("response", "")
        except Exception:
            return "Unable to generate content from Ollama at the moment."
