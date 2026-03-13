"""FastAPI service surface for clinical/research integration."""

from __future__ import annotations

from fastapi import FastAPI

from orthovision_ai.pipeline.orchestrator import OrthoVisionPipeline

app = FastAPI(title="ORTHOVISION AI")
pipeline = OrthoVisionPipeline()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/analyze")
def analyze(study_path: str, modality: str = "CT") -> dict[str, str]:
    result = pipeline.run(study_path=study_path, modality=modality)
    return {"study_uid": result.study_uid, "report": result.report_text}
