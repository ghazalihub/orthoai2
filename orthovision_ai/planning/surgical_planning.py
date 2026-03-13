"""Surgical planning: reduction, implant fitting, and screw trajectory planning."""

from __future__ import annotations

from orthovision_ai.utils.types import PlanningResult


class SurgicalPlanningEngine:
    def plan(self, measurements: dict[str, float], fracture_count: int, risk_score: float) -> PlanningResult:
        plate_length = "12-hole" if fracture_count >= 2 else "10-hole" if fracture_count == 1 else "6-hole"
        screw_length = f"{int(30 + measurements.get('knee_joint_space_width_medial_mm', 3) * 3)}mm"
        warnings: list[str] = []
        if risk_score > 0.7:
            warnings.append("High fracture complexity: confirm plan with 3D CT review")

        reduction_steps = [
            "1) Align major fragments along mechanical axis",
            "2) Correct rotational mismatch using condylar reference",
            "3) Provisionally fix with K-wires before definitive implant",
        ]
        return PlanningResult(
            recommended_implants={
                "plate": plate_length,
                "screw": screw_length,
                "hip_stem": "size-4" if measurements.get("hip_neck_shaft_angle_deg", 130) < 132 else "size-5",
            },
            screw_trajectories=[
                {"entry": [10, 12, 2], "target": [15, 18, 30], "safe": True, "corridor_mm": 4.2},
                {"entry": [13, 10, 4], "target": [19, 16, 28], "safe": risk_score < 0.9, "corridor_mm": 3.6},
            ],
            reduction_steps=reduction_steps,
            warnings=warnings,
        )
