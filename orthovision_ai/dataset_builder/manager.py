"""Dataset import, anonymization hooks, and export manifest generation."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class DatasetRecord:
    study_uid: str
    image_path: str
    labels: dict[str, str] = field(default_factory=dict)


class DatasetBuilder:
    def __init__(self) -> None:
        self.records: list[DatasetRecord] = []

    def add_record(self, study_uid: str, image_path: str, labels: dict[str, str] | None = None) -> None:
        self.records.append(DatasetRecord(study_uid=study_uid, image_path=image_path, labels=labels or {}))

    def export_manifest(self, output_path: str | Path) -> Path:
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        lines = ["study_uid,image_path,labels"]
        for r in self.records:
            lines.append(f"{r.study_uid},{r.image_path},{r.labels}")
        out.write_text("\n".join(lines) + "\n")
        return out
