"""Shared data contracts across ORTHOVISION AI modules.

The contracts are intentionally rich to support both research experiments and
future clinical-grade deployment pathways.
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class StudyMetadata:
    study_uid: str
    modality: str
    acquisition_time: datetime | None = None
    patient_age: str | None = None
    body_part_examined: str | None = None
    manufacturer: str | None = None
    pixel_spacing_mm: tuple[float, float] = (1.0, 1.0)


@dataclass(slots=True)
class ImagingStudy:
    source_path: Path
    metadata: StudyMetadata
    volume: list[float]
    spacing: tuple[float, float, float] = (1.0, 1.0, 1.0)


@dataclass(slots=True)
class SegmentationOutput:
    mask: list[int]
    labels: dict[int, str]
    confidence_map: list[float] = field(default_factory=list)
    quality_metrics: dict[str, float] = field(default_factory=dict)


@dataclass(slots=True)
class FractureFinding:
    location: str
    confidence: float
    displacement_mm: float
    angulation_deg: float
    comminution_score: float
    fragment_count: int = 1
    fragment_distance_mm: float = 0.0
    rotation_deg: float = 0.0


@dataclass(slots=True)
class FractureAnalysisResult:
    findings: list[FractureFinding]
    global_risk_score: float
    continuity_index: float
    algorithmic_trace: dict[str, float] = field(default_factory=dict)


@dataclass(slots=True)
class MeasurementResult:
    values: dict[str, float] = field(default_factory=dict)
    confidence: dict[str, float] = field(default_factory=dict)
    landmarks: dict[str, tuple[float, float]] = field(default_factory=dict)


@dataclass(slots=True)
class PlanningResult:
    recommended_implants: dict[str, str]
    screw_trajectories: list[dict[str, Any]]
    reduction_steps: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass(slots=True)
class HealingPoint:
    timepoint: str
    callus_score: float
    gap_closure_mm: float
    cortical_bridging_score: float
    healing_index: float


@dataclass(slots=True)
class HealingSeriesResult:
    points: list[HealingPoint]
    trend_slope: float
    plateau_detected: bool


@dataclass(slots=True)
class RuntimeMetrics:
    elapsed_seconds: float
    stage_seconds: dict[str, float] = field(default_factory=dict)


@dataclass(slots=True)
class PipelineResult:
    study_uid: str
    fracture_analysis: FractureAnalysisResult
    measurements: MeasurementResult
    planning: PlanningResult
    healing: HealingSeriesResult | None
    report_text: str
    runtime: RuntimeMetrics
