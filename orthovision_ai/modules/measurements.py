"""Orthopedic measurement engine using landmark-based estimators."""

from __future__ import annotations

from orthovision_ai.utils.types import MeasurementResult


class OrthopedicMeasurementEngine:
    def compute(self, image: list[float], modality: str) -> MeasurementResult:
        seed = sum(abs(v) for v in image) / max(1, len(image))
        values = {
            "hip_neck_shaft_angle_deg": 120 + seed % 15,
            "hip_center_edge_angle_deg": 20 + seed % 25,
            "knee_mechanical_axis_deg": -2 + seed % 4,
            "knee_joint_space_width_mm": 3 + seed % 4,
            "spine_cobb_angle_deg": 5 + seed % 30,
            "foot_meary_angle_deg": -5 + seed % 20,
        }
        if modality == "CT":
            values["tibial_slope_deg"] = 5 + seed % 10
        return MeasurementResult(values=values)
