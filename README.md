# ORTHOVISION AI

Advanced Orthopedic Imaging Analysis Platform for X-ray and CT decision support.

## What is new in this advanced version
- Multi-stage orchestration with **runtime telemetry** per stage.
- Rich fracture analytics outputs (risk score, continuity index, fragment geometry, rotation).
- Expanded orthopedic measurements (hip, knee, spine, foot) with measurement-level confidence and synthetic landmark maps.
- Longitudinal healing tracker producing trend slope and plateau detection.
- Surgical planning protocol generation with warnings for high-complexity injuries.
- Structured report text that includes geometry, risk, measurements, planning protocol, and warnings.

## Platform Modules
- DICOM ingestion and normalization (`modules/dicom_engine.py`)
- Adaptive segmentation fallback (`modules/segmentation.py`)
- Fracture geometry analytics (`modules/fracture_analysis.py`)
- Orthopedic measurements + landmarks (`modules/measurements.py`)
- 3D mesh generation placeholder (`modules/reconstruction3d.py`)
- Surgical planning (`planning/surgical_planning.py`)
- Implant recommendation (`modules/implant_recommendation.py`)
- Healing tracker (`modules/healing_tracker.py`)
- Report generation (`reporting/report_generator.py`)
- Orchestration (`pipeline/orchestrator.py`)

## Quickstart
```bash
python -m pip install -e .
python -m orthovision_ai.cli.main ./sample_study --modality CT --output-dir artifacts
```

## Validation
```bash
pytest -q
```
