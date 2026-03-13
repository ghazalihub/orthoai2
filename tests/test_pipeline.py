from pathlib import Path

from orthovision_ai.pipeline.orchestrator import OrthoVisionPipeline


def test_pipeline_generates_report_and_mesh(tmp_path: Path) -> None:
    pipeline = OrthoVisionPipeline()
    result = pipeline.run(study_path=tmp_path / "study1", modality="CT", output_dir=tmp_path)
    assert result.study_uid.startswith("study-")
    assert "Fracture analysis" in result.report_text
    assert (tmp_path / "meshes" / "bone_model.stl").exists()


def test_pipeline_supports_xray(tmp_path: Path) -> None:
    pipeline = OrthoVisionPipeline()
    result = pipeline.run(study_path=tmp_path / "xray1", modality="XRAY", output_dir=tmp_path)
    assert "Measurements" in result.report_text
    assert "hip_prosthesis" in result.report_text
