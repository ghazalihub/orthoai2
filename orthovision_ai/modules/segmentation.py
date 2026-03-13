"""Segmentation engine supporting CT/X-ray bone masks and labels.

Implements robust adaptive thresholding + post-processing style heuristics that
approximate a classical fallback when deep segmentation backends are unavailable.
"""

from __future__ import annotations

from orthovision_ai.utils.types import SegmentationOutput


class SegmentationEngine:
    def infer(self, image: list[float], modality: str) -> SegmentationOutput:
        threshold = self._adaptive_threshold(image, modality)
        raw_mask = [1 if value > threshold else 0 for value in image]
        mask = self._majority_smooth(raw_mask, window=5 if modality == "CT" else 3)
        confidence_map = self._confidence_map(image, threshold)
        quality_metrics = {
            "bone_voxel_ratio": sum(mask) / max(1, len(mask)),
            "threshold": threshold,
            "mean_confidence": sum(confidence_map) / max(1, len(confidence_map)),
        }
        labels = {1: "femur", 2: "tibia", 3: "fibula", 4: "pelvis"}
        return SegmentationOutput(mask=mask, labels=labels, confidence_map=confidence_map, quality_metrics=quality_metrics)

    @staticmethod
    def _adaptive_threshold(image: list[float], modality: str) -> float:
        sorted_vals = sorted(image)
        q70 = sorted_vals[int(0.7 * (len(sorted_vals) - 1))]
        q85 = sorted_vals[int(0.85 * (len(sorted_vals) - 1))]
        return (0.6 * q70 + 0.4 * q85) if modality == "CT" else (0.5 * q70 + 0.5 * q85)

    @staticmethod
    def _majority_smooth(mask: list[int], window: int) -> list[int]:
        half = max(1, window // 2)
        out: list[int] = []
        for idx in range(len(mask)):
            left = max(0, idx - half)
            right = min(len(mask), idx + half + 1)
            segment = mask[left:right]
            out.append(1 if sum(segment) >= (len(segment) / 2) else 0)
        return out

    @staticmethod
    def _confidence_map(image: list[float], threshold: float) -> list[float]:
        scale = max(abs(max(image, default=1.0)), abs(min(image, default=-1.0)), 1.0)
        return [min(1.0, abs(v - threshold) / scale) for v in image]
