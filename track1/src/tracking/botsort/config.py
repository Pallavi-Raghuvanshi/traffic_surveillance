# ============================================================================
# tracking/botsort/config.py
# ============================================================================

from __future__ import annotations

from types import SimpleNamespace

from core.config import Config


def build_botsort_args(
    config: Config,
) -> SimpleNamespace:
    """
    Build the argument namespace expected by the
    official Ultralytics BoT-SORT implementation.
    """

    cfg = config[
        "tracking"
    ][
        "botsort"
    ]

    return SimpleNamespace(

        # --------------------------------------------------------------
        # Thresholds
        # --------------------------------------------------------------

        track_high_thresh=cfg[
            "track_high_thresh"
        ],

        track_low_thresh=cfg[
            "track_low_thresh"
        ],

        new_track_thresh=cfg[
            "new_track_thresh"
        ],

        # --------------------------------------------------------------
        # Association
        # --------------------------------------------------------------

        match_thresh=cfg[
            "match_thresh"
        ],

        track_buffer=cfg[
            "track_buffer"
        ],

        fuse_score=cfg[
            "fuse_score"
        ],

        # --------------------------------------------------------------
        # ReID
        # --------------------------------------------------------------

        with_reid=cfg[
            "with_reid"
        ],

        proximity_thresh=cfg[
            "proximity_thresh"
        ],

        appearance_thresh=cfg[
            "appearance_thresh"
        ],

        model=cfg[
            "model"
        ],

        # --------------------------------------------------------------
        # GMC
        # --------------------------------------------------------------

        gmc_method=cfg[
            "gmc_method"
        ],

        # --------------------------------------------------------------
        # Optional
        # --------------------------------------------------------------

        device=None,
    )