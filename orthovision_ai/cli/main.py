"""Command line interface for ORTHOVISION AI."""

from __future__ import annotations

import argparse

from orthovision_ai.pipeline.orchestrator import OrthoVisionPipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="ORTHOVISION AI pipeline runner")
    parser.add_argument("study_path", help="Path to DICOM study folder or file")
    parser.add_argument("--modality", default="CT", choices=["CT", "XRAY"], help="Imaging modality")
    parser.add_argument("--output-dir", default="artifacts", help="Output directory")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    pipeline = OrthoVisionPipeline()
    result = pipeline.run(args.study_path, modality=args.modality, output_dir=args.output_dir)
    print(result.report_text)


if __name__ == "__main__":
    main()
