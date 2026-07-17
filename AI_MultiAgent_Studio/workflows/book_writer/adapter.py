from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from services.workflow_service import WorkflowService


@dataclass
class BookWriterResult:
    topic: str
    total_chapters: int
    llm_model: str
    payload: dict[str, Any]


class BookWriterAdapter:
    def __init__(self, service: WorkflowService | None = None) -> None:
        self.service = service or WorkflowService()

    def run(self, topic: str, total_chapters: int, llm_model: str) -> BookWriterResult:
        payload = {"topic": topic, "total_chapters": total_chapters, "llm_model": llm_model}
        self.service.save_json(payload, "book_writer_payload.json")
        return BookWriterResult(topic=topic, total_chapters=total_chapters, llm_model=llm_model, payload=payload)
