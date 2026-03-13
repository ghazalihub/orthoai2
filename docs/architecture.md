# ORTHOVISION AI Architecture

## Design principles
- **Modular**: each clinical function is a replaceable engine.
- **Scalable**: orchestration layer supports swapping mock logic with production MONAI/nnUNet/Torch models.
- **Research + clinical**: reproducible pipelines and API surfaces.

## Module map
- `modules/dicom_engine.py`: ingestion, anonymization, intensity normalization
- `modules/preprocessing.py`: z-score normalization and denoising
- `modules/segmentation.py`: CT/X-ray segmentation entrypoint
- `modules/fracture_analysis.py`: fracture geometry scoring and displacement/angulation estimation
- `modules/measurements.py`: hip, knee, spine, and foot metrics
- `modules/reconstruction3d.py`: STL export placeholder, easily replaced with VTK marching cubes
- `planning/surgical_planning.py`: reduction and screw trajectory output contracts
- `modules/implant_recommendation.py`: implant prediction baseline
- `modules/healing_tracker.py`: multi-timepoint healing scoring
- `reporting/report_generator.py`: structured report strings (adaptable to PDF/SR)
- `dataset_builder/manager.py`: import/index/export manifest workflows
- `integration/slicer_bridge.py`: 3D Slicer command construction

## Extension strategy
1. Replace segmentation `infer()` with nnUNet/MONAI inferers.
2. Add landmark detector for robust angle/axis extraction.
3. Integrate graph-based fragment analysis in fracture module.
4. Export report payload to DICOM SR via highdicom/pydicom.
5. Add asynchronous GPU workers and job queue for batch processing.
