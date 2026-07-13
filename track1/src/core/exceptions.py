# exceptions.py
# ============================================================================

class TrafficSurveillanceError(Exception):
    pass

class ConfigurationError(TrafficSurveillanceError):
    pass

class VideoError(TrafficSurveillanceError):
    pass

class DetectorError(TrafficSurveillanceError):
    pass

class TrackerError(TrafficSurveillanceError):
    pass

class CalibrationError(TrafficSurveillanceError):
    pass

class SpeedEstimationError(TrafficSurveillanceError):
    pass

class EvaluationError(TrafficSurveillanceError):
    pass