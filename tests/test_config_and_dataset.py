from pathlib import Path

from orthovision_ai.dataset_builder.manager import DatasetBuilder
from orthovision_ai.utils.io import load_config


def test_load_config() -> None:
    config = load_config("orthovision_ai/config/defaults.json")
    assert config.runtime.max_ct_processing_seconds == 60
    assert config.models.segmentation_backend == "mock"


def test_dataset_manifest_export(tmp_path: Path) -> None:
    builder = DatasetBuilder()
    builder.add_record("abc", "img1.dcm", {"fracture": "yes"})
    out = builder.export_manifest(tmp_path / "manifest.csv")
    assert out.exists()
    assert "abc,img1.dcm" in out.read_text()
