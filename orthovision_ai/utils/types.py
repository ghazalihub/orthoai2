"""Shared data contracts across modules."""

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


@dataclass(slots=True)
class ImagingStudy:
    source_path: Path
    metadata: StudyMetadata
    volume: Any
    spacing: tuple[float, float, float] = (1.0, 1.0, 1.0)


@dataclass(slots=True)
class SegmentationOutput:
    mask: Any
    labels: dict[int, str]


@dataclass(slots=True)
class FractureFinding:
    location: str
    confidence: float
    displacement_mm: float
    angulation_deg: float
    comminution_score: float


@dataclass(slots=True)
class MeasurementResult:
    values: dict[str, float] = field(default_factory=dict)


@dataclass(slots=True)
class PlanningResult:
    recommended_implants: dict[str, str]
    screw_trajectories: list[dict[str, Any]]


@dataclass(slots=True)
class PipelineResult:
    study_uid: str
    fracture_findings: list[FractureFinding]
    measurements: MeasurementResult
    planning: PlanningResult
    report_text: str
