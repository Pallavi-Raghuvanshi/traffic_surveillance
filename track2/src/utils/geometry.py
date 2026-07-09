# ============================================================================
# geometry.py
#
# Pure geometric and vector-motion helpers shared by the anomaly engine
# and every anomaly detector. Functions here operate on plain tuples and
# BoundingBox values only — no dependency on tracks, history, or config.
# ============================================================================

from __future__ import annotations

import math
from typing import Sequence

from core.constants import EPSILON_SPEED
from core.schemas import BoundingBox


Point = tuple[float, float]
Vector = tuple[float, float]


# ---------------------------------------------------------------------- #
# Bounding Box Geometry
# ---------------------------------------------------------------------- #

def centroid(
    bbox: BoundingBox,
) -> Point:
    """
    Return the geometric center of a bounding box.
    """

    return (

        (bbox.x1 + bbox.x2) / 2.0,

        (bbox.y1 + bbox.y2) / 2.0,
    )


def area(
    bbox: BoundingBox,
) -> float:

    width = max(0.0, bbox.x2 - bbox.x1)

    height = max(0.0, bbox.y2 - bbox.y1)

    return width * height


def iou(
    a: BoundingBox,
    b: BoundingBox,
) -> float:
    """
    Intersection-over-Union of two axis-aligned bounding boxes.
    """

    inter_x1 = max(a.x1, b.x1)
    inter_y1 = max(a.y1, b.y1)
    inter_x2 = min(a.x2, b.x2)
    inter_y2 = min(a.y2, b.y2)

    inter_width = max(0.0, inter_x2 - inter_x1)
    inter_height = max(0.0, inter_y2 - inter_y1)

    intersection = inter_width * inter_height

    union = area(a) + area(b) - intersection

    if union <= 0.0:

        return 0.0

    return intersection / union


def bbox_gap_distance(
    a: BoundingBox,
    b: BoundingBox,
) -> float:
    """
    Shortest edge-to-edge distance between two bounding boxes.

    Returns 0.0 when the boxes touch or overlap.
    """

    dx = max(0.0, max(a.x1, b.x1) - min(a.x2, b.x2))

    dy = max(0.0, max(a.y1, b.y1) - min(a.y2, b.y2))

    return math.hypot(dx, dy)


# ---------------------------------------------------------------------- #
# Vector / Motion Geometry
# ---------------------------------------------------------------------- #

def euclidean_distance(
    p1: Point,
    p2: Point,
) -> float:

    return math.hypot(
        p2[0] - p1[0],
        p2[1] - p1[1],
    )


def vector_between(
    p1: Point,
    p2: Point,
) -> Vector:
    """
    Displacement vector pointing from `p1` to `p2`.
    """

    return (
        p2[0] - p1[0],
        p2[1] - p1[1],
    )


def vector_magnitude(
    vector: Vector,
) -> float:

    return math.hypot(
        vector[0],
        vector[1],
    )


def vector_heading(
    vector: Vector,
) -> float | None:
    """
    Direction of `vector` in radians, or None if the vector is
    too small to carry a reliable direction.
    """

    if vector_magnitude(vector) < EPSILON_SPEED:

        return None

    return math.atan2(
        vector[1],
        vector[0],
    )


def angle_difference(
    heading_a: float,
    heading_b: float,
) -> float:
    """
    Smallest absolute angle (radians, in [0, pi]) between two headings.
    """

    diff = abs(heading_a - heading_b) % (2 * math.pi)

    if diff > math.pi:

        diff = (2 * math.pi) - diff

    return diff


def circular_mean(
    headings: Sequence[float],
) -> float | None:
    """
    Mean direction of a sequence of headings (radians).

    Returns None for an empty sequence.
    """

    if not headings:

        return None

    sin_sum = sum(math.sin(h) for h in headings)

    cos_sum = sum(math.cos(h) for h in headings)

    if abs(sin_sum) < EPSILON_SPEED and abs(cos_sum) < EPSILON_SPEED:

        return None

    return math.atan2(
        sin_sum,
        cos_sum,
    )


def circular_variance(
    headings: Sequence[float],
) -> float:
    """
    Circular variance of a sequence of headings, in [0, 1].

    0.0 means every heading points the same direction; values close to
    1.0 mean headings are scattered in all directions (erratic motion).
    """

    if len(headings) < 2:

        return 0.0

    sin_sum = sum(math.sin(h) for h in headings)

    cos_sum = sum(math.cos(h) for h in headings)

    mean_resultant_length = (

        math.hypot(sin_sum, cos_sum)

        / len(headings)
    )

    return 1.0 - mean_resultant_length
