from pathlib import Path

from workflows.book_writer.adapter import BookWriterAdapter
from workflows.book_writer.real_adapter import BookWriterRealAdapter
from workflows.fact_checker.adapter import FactCheckerAdapter
from workflows.fact_checker.real_adapter import FactCheckerRealAdapter
from workflows.social_content.adapter import SocialContentAdapter
from workflows.social_content.real_adapter import SocialContentRealAdapter


def test_social_content_adapter_returns_content(monkeypatch):
    def fake_run(self, blog_post_url, post_type, draft_path, example_threads, example_linkedin):
        return {
            "title": "Generated social post",
            "content": "A rich social post",
            "platform": post_type,
        }

    monkeypatch.setattr(SocialContentAdapter, "run", fake_run)
    adapter = SocialContentAdapter(service=None)
    result = adapter.run("https://example.com", "twitter", "assets/demo.md", "assets/threads.txt", "assets/linkedin.txt")
    assert result["platform"] == "twitter"
    assert "content" in result


def test_social_content_real_adapter_uses_thread_prompt(monkeypatch):
    captured = {}

    def fake_call_ollama(self, prompt):
        captured["prompt"] = prompt
        return "Tweet 1: Hook"

    monkeypatch.setattr(SocialContentRealAdapter, "_call_ollama", fake_call_ollama)
    adapter = SocialContentRealAdapter()
    adapter.firecrawl_api_key = None

    result = adapter.run("https://example.com", "twitter", "assets/demo.md", "assets/threads.txt", "assets/linkedin.txt")

    assert "create a Twitter thread" in captured["prompt"]
    assert "Tweet 1" in captured["prompt"]
    assert result["workflow_steps"][0]["task"] == "analyze_draft"
    assert "Rédacteur_contenu" in result["source_config"]["agents_path"]


def test_book_writer_real_adapter_uses_research_and_outline(monkeypatch):
    prompts = []

    def fake_call_ollama(self, prompt):
        prompts.append(prompt)
        return "outline"

    monkeypatch.setattr(BookWriterRealAdapter, "_call_ollama", fake_call_ollama)
    adapter = BookWriterRealAdapter()

    result = adapter.run("AI", 3, "ollama/llama3.2:3b")

    assert len(prompts) == 2
    assert "Research the topic" in prompts[0]
    assert "Write a outline" in prompts[1] or "Write an outline" in prompts[1]
    assert result["workflow_steps"][0]["task"] == "research_task"
    assert "book_writing_flow" in result["source_config"]["agents_path"]


def test_fact_checker_real_adapter_uses_three_stage_flow(monkeypatch):
    prompts = []

    def fake_call_ollama(self, prompt):
        prompts.append(prompt)
        return "verified"

    monkeypatch.setattr(FactCheckerRealAdapter, "_call_ollama", fake_call_ollama)
    adapter = FactCheckerRealAdapter()

    result = adapter.run("What is AI?", "AI", "Some text")

    assert len(prompts) == 3
    assert result["workflow_steps"][0]["task"] == "research_task"
    assert result["workflow_steps"][2]["task"] == "fact_checking_task"
    assert "Agentic_system101" in result["source_config"]["agents_path"]


def test_book_writer_adapter_returns_payload():
    adapter = BookWriterAdapter(service=None)
    result = adapter.run("AI", 2, "ollama/llama3.2:3b")
    assert result.payload["topic"] == "AI"
    assert result.payload["total_chapters"] == 2


def test_fact_checker_adapter_returns_payload():
    adapter = FactCheckerAdapter(service=None)
    result = adapter.run("What is AI?", "AI", "Some text")
    assert result.payload["topic"] == "AI"
    assert result.payload["question"] == "What is AI?"
