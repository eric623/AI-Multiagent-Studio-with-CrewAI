from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from utils.logging_config import get_logger

logger = get_logger(__name__)


class WorkflowService:
    """Thin service layer for orchestration and persistence."""

    def __init__(self, base_dir: str | None = None) -> None:
        self.base_dir = Path(base_dir or Path(__file__).resolve().parent.parent)
        self.output_dir = self.base_dir / "output"
        self.output_dir.mkdir(exist_ok=True)

    def save_json(self, payload: dict[str, Any], filename: str) -> Path:
        path = self.output_dir / filename
        with path.open("w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2, ensure_ascii=False)
        logger.info("Saved JSON output to %s", path)
        return path

    def save_markdown(self, content: str, filename: str) -> Path:
        path = self.output_dir / filename
        with path.open("w", encoding="utf-8") as fh:
            fh.write(content)
        logger.info("Saved markdown output to %s", path)
        return path
