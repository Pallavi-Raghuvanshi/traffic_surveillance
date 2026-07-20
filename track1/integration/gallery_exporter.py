from __future__ import annotations

from pathlib import Path

import cv2

from integration.reid_post_processor import GalleryRecord


class GalleryExporter:
    """
    Saves representative crops grouped by vehicle ID.
    """

    @staticmethod
    def export(
        records: list[GalleryRecord],
        output_directory: str | Path,
    ) -> None:

        output_directory = Path(output_directory)

        for record in records:

            vehicle_dir = (
                output_directory
                / f"vehicle_{record.result.vehicle_id:03d}"
            )

            vehicle_dir.mkdir(
                parents=True,
                exist_ok=True,
            )

            filename = (
                vehicle_dir
                / f"track_{record.result.track_id}.jpg"
            )

            cv2.imwrite(
                str(filename),
                record.crop,
            )