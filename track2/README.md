# 🚨 Traffic Surveillance System – Track 2 (Traffic Anomaly Detection)

> **A Modular, Detector/Tracker-Independent Anomaly Detection Engine — inspired by AI City Challenge 2018 Track 2**

M.Sc. Data Science Minor Project — **Component 2** of a four-component system. Component 2 performs no detection or tracking of its own: it consumes standardized `Track` objects produced by **Component 1** (default: YOLO11n + official Ultralytics BoT-SORT) and reasons purely over track geometry and motion history to flag anomalous traffic behaviour.

Every anomaly detector is a self-contained, independently pluggable module. New detectors register themselves with a factory and require **zero changes** to the orchestration engine.

---

## 🏗️ Architecture

```text
Component 1 (Track 1)                    Component 2 (Track 2)
──────────────────────                   ─────────────────────
video → detector → tracker    ──JSONL──▶  RecordedTrackSource
                                               │
                                               ▼
                                        TrackHistoryManager ──▶ DominantFlowModel
                                               │                      │
                                               ▼                      │
                                        AnomalyEngine  ◀──────────────┘
                                               │
                                   (7 independent AnomalyDetector modules)
                                               │
                                               ▼
                              AnomalyDeduplicator → AnomalyEvent[] → Evaluation / Visualization / Export
```

```text
track2/
├── configs/       config.yaml, logging.yaml
├── data/          raw/ (optional video), tracks/ (JSONL exports from Component 1)
├── outputs/       anomaly_runs/, anomaly_benchmark/
├── src/
│   ├── core/          config, schemas (BoundingBox, Track, FrameTracks, AnomalyEvent), exceptions, logger
│   ├── utils/          geometry.py (IoU, TTC, circular variance, ...), file_utils.py
│   ├── engine/         TrackHistoryManager, DominantFlowModel, AnomalyDeduplicator, AnomalyEngine
│   ├── detectors/      BaseAnomalyDetector, AnomalyDetectorFactory, 7 detector implementations
│   ├── input/          BaseTrackSource, RecordedTrackSource, VideoLoader (visualization only)
│   ├── evaluation/      Metrics, AnomalyEvaluator, MetricsExporter, AnomalyBenchmarkSummary
│   ├── visualization/  AnomalyVisualizer
│   ├── pipeline/        Pipeline (owns the per-frame loop)
│   ├── experiments/     ExperimentRunner (composition root)
│   ├── main.py
│   ├── export_tracks.py       bridges Component 1 → Component 2 (see below)
│   └── benchmark_anomalies.py
└── requirements.txt
```

This mirrors Track 1's architecture (`Config`, `ExperimentRunner`, `Pipeline`, ABC-based interfaces, `Metrics`/`Evaluator`/`MetricsExporter` split) so the two components feel like they were built by the same engineer.

---

## 🔗 Integration with Component 1

Component 2 is **fully detector- and tracker-independent**: the engine and every detector operate only on the generic `Track` dataclass (`track_id`, `bbox`, `confidence`, `class_id`, `class_name`).

The two components are connected by a plain-text file contract, not a shared Python process:

1. **`export_tracks.py`** runs Track 1's own YOLO11n detector + official BoT-SORT tracker over a video and writes one JSON record per frame to `data/tracks/*.jsonl`.
2. **`RecordedTrackSource`** streams that file back as `FrameTracks` for the anomaly engine.

```bash
# From track2/, with the shared project .venv active
python src/export_tracks.py --device cuda
python src/main.py
```

Because the boundary is a file, Component 2 never imports a line of Track 1's code at runtime, any upstream detector/tracker that can emit the same JSONL shape can replace Track 1 without touching Component 2, and tracks only need to be computed once even while anomaly parameters are iterated on repeatedly.

---

## 🚦 Anomalies Detected Today

All seven are inferred purely from bounding-box geometry and motion history — no homography, lane annotations, parking zones, traffic-light state, HD maps, GPS, or calibration.

| # | Anomaly                       | Signal                                                                                                                                                        |
| - | ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | **Vehicle Collision**   | Two boxes' IoU spikes above threshold while at least one track shows a sharp pre-impact deceleration.                                                         |
| 2 | **Near Collision**      | Estimated time-to-collision (closing speed vs. gap distance) drops below threshold without an actual impact.                                                  |
| 3 | **Stalled Vehicle**     | Track stays within a small radius (speed below the stationary threshold) for an abnormally long duration.                                                     |
| 4 | **Sudden Stop**         | Track's speed drops sharply relative to its own recent peak within a short window — a braking event.                                                         |
| 5 | **Abnormal Trajectory** | High circular variance of recent headings — zig-zag / erratic motion.                                                                                        |
| 6 | **Wrong-Way Driving**   | Track moves opposite to the**dominant flow direction learned automatically** from a grid of historical trajectory vectors — no manually defined lanes. |
| 7 | **Vehicle Reversal**    | Track's recent heading deviates ~180° from its own earlier heading (self-referential, unlike wrong-way).                                                     |

Every detector implements `BaseAnomalyDetector` and self-registers with `AnomalyDetectorFactory`; `AnomalyEngine` invokes whichever set is listed in `config.yaml`, aggregates results, and deduplicates ongoing events via a cooldown window. No detector is aware of any other detector.

---

## 🔭 Planned Anomalies (Blocked on Additional Data)

These require information this project deliberately does not assume is available. They are documented here so the roadmap is explicit once that data exists.

| Anomaly                   | Requires                                                    | Status                                                                         |
| ------------------------- | ----------------------------------------------------------- | ------------------------------------------------------------------------------ |
| Illegal Parking           | Lane / parking-zone annotations                             | Not implemented                                                                |
| Overspeeding              | Homography calibration (real-world speed, not pixel motion) | Not implemented — Component 1's`HomographySpeedEstimator` would supply this |
| Lane Violation            | Lane geometry annotations                                   | Not implemented                                                                |
| Stop-Line Violation       | Stop-line / intersection annotations                        | Not implemented                                                                |
| Restricted Zone Intrusion | Zone polygon definitions                                    | Not implemented                                                                |
| Red-Light Violation       | Traffic signal state feed                                   | Not implemented                                                                |
| Traffic Congestion        | Calibrated road-segment density / area                      | Not implemented                                                                |
| Tailgating                | Calibrated real-world following distance                    | Not implemented                                                                |

---

## ⚙️ Configuration

Nothing is hardcoded — every threshold, window, and path lives in `configs/config.yaml`:

```yaml
anomaly:
  detectors:
    - collision
    - near_collision
    - stalled_vehicle
    - sudden_stop
    - abnormal_trajectory
    - wrong_way
    - vehicle_reversal

  dedup_cooldown_seconds: 3.0

  collision:
    iou_threshold: 0.30
    pre_impact_min_speed: 25.0
    deceleration_ratio: 0.5
    confirmation_window_seconds: 0.8
```

---

## 🚀 Getting Started

```bash
cd track2
pip install -r requirements.txt        # plus track1/requirements.txt for export_tracks.py

python src/export_tracks.py             # produces data/tracks/sample.jsonl
python src/main.py                      # runs the anomaly engine over that export
python src/benchmark_anomalies.py       # benchmarks detector-set combinations
```

Outputs land in `outputs/anomaly_runs/<experiment>/`: `anomalies.csv` / `anomalies.json` (every `AnomalyEvent`), `metrics.csv` / `metrics.json` (aggregate `AnomalyBenchmarkSummary`), and `annotated.mp4` when a source video is available.

---

## 🔬 Extending the Framework

| Add a...         | Steps                                                                                                                                                                                       |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Anomaly Detector | Subclass`BaseAnomalyDetector` in `src/detectors/`, decorate with `@AnomalyDetectorFactory.register("name")`, import it in `detectors/__init__.py`, add its name to `config.yaml`. |
| Track Source     | Subclass`BaseTrackSource` in `src/input/` (e.g. a live streaming feed).                                                                                                                 |

No changes to `AnomalyEngine` or `Pipeline` are required.

---

## 👨‍💻 Tech Stack

Python 3.12+ · NumPy · OpenCV · PyYAML · tabulate

**Design principles:** modular, extensible (open/closed via detector registry), configuration-driven, detector/tracker-independent, composition over inheritance.

---

## 📄 License & Authors

Developed for academic and research purposes — M.Sc. Data Science Minor Project.

**Pallavi Raghuvanshi, Megh Nanavati**
