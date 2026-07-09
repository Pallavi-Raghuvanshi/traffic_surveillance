# ============================================================================
# detectors/__init__.py
#
# Importing this package registers every built-in anomaly detector with
# `AnomalyDetectorFactory`. A new detector module only needs to be
# imported here to become available — no other file changes.
# ============================================================================

from .base_anomaly_detector import (
    BaseAnomalyDetector,
    FrameContext,
)

from .factory import (
    AnomalyDetectorFactory,
)

from .abnormal_trajectory_detector import (
    AbnormalTrajectoryDetector,
)

from .collision_detector import (
    CollisionDetector,
)

from .near_collision_detector import (
    NearCollisionDetector,
)

from .stalled_vehicle_detector import (
    StalledVehicleDetector,
)

from .sudden_stop_detector import (
    SuddenStopDetector,
)

from .vehicle_reversal_detector import (
    VehicleReversalDetector,
)

from .wrong_way_detector import (
    WrongWayDetector,
)

__all__ = [

    "BaseAnomalyDetector",

    "FrameContext",

    "AnomalyDetectorFactory",

    "CollisionDetector",

    "NearCollisionDetector",

    "StalledVehicleDetector",

    "SuddenStopDetector",

    "AbnormalTrajectoryDetector",

    "WrongWayDetector",

    "VehicleReversalDetector",
]
