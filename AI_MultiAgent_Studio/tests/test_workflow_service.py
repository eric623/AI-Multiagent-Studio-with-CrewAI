from pathlib import Path

from services.workflow_service import WorkflowService


def test_save_json_and_markdown(tmp_path: Path) -> None:
    service = WorkflowService(base_dir=str(tmp_path))
    payload = {"key": "value"}

    json_path = service.save_json(payload, "sample.json")
    md_path = service.save_markdown("# hello", "sample.md")

    assert json_path.exists()
    assert md_path.exists()
    assert json_path.parent == tmp_path / "output"
    assert md_path.parent == tmp_path / "output"
