"""3D reconstruction from segmentation masks."""

from __future__ import annotations

from pathlib import Path

from orthovision_ai.utils.io import ensure_dir


class ReconstructionEngine:
    def generate_mesh(self, mask: list[int], output_dir: str | Path) -> Path:
        _ = mask
        out_dir = ensure_dir(output_dir)
        stl_path = out_dir / "bone_model.stl"
        stl_path.write_text("solid bone\nendsolid bone\n")
        return stl_path
