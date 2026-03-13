"""Fracture detection and geometric characterization."""

from __future__ import annotations

from orthovision_ai.utils.types import FractureFinding


class FractureAnalysisEngine:
    def analyze(self, image: list[float], mask: list[int]) -> list[FractureFinding]:
        masked = [abs(v) for v, m in zip(image, mask) if m > 0]
        if not masked:
            return []
        roi_score = sum(masked) / len(masked)
        if roi_score < 0.8:
            return []
        return [
            FractureFinding(
                location="distal_femur",
                confidence=min(0.99, roi_score / 3.0),
                displacement_mm=roi_score * 1.5,
                angulation_deg=roi_score * 2.1,
                comminution_score=min(1.0, roi_score / 5.0),
            )
        ]
