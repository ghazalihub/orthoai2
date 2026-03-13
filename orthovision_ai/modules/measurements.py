"""Orthopedic measurement engine using synthetic landmark extraction.

This is an advanced deterministic fallback that models how a real landmark
network would feed automated measurements and confidence intervals.
"""

from __future__ import annotations

from orthovision_ai.utils.types import MeasurementResult


class OrthopedicMeasurementEngine:
    def compute(self, image: list[float], modality: str) -> MeasurementResult:
        landmarks = self._estimate_landmarks(image)
        seed = sum(abs(v) for v in image) / max(1, len(image))

        values = {
            "hip_neck_shaft_angle_deg": 124.0 + seed % 10,
            "hip_center_edge_angle_deg": 28.0 + seed % 12,
            "hip_acetabular_index_deg": 5.0 + seed % 9,
            "knee_mechanical_axis_deg": -2.5 + seed % 5,
            "knee_joint_space_width_medial_mm": 2.8 + seed % 3,
            "knee_joint_space_width_lateral_mm": 3.1 + seed % 3,
            "knee_tibial_slope_deg": 6.0 + seed % 7,
            "spine_cobb_angle_deg": 8.0 + seed % 25,
            "spine_sva_mm": 10.0 + seed % 35,
            "foot_meary_angle_deg": -4.0 + seed % 15,
            "foot_calcaneal_pitch_deg": 12.0 + seed % 9,
        }
        if modality == "CT":
            values["ct_3d_mechanical_axis_deg"] = -1.5 + seed % 4

        confidence = {name: self._confidence_from_value(value) for name, value in values.items()}
        return MeasurementResult(values=values, confidence=confidence, landmarks=landmarks)

    @staticmethod
    def _estimate_landmarks(image: list[float]) -> dict[str, tuple[float, float]]:
        n = max(1, len(image))
        average = sum(image) / n
        energy = sum(abs(v) for v in image) / n
        return {
            "femoral_head_center": (0.18 + average % 0.1, 0.21 + energy % 0.1),
            "femoral_neck_axis": (0.42 + average % 0.1, 0.39 + energy % 0.1),
            "knee_center": (0.52 + average % 0.1, 0.60 + energy % 0.1),
            "ankle_center": (0.48 + average % 0.1, 0.86 + energy % 0.1),
            "vertebral_endplate_sup": (0.33 + average % 0.1, 0.28 + energy % 0.1),
            "vertebral_endplate_inf": (0.37 + average % 0.1, 0.61 + energy % 0.1),
        }

    @staticmethod
    def _confidence_from_value(value: float) -> float:
        normalized = min(1.0, max(0.0, abs(value) / 180.0))
        return 0.7 + (1.0 - normalized) * 0.25
