from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from services.workflow_service import WorkflowService


@dataclass
class FactCheckerResult:
    question: str
    topic: str
    text: str
    payload: dict[str, Any]


class FactCheckerAdapter:
    def __init__(self, service: WorkflowService | None = None) -> None:
        self.service = service or WorkflowService()

    def run(self, question: str, topic: str, text: str) -> FactCheckerResult:
        payload = {"question": question, "topic": topic, "text": text}
        self.service.save_json(payload, "fact_checker_payload.json")
        return FactCheckerResult(question=question, topic=topic, text=text, payload=payload)
