"""Longitudinal fracture healing analytics with trend estimation."""

from __future__ import annotations

from orthovision_ai.utils.types import HealingPoint, HealingSeriesResult


class HealingTracker:
    def score_series(self, timepoints: list[str]) -> HealingSeriesResult:
        points: list[HealingPoint] = []
        indices: list[float] = []
        for idx, tp in enumerate(timepoints):
            callus = min(1.0, 0.15 + idx * 0.18)
            gap = min(8.0, idx * 1.25)
            cortical = min(1.0, 0.1 + idx * 0.22)
            healing_index = 0.4 * callus + 0.3 * cortical + 0.3 * min(1.0, gap / 6.0)
            indices.append(healing_index)
            points.append(
                HealingPoint(
                    timepoint=tp,
                    callus_score=callus,
                    gap_closure_mm=gap,
                    cortical_bridging_score=cortical,
                    healing_index=healing_index,
                )
            )

        trend_slope = (indices[-1] - indices[0]) / max(1, len(indices) - 1) if indices else 0.0
        plateau_detected = len(indices) >= 3 and max(indices[-3:]) - min(indices[-3:]) < 0.05
        return HealingSeriesResult(points=points, trend_slope=trend_slope, plateau_detected=plateau_detected)
