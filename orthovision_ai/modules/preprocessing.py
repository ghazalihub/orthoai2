"""Image preprocessing pipeline."""

from __future__ import annotations

import statistics


class PreprocessingPipeline:
    def run(self, image: list[float]) -> list[float]:
        image = self._zscore(image)
        image = self._denoise(image)
        return image

    @staticmethod
    def _zscore(image: list[float]) -> list[float]:
        mean = statistics.fmean(image)
        stdev = statistics.pstdev(image) or 1e-6
        return [(v - mean) / stdev for v in image]

    @staticmethod
    def _denoise(image: list[float]) -> list[float]:
        return [max(-3.0, min(3.0, v)) for v in image]
