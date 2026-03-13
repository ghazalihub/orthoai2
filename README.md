# ORTHOVISION AI

Advanced Orthopedic Imaging Analysis Platform for X-ray and CT based decision support.

## Key capabilities
- DICOM ingestion and metadata normalization/anonymization
- Automated segmentation, fracture analysis, and orthopedic measurements
- 3D reconstruction pipeline with STL export and 3D Slicer bridge
- Surgical planning and implant recommendation baseline engines
- Longitudinal fracture healing tracker and structured report generation
- Dataset builder for model development workflows

## Architecture
The package is modular and centered around `OrthoVisionPipeline`, which orchestrates:
1. DICOM processing
2. Preprocessing
3. Segmentation
4. Fracture analysis
5. Measurement extraction
6. 3D reconstruction
7. Surgical planning
8. Implant recommendation
9. Reporting and visualization manifest generation

See `docs/architecture.md` for full module design and extension points.

## Quickstart
```bash
python -m pip install -e .
python -m orthovision_ai.cli.main ./sample_study --modality CT --output-dir artifacts
```

## Development
```bash
pytest
```
