"""Visualization adapters for 2D/3D rendering targets."""

from __future__ import annotations

from pathlib import Path


class VisualizationInterface:
    def build_overlay_manifest(self, stl_path: Path, report_text: str) -> dict[str, str]:
        return {
            "mesh": str(stl_path),
            "report_preview": report_text[:240],
            "viewer": "3D Slicer / WebGL compatible",
        }
