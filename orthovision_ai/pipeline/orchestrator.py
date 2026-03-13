"""End-to-end orchestration for ORTHOVISION AI modules."""

from __future__ import annotations

from pathlib import Path
from time import perf_counter

from orthovision_ai.config.settings import AppConfig, DEFAULT_CONFIG
from orthovision_ai.modules.dicom_engine import DicomProcessingEngine
from orthovision_ai.modules.fracture_analysis import FractureAnalysisEngine
from orthovision_ai.modules.healing_tracker import HealingTracker
from orthovision_ai.modules.implant_recommendation import ImplantRecommendationEngine
from orthovision_ai.modules.measurements import OrthopedicMeasurementEngine
from orthovision_ai.modules.preprocessing import PreprocessingPipeline
from orthovision_ai.modules.reconstruction3d import ReconstructionEngine
from orthovision_ai.modules.segmentation import SegmentationEngine
from orthovision_ai.planning.surgical_planning import SurgicalPlanningEngine
from orthovision_ai.reporting.report_generator import ReportGenerator
from orthovision_ai.utils.types import PipelineResult, RuntimeMetrics
from orthovision_ai.visualization.viewer import VisualizationInterface


class OrthoVisionPipeline:
    def __init__(self, config: AppConfig = DEFAULT_CONFIG) -> None:
        self.config = config
        self.dicom_engine = DicomProcessingEngine(anonymize=config.dicom.anonymize)
        self.preprocessor = PreprocessingPipeline()
        self.segmentation = SegmentationEngine()
        self.fracture = FractureAnalysisEngine()
        self.measurements = OrthopedicMeasurementEngine()
        self.reconstruction = ReconstructionEngine()
        self.planner = SurgicalPlanningEngine()
        self.implants = ImplantRecommendationEngine()
        self.reports = ReportGenerator()
        self.healing = HealingTracker()
        self.viewer = VisualizationInterface()

    def run(
        self,
        study_path: str | Path,
        modality: str = "CT",
        output_dir: str | Path = "artifacts",
        healing_timepoints: list[str] | None = None,
    ) -> PipelineResult:
        start = perf_counter()
        stage_seconds: dict[str, float] = {}

        t0 = perf_counter()
        study = self.dicom_engine.load_study(study_path, modality=modality)
        normalized = self.dicom_engine.normalize_intensity(study.volume, modality=modality)
        stage_seconds["ingestion"] = perf_counter() - t0

        t0 = perf_counter()
        image = self.preprocessor.run(normalized)
        stage_seconds["preprocessing"] = perf_counter() - t0

        t0 = perf_counter()
        segmentation = self.segmentation.infer(image, modality=modality)
        fracture_analysis = self.fracture.analyze(image, segmentation.mask)
        stage_seconds["analysis"] = perf_counter() - t0

        t0 = perf_counter()
        measurement_result = self.measurements.compute(image, modality=modality)
        stage_seconds["measurements"] = perf_counter() - t0

        t0 = perf_counter()
        stl_path = self.reconstruction.generate_mesh(segmentation.mask, output_dir=Path(output_dir) / "meshes")
        planning = self.planner.plan(
            measurement_result.values,
            fracture_count=len(fracture_analysis.findings),
            risk_score=fracture_analysis.global_risk_score,
        )
        implant_suggestions = self.implants.recommend(measurement_result.values)
        stage_seconds["planning_and_recon"] = perf_counter() - t0

        t0 = perf_counter()
        healing = self.healing.score_series(healing_timepoints or ["t0", "t6w", "t12w"])
        report = self.reports.generate(
            study.metadata.study_uid,
            fracture_analysis,
            measurement_result,
            implant_suggestions,
            planning,
        )
        _overlay_manifest = self.viewer.build_overlay_manifest(stl_path, report)
        stage_seconds["reporting"] = perf_counter() - t0

        runtime = RuntimeMetrics(elapsed_seconds=perf_counter() - start, stage_seconds=stage_seconds)
        return PipelineResult(
            study_uid=study.metadata.study_uid,
            fracture_analysis=fracture_analysis,
            measurements=measurement_result,
            planning=planning,
            healing=healing,
            report_text=report,
            runtime=runtime,
        )
