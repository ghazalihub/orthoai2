"""Implant size prediction using measurements and fracture features."""

from __future__ import annotations


class ImplantRecommendationEngine:
    def recommend(self, measurements: dict[str, float]) -> dict[str, str]:
        femoral_angle = measurements.get("hip_neck_shaft_angle_deg", 130)
        return {
            "hip_prosthesis": "size-5" if femoral_angle > 130 else "size-4",
            "intramedullary_nail_length": "340mm" if femoral_angle > 125 else "320mm",
            "locking_plate": "LCP-distal-femur-9-hole",
        }
