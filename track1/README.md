# 🚦 Traffic Surveillance System – Track 1

> **A Modular AI Framework for Vehicle Detection, Multi-Object Tracking, Speed Estimation, and Benchmarking**

Rather than relying on a single detector or tracker, the framework benchmarks multiple computer vision algorithms under one common pipeline — detectors, trackers, and speed estimators are swapped through configuration, with no source code changes.

**Objectives:** detect vehicles → track them consistently across frames → estimate real-world speed via camera calibration → compare algorithms on the same evaluation pipeline.

---

## 🏗️ Architecture

```text
config.yaml → Experiment Runner → Pipeline → Detector → Trajectory Manager → Tracker → Evaluation → Visualization → Results Export 
```

```text
track1/
├── configs/    config.yaml, logging.yaml
├── data/       raw/, processed/, calibration/
├── models/
├── outputs/    detections/, tracks/, speed/, visualizations/
├── src/        calibration/, core/, detection/, evaluation/, experiments/,
│               input/, pipeline/, speed/, tracking/, utils/, visualization/, main.py
└── tests/
```

---

## 🧩 Supported Algorithms

| Component | Algorithms                      | Base Class       |
| --------- | ------------------------------- | ---------------- |
| Detection | YOLO, RT-DETR, Faster R-CNN     | `BaseDetector` |
| Tracking  | ByteTrack, DeepSORT, BoT-SORT  | `BaseTracker`  |

All are selected entirely through `configs/config.yaml`:

```yaml
detection:
  algorithm: yolo
  model: yolo26

tracking:
  algorithm: bytetrack
```

Any detector × tracker × speed-estimator combination can be benchmarked automatically via `benchmark_detectors.py` / `benchmark_trackers.py`, which export comparison metrics (FPS, avg. detections/tracks, avg. speed) for every run.

---

## 📊 Benchmark Results

**Environment:** Python 3.12 · Ultralytics 8.4.89 · PyTorch · OpenCV · NVIDIA GPU
**Sample video:** `sample.avi` — 1280×720, 10 FPS, 2001 frames. All detectors/trackers were run on the same video with identical pipeline settings.

### Detector Benchmark

| Rank | Detector     |   FPS | Avg Time (ms) | Avg Detections | Avg Tracks | Avg Speed |
| ---- | ------------ | ----: | ------------: | -------------: | ---------: | --------: |
| 1    | YOLO11n      | 72.84 |         14.67 |           5.16 |       3.91 |    115.37 |
| 2    | YOLO26n      | 67.88 |         15.25 |           4.94 |       3.55 |    115.60 |
| 3    | RT-DETR-L    | 16.67 |         61.50 |          16.75 |      12.21 |     56.79 |
| 4    | Faster R-CNN |  7.14 |        140.10 |          14.53 |      12.22 |     55.62 |

YOLO11n gives the best speed/accuracy balance; RT-DETR-L and Faster R-CNN detect more objects but are too slow for real-time use.

### Tracker Benchmark

| Rank | Tracker   |   FPS | Avg Time (ms) | Avg Detections | Avg Tracks | Avg Speed |
| ---- | --------- | ----: | ------------: | -------------: | ---------: | --------: |
| 1    | ByteTrack | 69.18 |         15.50 |           5.16 |       3.91 |    115.37 |
| 2    | BoTSORT   | 27.83 |         37.28 |           5.16 |       2.11 |    179.67 |
| 3    | DeepSORT  | 24.85 |         66.57 |           5.16 |       4.69 |    109.21 |

ByteTrack is fastest (motion-only association). DeepSORT costs more due to appearance embeddings. Official Ultralytics BoT-SORT is integrated and working, though it currently yields fewer active tracks than ByteTrack — likely needs threshold/GMC/ReID tuning.

> **⚠️ Note:** Speed values above come from the temporary `PixelSpeedEstimator` — no homography calibration has been applied yet, so they are **relative benchmarking metrics only**, not physical km/h. Real-world speeds will be available once `HomographySpeedEstimator` is integrated.

**Conclusion:** YOLO11n + ByteTrack is the current default combination. BoT-SORT is fully integrated and will be tuned further. RT-DETR-L and DeepSORT remain available for comparative evaluation.

**Future work:** homography-based speed estimation, BoT-SORT hyperparameter tuning, MOTA/IDF1/HOTA tracking evaluation, mAP-based detector evaluation, multi-camera evaluation, AI City Challenge dataset benchmarking.

---

## 🚀 Getting Started

```bash
git clone <repository-url>
cd track1

python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Linux

pip install -r requirements.txt

# Edit configs/config.yaml to select detector, tracker, speed estimator, weights, thresholds
python src/main.py
```

---

## 🔬 Extending the Framework

| Add a...        | Steps                                                                                    |
| --------------- | ---------------------------------------------------------------------------------------- |
| Detector        | Subclass `BaseDetector` in `src/detection/`, register in `DetectorFactory`         |
| Tracker         | Subclass `BaseTracker` in `src/tracking/`, register in `TrackerFactory`            |
| Speed Estimator | Subclass `BaseSpeedEstimator` in `src/speed/`, register in `SpeedEstimatorFactory` |

No pipeline modifications are required.

---

## 📅 Roadmap

- 🚧 **In Progress** — speed estimation integration (`HomographySpeedEstimator`)
- 📌 **Planned** — multi-camera tracking, vehicle ReID, traffic density estimation, lane-wise analytics, vehicle counting, event detection, web dashboard, REST API, real-time deployment

---

## 👨‍💻 Tech Stack

Python 3.12+ · OpenCV · NumPy · Ultralytics · PyTorch · SciPy · PyYAML

**Design principles:** modular, extensible, configuration-driven, algorithm-independent, research-oriented, maintainable, scalable.

---

## References

1. [fasterrcnn_resnet50_fpn Documentation](URhttps://docs.pytorch.org/vision/stable/models/generated/torchvision.models.detection.fasterrcnn_resnet50_fpn.htmlL)
2. [Model Prediction with Ultralytics YOLO
   ](https://docs.ultralytics.com/modes/predict#introduction)
2. [BoTSORT  Tracker Reference](https://docs.ultralytics.com/reference/trackers/bot_sort#ultralytics.trackers.bot_sort.BOTrack)

---

## 📄 License & Authors

Developed for academic and research purposes — M.Sc. Data Science Minor Project.

**Pallavi Raghuvanshi**
