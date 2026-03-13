"""DICOM ingestion, metadata parsing, normalization, and anonymization."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import random

from orthovision_ai.utils.types import ImagingStudy, StudyMetadata


class DicomProcessingEngine:
    """Baseline implementation; can be swapped with pydicom/SimpleITK full backends."""

    def __init__(self, anonymize: bool = True) -> None:
        self.anonymize = anonymize

    def load_study(self, path: str | Path, modality: str = "CT") -> ImagingStudy:
        source_path = Path(path)
        volume = self._mock_volume(modality)
        metadata = StudyMetadata(
            study_uid=f"study-{source_path.stem}",
            modality=modality,
            acquisition_time=datetime.utcnow(),
            body_part_examined="LOWER_EXTREMITY",
        )
        if self.anonymize:
            metadata.patient_age = None
        return ImagingStudy(source_path=source_path, metadata=metadata, volume=volume)

    @staticmethod
    def normalize_intensity(volume: list[float], modality: str) -> list[float]:
        if modality.upper() == "CT":
            return [max(0.0, min(1.0, (v + 1000.0) / 3000.0)) for v in volume]
        vmin, vmax = min(volume), max(volume)
        scale = (vmax - vmin) or 1.0
        return [(v - vmin) / scale for v in volume]

    @staticmethod
    def _mock_volume(modality: str) -> list[float]:
        size = 4096 if modality == "CT" else 2048
        return [random.uniform(-1000, 2000) for _ in range(size)]
