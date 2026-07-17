from __future__ import annotations

import json
import os
import re
import urllib.request
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / ".env")


class SocialContentRealAdapter:
    """Real adapter for the existing social content planning flow using Ollama."""

    def __init__(self) -> None:
        self.firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")
        self.ollama_model = os.getenv("DEFAULT_LLM_MODEL", "ollama/llama3.2:1b")
        self.ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    def run(self, blog_post_url: str, post_type: str, draft_path: str, example_threads: str, example_linkedin: str) -> dict[str, Any]:
        tools_used = ["ollama.generate"]
        markdown = ""
        if self.firecrawl_api_key:
            from firecrawl import Firecrawl

            app = Firecrawl(api_key=self.firecrawl_api_key)
            result = app.scrape(blog_post_url, formats=["markdown", "html"])
            markdown = getattr(result, "markdown", "") or ""
            tools_used.append("firecrawl.scrape")
        else:
            markdown = self._fetch_page_excerpt(blog_post_url)
        draft_path_obj = Path(draft_path)
        draft_path_obj.parent.mkdir(parents=True, exist_ok=True)
        draft_path_obj.write_text(markdown or "No content scraped", encoding="utf-8")

        project_root = Path(__file__).resolve().parents[3]
        original_config_dir = project_root / "Rédacteur_contenu" / "config"
        if not original_config_dir.exists():
            original_config_dir = Path(__file__).resolve().parent / "agentic"
        with (original_config_dir / "planner_agents.yaml").open("r", encoding="utf-8") as fh:
            agents_config = yaml.safe_load(fh)
        with (original_config_dir / "planner_tasks.yaml").open("r", encoding="utf-8") as fh:
            tasks_config = yaml.safe_load(fh)

        if post_type.lower() == "twitter":
            analysis_prompt = (
                f"Analyze the following draft and produce a technical summary for a Twitter thread.\n\nDraft:\n{markdown[:4000]}"
            )
            analysis = self._call_ollama(analysis_prompt)
            plan_prompt = (
                f"Using the following analysis, create a Twitter thread with 4 tweets. "
                f"Format each tweet as 'Tweet 1:', 'Tweet 2:', 'Tweet 3:', and 'Tweet 4:'. "
                f"Do not use the '1/5' style. The first tweet should be a strong hook, the rest should build the story, and the final tweet should include a call to action.\n\nAnalysis:\n{analysis}"
            )
            generated_content = self._call_ollama(plan_prompt)
            workflow_steps = [
                {"task": "analyze_draft", "agent": "draft_analyzer", "output": analysis},
                {"task": "create_twitter_thread_plan", "agent": "twitter_thread_planner", "output": generated_content},
            ]
        else:
            analysis_prompt = (
                f"Analyze the following draft and produce a professional summary for a LinkedIn post.\n\nDraft:\n{markdown[:4000]}"
            )
            analysis = self._call_ollama(analysis_prompt)
            plan_prompt = (
                f"Using the following analysis, create a polished LinkedIn post with an engaging opening and a clear call to action.\n\nAnalysis:\n{analysis}"
            )
            generated_content = self._call_ollama(plan_prompt)
            workflow_steps = [
                {"task": "analyze_draft", "agent": "draft_analyzer", "output": analysis},
                {"task": "create_linkedin_post_plan", "agent": "linkedin_post_planner", "output": generated_content},
            ]

        return {
            "blog_post_url": blog_post_url,
            "post_type": post_type,
            "draft_path": draft_path,
            "markdown_excerpt": markdown[:800],
            "generated_content": generated_content,
            "workflow_steps": workflow_steps,
            "fallback_used": not bool(self.firecrawl_api_key),
            "source": "ollama" if not self.firecrawl_api_key else "firecrawl+ollama",
            "tools_used": tools_used,
            "tool_status": {
                "firecrawl": bool(self.firecrawl_api_key),
                "ollama": True,
            },
            "llm": {
                "provider": "ollama",
                "model": self.ollama_model,
                "base_url": self.ollama_base_url,
            },
            "agent_config": {
                "agents": agents_config,
                "tasks": tasks_config,
            },
            "source_config": {
                "agents_path": str((original_config_dir / "planner_agents.yaml").resolve()),
                "tasks_path": str((original_config_dir / "planner_tasks.yaml").resolve()),
            },
        }

    def _fetch_page_excerpt(self, url: str) -> str:
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(request, timeout=30) as response:
                html = response.read().decode("utf-8", errors="ignore")
        except Exception:
            return f"Blog URL: {url}\nTopic: {url.split('/')[-1]} content planning"

        title_match = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
        title = re.sub(r"<[^>]+>", "", title_match.group(1)).strip() if title_match else ""
        description_match = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)["\']', html, re.IGNORECASE)
        description = description_match.group(1).strip() if description_match else ""
        cleaned = re.sub(r"\s+", " ", f"{title}\n{description}".strip())
        return f"Blog URL: {url}\nTitle: {title}\nDescription: {description}\nExcerpt: {cleaned[:2000]}"

    def _call_ollama(self, prompt: str) -> str:
        model_name = self.ollama_model.replace("ollama/", "")
        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": False,
        }
        request = urllib.request.Request(
            f"{self.ollama_base_url.rstrip('/')}/api/generate",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(request, timeout=300) as response:
                data = json.loads(response.read().decode("utf-8"))
            return data.get("response", "")
        except Exception:
            return "Unable to generate content from Ollama at the moment."
