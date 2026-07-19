# ============================================================================
# tracking/botsort/config.py
# ============================================================================

from __future__ import annotations
from argparse import Namespace

from src.core.config import Config

def build_botsort_args(config: Config) -> Namespace:
    """
    Convert project configuration into the Namespace expected by
    Ultralytics BoTSORT.
    """

    cfg = config["tracking"]["botsort"]

    return Namespace(
        track_high_thresh=cfg["track_high_thresh"],
        track_low_thresh=cfg["track_low_thresh"],
        new_track_thresh=cfg["new_track_thresh"],
        match_thresh=cfg["match_thresh"],
        track_buffer=cfg["track_buffer"],
        fuse_score=cfg["fuse_score"],
        proximity_thresh=cfg["proximity_thresh"],
        appearance_thresh=cfg["appearance_thresh"],
        with_reid=cfg["with_reid"],
        gmc_method=cfg["gmc_method"],
        model=cfg["model"],
    )