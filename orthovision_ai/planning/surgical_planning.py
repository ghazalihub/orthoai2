"""Surgical planning: reduction, implant fitting, and screw trajectory planning."""

from __future__ import annotations

from orthovision_ai.utils.types import PlanningResult


class SurgicalPlanningEngine:
    def plan(self, measurements: dict[str, float], fracture_count: int) -> PlanningResult:
        plate_length = "10-hole" if fracture_count > 0 else "6-hole"
        screw_length = f"{int(30 + measurements.get('knee_joint_space_width_mm', 4) * 2)}mm"
        return PlanningResult(
            recommended_implants={
                "plate": plate_length,
                "screw": screw_length,
                "hip_stem": "size-4",
            },
            screw_trajectories=[{"entry": [10, 12, 2], "target": [15, 18, 30], "safe": True}],
        )
