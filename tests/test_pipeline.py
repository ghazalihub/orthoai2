from pathlib import Path

from orthovision_ai.pipeline.orchestrator import OrthoVisionPipeline


def test_pipeline_generates_report_mesh_and_runtime(tmp_path: Path) -> None:
    pipeline = OrthoVisionPipeline()
    result = pipeline.run(study_path=tmp_path / "study1", modality="CT", output_dir=tmp_path)
    assert result.study_uid.startswith("study-")
    assert "Fracture risk score" in result.report_text
    assert result.runtime.elapsed_seconds >= 0.0
    assert "analysis" in result.runtime.stage_seconds
    assert (tmp_path / "meshes" / "bone_model.stl").exists()


def test_pipeline_supports_xray_and_healing_series(tmp_path: Path) -> None:
    pipeline = OrthoVisionPipeline()
    result = pipeline.run(
        study_path=tmp_path / "xray1",
        modality="XRAY",
        output_dir=tmp_path,
        healing_timepoints=["baseline", "week2", "week6", "week12"],
    )
    assert "Measurements" in result.report_text
    assert result.healing is not None
    assert len(result.healing.points) == 4
    assert "hip_prosthesis" in result.report_text
