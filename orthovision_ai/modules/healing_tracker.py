"""Longitudinal fracture healing analysis."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class HealingPoint:
    timepoint: str
    callus_score: float
    gap_closure_mm: float
    cortical_bridging_score: float


class HealingTracker:
    def score_series(self, timepoints: list[str]) -> list[HealingPoint]:
        points: list[HealingPoint] = []
        for idx, tp in enumerate(timepoints):
            points.append(
                HealingPoint(
                    timepoint=tp,
                    callus_score=min(1.0, 0.2 + idx * 0.2),
                    gap_closure_mm=min(6.0, idx * 1.1),
                    cortical_bridging_score=min(1.0, idx * 0.25),
                )
            )
        return points
