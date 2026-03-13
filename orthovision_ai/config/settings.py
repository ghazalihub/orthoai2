"""Global settings and typed configuration for ORTHOVISION AI."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal


@dataclass(slots=True)
class RuntimeConfig:
    device: Literal["cpu", "cuda"] = "cpu"
    batch_size: int = 1
    max_ct_processing_seconds: int = 60
    max_xray_processing_seconds: int = 5


@dataclass(slots=True)
class DicomConfig:
    anonymize: bool = True
    nifti_export_dir: Path = Path("artifacts/nifti")


@dataclass(slots=True)
class ModelConfig:
    segmentation_backend: Literal["monai", "nnunet", "mock"] = "mock"
    fracture_backend: Literal["torch", "mock"] = "mock"
    landmark_backend: Literal["torch", "mock"] = "mock"


@dataclass(slots=True)
class AppConfig:
    runtime: RuntimeConfig = field(default_factory=RuntimeConfig)
    dicom: DicomConfig = field(default_factory=DicomConfig)
    models: ModelConfig = field(default_factory=ModelConfig)


DEFAULT_CONFIG = AppConfig()
