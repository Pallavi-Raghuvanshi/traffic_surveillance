# ============================================================================
# exceptions.py
# ============================================================================


class AnomalyDetectionError(Exception):
    """
    Base exception for the Traffic Anomaly Detection project.
    """

    pass


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

class ConfigurationError(AnomalyDetectionError):
    """
    Invalid or missing configuration.
    """

    pass


# ---------------------------------------------------------------------------
# Input
# ---------------------------------------------------------------------------

class TrackSourceError(AnomalyDetectionError):
    """
    Track source loading or decoding error.
    """

    pass


class VideoError(AnomalyDetectionError):
    """
    Video loading or decoding error.
    """

    pass


# ---------------------------------------------------------------------------
# Detectors
# ---------------------------------------------------------------------------

class DetectorRegistrationError(AnomalyDetectionError):
    """
    Anomaly detector registration or lookup error.
    """

    pass


class AnomalyDetectorError(AnomalyDetectionError):
    """
    Anomaly detector initialization or processing error.
    """

    pass


# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------

class EngineError(AnomalyDetectionError):
    """
    Anomaly engine orchestration error.
    """

    pass


# ---------------------------------------------------------------------------
# Evaluation
# ---------------------------------------------------------------------------

class EvaluationError(AnomalyDetectionError):
    """
    Evaluation or benchmarking error.
    """

    pass
