"""I/O helpers for configuration and artifact persistence."""

import json
from pathlib import Path

from orthovision_ai.config.settings import AppConfig, DicomConfig, ModelConfig, RuntimeConfig


def load_config(path: str | Path) -> AppConfig:
    payload = json.loads(Path(path).read_text())
    return AppConfig(
        runtime=RuntimeConfig(**payload.get("runtime", {})),
        dicom=DicomConfig(**payload.get("dicom", {})),
        models=ModelConfig(**payload.get("models", {})),
    )


def ensure_dir(path: str | Path) -> Path:
    out = Path(path)
    out.mkdir(parents=True, exist_ok=True)
    return out
