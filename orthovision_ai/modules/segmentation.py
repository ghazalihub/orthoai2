"""Segmentation engine supporting CT/X-ray bone masks and labels."""

from __future__ import annotations

from orthovision_ai.utils.types import SegmentationOutput


class SegmentationEngine:
    def infer(self, image: list[float], modality: str) -> SegmentationOutput:
        threshold = 0.35 if modality == "CT" else 0.5
        mask = [1 if value > threshold else 0 for value in image]
        labels = {1: "femur", 2: "tibia", 3: "fibula", 4: "pelvis"}
        return SegmentationOutput(mask=mask, labels=labels)
