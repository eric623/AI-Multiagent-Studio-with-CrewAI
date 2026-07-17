from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from services.workflow_service import WorkflowService


@dataclass
class SocialContentResult:
    blog_post_url: str
    post_type: str
    draft_path: str
    payload: dict[str, Any]


class SocialContentAdapter:
    def __init__(self, service: WorkflowService | None = None) -> None:
        self.service = service or WorkflowService()

    def run(self, blog_post_url: str, post_type: str, draft_path: str, example_threads: str, example_linkedin: str) -> SocialContentResult:
        payload = {
            "blog_post_url": blog_post_url,
            "post_type": post_type,
            "draft_path": draft_path,
            "path_to_example_threads": example_threads,
            "path_to_example_linkedin": example_linkedin,
        }
        self.service.save_json(payload, "social_content_payload.json")
        return SocialContentResult(
            blog_post_url=blog_post_url,
            post_type=post_type,
            draft_path=draft_path,
            payload=payload,
        )
