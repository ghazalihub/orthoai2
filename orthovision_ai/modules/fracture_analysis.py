"""Fracture detection and geometric characterization."""

from __future__ import annotations

from orthovision_ai.utils.types import FractureAnalysisResult, FractureFinding


class FractureAnalysisEngine:
    def analyze(self, image: list[float], mask: list[int]) -> FractureAnalysisResult:
        masked = [abs(v) for v, m in zip(image, mask) if m > 0]
        if not masked:
            return FractureAnalysisResult(findings=[], global_risk_score=0.0, continuity_index=1.0)

        mean_signal = sum(masked) / len(masked)
        high_grad = sum(1 for i in range(1, len(masked)) if abs(masked[i] - masked[i - 1]) > mean_signal * 0.75)
        discontinuity_rate = high_grad / max(1, len(masked) - 1)
        continuity_index = max(0.0, 1.0 - discontinuity_rate)

        findings = self._extract_findings(mean_signal, discontinuity_rate)
        global_risk = min(1.0, 0.45 * (mean_signal / 2.0) + 0.55 * discontinuity_rate)
        trace = {
            "mean_roi_signal": mean_signal,
            "discontinuity_rate": discontinuity_rate,
            "high_gradient_count": float(high_grad),
        }
        return FractureAnalysisResult(
            findings=findings,
            global_risk_score=global_risk,
            continuity_index=continuity_index,
            algorithmic_trace=trace,
        )

    @staticmethod
    def _extract_findings(mean_signal: float, discontinuity_rate: float) -> list[FractureFinding]:
        if mean_signal < 0.65 and discontinuity_rate < 0.12:
            return []

        base_conf = min(0.99, 0.35 + mean_signal * 0.25 + discontinuity_rate * 0.5)
        primary = FractureFinding(
            location="distal_femur",
            confidence=base_conf,
            displacement_mm=2.0 + mean_signal * 2.1,
            angulation_deg=4.0 + discontinuity_rate * 55,
            comminution_score=min(1.0, 0.15 + discontinuity_rate * 1.1),
            fragment_count=2 if discontinuity_rate < 0.2 else 3,
            fragment_distance_mm=1.2 + discontinuity_rate * 6.0,
            rotation_deg=2.0 + discontinuity_rate * 12.0,
        )
        findings = [primary]
        if discontinuity_rate > 0.28:
            findings.append(
                FractureFinding(
                    location="metaphyseal_extension",
                    confidence=min(0.93, base_conf - 0.08),
                    displacement_mm=1.0 + mean_signal,
                    angulation_deg=3.0 + discontinuity_rate * 35,
                    comminution_score=min(1.0, 0.25 + discontinuity_rate),
                    fragment_count=2,
                    fragment_distance_mm=0.8 + discontinuity_rate * 4.0,
                    rotation_deg=1.5 + discontinuity_rate * 9.0,
                )
            )
        return findings
