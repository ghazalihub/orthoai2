"""Structured orthopedic report generation."""

from __future__ import annotations

from orthovision_ai.utils.types import FractureAnalysisResult, MeasurementResult, PlanningResult


class ReportGenerator:
    def generate(
        self,
        study_uid: str,
        fracture: FractureAnalysisResult,
        measurements: MeasurementResult,
        implants: dict[str, str],
        planning: PlanningResult,
    ) -> str:
        if not fracture.findings:
            fracture_lines = "No acute fracture detected"
        else:
            fracture_lines = "; ".join(
                (
                    f"{f.location}: disp {f.displacement_mm:.1f}mm, ang {f.angulation_deg:.1f}°, "
                    f"fragments {f.fragment_count}, rotation {f.rotation_deg:.1f}°"
                )
                for f in fracture.findings
            )

        m = ", ".join(f"{k}={v:.2f} (c={measurements.confidence.get(k, 0.0):.2f})" for k, v in measurements.values.items())
        i = ", ".join(f"{k}:{v}" for k, v in implants.items())
        p = " | ".join(planning.reduction_steps)
        w = "None" if not planning.warnings else "; ".join(planning.warnings)

        return (
            f"Study {study_uid}\n"
            f"Fracture analysis: {fracture_lines}\n"
            f"Fracture risk score: {fracture.global_risk_score:.2f}, continuity index: {fracture.continuity_index:.2f}\n"
            f"Measurements: {m}\n"
            f"Implant suggestions: {i}\n"
            f"Planning protocol: {p}\n"
            f"Planning warnings: {w}"
        )
