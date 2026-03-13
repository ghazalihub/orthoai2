"""3D Slicer integration command builder."""

from __future__ import annotations

from pathlib import Path


class SlicerBridge:
    def build_load_command(self, volume_path: str | Path, model_path: str | Path) -> str:
        return (
            "slicer --python-code \""
            f"loadVolume(r'{Path(volume_path)}');"
            f"loadModel(r'{Path(model_path)}');"
            "\""
        )
