"""Structured orthopedic report generation."""

from __future__ import annotations

from orthovision_ai.utils.types import FractureFinding, MeasurementResult


class ReportGenerator:
    def generate(
        self,
        study_uid: str,
        fractures: list[FractureFinding],
        measurements: MeasurementResult,
        implants: dict[str, str],
    ) -> str:
        findings = "No acute fracture detected" if not fractures else "; ".join(
            f"{f.location} (disp {f.displacement_mm:.1f}mm, ang {f.angulation_deg:.1f}°)" for f in fractures
        )
        m = ", ".join(f"{k}={v:.2f}" for k, v in measurements.values.items())
        i = ", ".join(f"{k}:{v}" for k, v in implants.items())
        return f"Study {study_uid}\nFracture analysis: {findings}\nMeasurements: {m}\nImplant suggestions: {i}"
