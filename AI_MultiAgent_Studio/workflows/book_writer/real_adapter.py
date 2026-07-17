from __future__ import annotations

import json
import os
import urllib.request
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / ".env")


class BookWriterRealAdapter:
    """Real adapter for the existing CrewAI book-writing flow using Ollama."""

    def run(self, topic: str, total_chapters: int, llm_model: str) -> dict[str, Any]:
        project_root = Path(__file__).resolve().parents[3]
        original_config_dir = project_root / "Rédacteur_contenu" / "book_flow" / "book_writing_flow" / "src" / "book_writing_flow" / "crews" / "Outline_crew" / "config"
        if not original_config_dir.exists():
            original_config_dir = project_root / "Rédacteur_contenu" / "book_flow" / "book_writing_flow" / "src" / "book_writing_flow" / "crews" / "Outline_crew" / "config"
        with (original_config_dir / "agents.yaml").open("r", encoding="utf-8") as fh:
            agents_config = yaml.safe_load(fh)
        with (original_config_dir / "tasks.yaml").open("r", encoding="utf-8") as fh:
            tasks_config = yaml.safe_load(fh)

        research_prompt = (
            f"Research the topic '{topic}' and gather the key ideas, themes, and structure that a book should cover."
        )
        research_findings = self._call_ollama(research_prompt)

        outline_prompt = (
            f"Write an outline for a book about '{topic}' with exactly {total_chapters} chapters. "
            f"Use the research findings below to make the outline relevant and structured.\n\nResearch:\n{research_findings}"
        )
        generated_outline = self._call_ollama(outline_prompt)
        return {
            "topic": topic,
            "total_chapters": total_chapters,
            "llm_model": llm_model,
            "book_path": str(Path("book.md").resolve()),
            "generated_outline": generated_outline,
            "research_findings": research_findings,
            "workflow_steps": [
                {"task": "research_task", "agent": "research_agent", "output": research_findings},
                {"task": "write_outline", "agent": "outline_writer", "output": generated_outline},
            ],
            "source": "book_flow+ollama",
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
                "model": llm_model or os.getenv("DEFAULT_LLM_MODEL", "ollama/llama3.2:3b"),
                "base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            },
        }

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
