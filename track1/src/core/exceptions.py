# ============================================================================
# exceptions.py
# ============================================================================


class TrafficSurveillanceError(Exception):
    """
    Base exception for the Traffic Surveillance project.
    """

    pass


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

class ConfigurationError(TrafficSurveillanceError):
    """
    Invalid or missing configuration.
    """

    pass


# ---------------------------------------------------------------------------
# Input
# ---------------------------------------------------------------------------

class VideoError(TrafficSurveillanceError):
    """
    Video loading or decoding error.
    """

    pass


# ---------------------------------------------------------------------------
# Detection
# ---------------------------------------------------------------------------

class DetectorError(TrafficSurveillanceError):
    """
    Detector initialization or inference error.
    """

    pass


# ---------------------------------------------------------------------------
# Tracking
# ---------------------------------------------------------------------------

class TrackerError(TrafficSurveillanceError):
    """
    Tracker initialization or update error.
    """

    pass


# ---------------------------------------------------------------------------
# Calibration
# ---------------------------------------------------------------------------

class CalibrationError(TrafficSurveillanceError):
    """
    Homography or calibration related error.
    """

    pass


# ---------------------------------------------------------------------------
# Speed Estimation
# ---------------------------------------------------------------------------

class SpeedEstimationError(TrafficSurveillanceError):
    """
    Speed estimation failure.
    """

    pass


# ---------------------------------------------------------------------------
# Evaluation
# ---------------------------------------------------------------------------

class EvaluationError(TrafficSurveillanceError):
    """
    Evaluation or benchmarking error.
    """

    pass