
# 🚦 Traffic Surveillance System – Track 1

> **A Modular AI Framework for Vehicle Detection, Multi-Object Tracking, Speed Estimation, and Benchmarking**

---

## 📌 Overview

This project is a research-oriented traffic surveillance framework developed as part of an M.Sc. Data Science Minor Project.

Unlike conventional implementations that rely on a single detection or tracking algorithm, this framework is designed to **benchmark multiple computer vision algorithms under a common pipeline**.

The architecture allows different detectors, trackers, and speed estimation techniques to be swapped through configuration without modifying the source code.

---

## 🎯 Objectives

- Detect vehicles in traffic surveillance videos.
- Track vehicles consistently across consecutive frames.
- Estimate real-world vehicle speeds using camera calibration.
- Compare multiple AI algorithms using the same evaluation pipeline.
- Build a scalable framework for future traffic analytics research.

---

# 🏗️ System Architecture

```text
                   config.yaml
                        │
                        ▼
               Experiment Runner
                        │
                        ▼
                   Processing Pipeline
                        │
        ┌───────────────┼────────────────┐
        ▼               ▼                ▼
  Vehicle Detector   Multi-Object    Speed Estimator
                        Tracker
        │               │                │
        └───────────────┼────────────────┘
                        ▼
               Trajectory Manager
                        │
                        ▼
                  Evaluation Module
                        │
                        ▼
                   Visualization
                        │
                        ▼
                  Results Exporter
```

---

# 📂 Project Structure

```text
track1/

├── configs/
│   ├── config.yaml
│   └── logging.yaml
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── calibration/
│
├── logs/
│
├── models/
│
├── outputs/
│   ├── detections/
│   ├── speed/
│   ├── tracks/
│   └── visualizations/
│
├── src/
│
│   ├── calibration/
│   ├── core/
│   ├── detection/
│   ├── evaluation/
│   ├── experiments/
│   ├── input/
│   ├── pipeline/
│   ├── speed/
│   ├── tracking/
│   ├── utils/
│   ├── visualization/
│   │
│   └── main.py
│
└── tests/
```

---

# 🔄 Processing Workflow

```text
Video Input
      │
      ▼
Video Loader
      │
      ▼
Vehicle Detection
      │
      ▼
Multi-Object Tracking
      │
      ▼
Trajectory Management
      │
      ▼
Speed Estimation
      │
      ▼
Evaluation
      │
      ▼
Visualization
      │
      ▼
Results Export
```

---

# 🚗 Vehicle Detection

The framework supports multiple detection algorithms through a common interface.

### Current Algorithms

- YOLO
- RT-DETR
- Faster R-CNN

Each detector inherits from `BaseDetector`.

Adding a new detector only requires:

1. Create a detector class.
2. Extend `BaseDetector`.
3. Register it inside `DetectorFactory`.

No pipeline modifications are required.

---

# 🎯 Multi-Object Tracking

Supported tracking algorithms:

- ByteTrack
- DeepSORT
- BoT-SORT

Each tracker implements `BaseTracker`.

The tracker is selected entirely through `config.yaml`.

---

# 🚙 Speed Estimation

Implemented speed estimation framework:

- Homography-based estimation
- Optical Flow estimation
- Hybrid estimation

All estimators implement `BaseSpeedEstimator`.

---

# ⚙️ Configuration Driven Design

Experiments are configured through:

```text
configs/config.yaml
```

Example:

```yaml
detection:
  algorithm: yolo
  model: yolo26

tracking:
  algorithm: bytetrack

speed:
  algorithm: homography
```

Changing the algorithm requires **no source code modifications**.

---

# 📊 Benchmarking Framework

The framework is designed to compare combinations such as:

| Detector     | Tracker   | Speed Estimator |
| ------------ | --------- | --------------- |
| YOLO         | ByteTrack | Homography      |
| YOLO         | DeepSORT  | Homography      |
| RT-DETR      | ByteTrack | Optical Flow    |
| Faster R-CNN | BoT-SORT  | Hybrid          |

Evaluation results are exported automatically for comparison.

---

# 📈 Evaluation Metrics

### Currently Implemented

- Average FPS
- Average Vehicle Speed
- Average Detections per Frame

### Planned Metrics

- mAP
- Precision
- Recall
- MOTA
- MOTP
- IDF1
- HOTA
- Speed MAE
- RMSE

---

# 🖥️ Benchmark Environment

Benchmarking was performed under the following environment:

- **Python**: 3.12
- **Ultralytics**: 8.4.89
- **PyTorch** (Torch)
- **OpenCV**
- **GPU**: NVIDIA GPU

**Sample video**

| Property   | Value          |
| ---------- | -------------- |
| File       | `sample.avi`   |
| Resolution | 1280 × 720     |
| FPS        | 10             |
| Frames     | 2001           |

All detectors and trackers were benchmarked using the **same video** and **identical pipeline settings**, ensuring that the results below are directly comparable across algorithms.

---

# 🚗 Detector Benchmark

| Rank | Detector     | Frames | FPS   | Avg Time (ms) | Avg Detections | Avg Tracks | Avg Speed |
| ---- | ------------ | -----: | ----: | -------------: | --------------: | ----------: | ---------: |
| 1    | YOLO11n      | 2001   | 72.84 | 14.67          | 5.16            | 3.91        | 115.37     |
| 2    | YOLO26n      | 2001   | 67.88 | 15.25          | 4.94            | 3.55        | 115.60     |
| 3    | RT-DETR-L    | 2001   | 16.67 | 61.50           | 16.75           | 12.21       | 56.79      |
| 4    | Faster R-CNN | 2001   | 7.14  | 140.10          | 14.53           | 12.22       | 55.62      |

**Discussion**

- **YOLO11n** achieved the highest throughput among all evaluated detectors.
- **YOLO26n** was slightly slower, with similar detection behaviour overall.
- **RT-DETR-L** detected considerably more objects but required significantly more computation, reducing achievable FPS.
- **Faster R-CNN** produced competitive detection counts but was unsuitable for real-time inference due to its low FPS.

---

# 🎯 Tracker Benchmark

| Rank | Tracker   | Frames | FPS   | Avg Time (ms) | Avg Detections | Avg Tracks | Avg Speed |
| ---- | --------- | -----: | ----: | -------------: | --------------: | ----------: | ---------: |
| 1    | ByteTrack | 2001   | 69.18 | 15.50           | 5.16            | 3.91        | 115.37     |
| 2    | BoTSORT   | 2001   | 27.83 | 37.28           | 5.16            | 2.11        | 179.67     |
| 3    | DeepSORT  | 2001   | 24.85 | 66.57           | 5.16            | 4.69        | 109.21     |

**Discussion**

- **ByteTrack** was the fastest tracker, benefiting from its lightweight, motion-only association strategy.
- **DeepSORT** incurred additional computational cost due to its use of appearance embeddings for re-identification.
- The official **Ultralytics BoT-SORT** integration was successfully completed and benchmarked end-to-end within the framework.
- **BoTSORT** currently reports fewer active tracks than ByteTrack, suggesting that additional parameter tuning (thresholds, GMC, or ReID configuration) may improve its tracking performance.

---

# 🔑 Key Observations

- The detector benchmarking framework is fully functional.
- The tracker benchmarking framework is fully functional.
- All algorithms execute through the same `ExperimentRunner` and `Pipeline`, ensuring a fair, like-for-like comparison.
- Benchmark metrics are automatically exported for every run.
- **YOLO11n** currently provides the best balance between speed and computational efficiency.
- **ByteTrack** currently provides the highest throughput among the evaluated trackers.
- **BoTSORT** is integrated successfully but still requires configuration tuning for optimal tracking performance.

> **⚠️ Important Note**
>
> Current speed values are generated using the temporary `PixelSpeedEstimator`.
>
> Since no homography calibration has yet been applied, these values are **not** physically meaningful (km/h) and should be interpreted **only as relative benchmarking metrics**.
>
> Meaningful real-world vehicle speeds will be available once the `HomographySpeedEstimator` is integrated.

---

# 🧾 Conclusions

- **YOLO11n** is currently selected as the default detector due to its excellent balance of speed and efficiency.
- **ByteTrack** serves as the primary baseline tracker for the framework.
- The official **Ultralytics BoT-SORT** integration has been completed successfully and will be further tuned for improved tracking quality.
- **RT-DETR-L** and **DeepSORT** remain available as higher-complexity alternatives for comparative evaluation.

---

# 🔭 Future Work

- Homography-based speed estimation.
- BoTSORT hyperparameter tuning.
- Tracking quality evaluation (MOTA, IDF1, HOTA).
- Detector evaluation using mAP metrics.
- Multi-camera evaluation.
- AI City Challenge dataset benchmarking.

---

# 🧩 Design Principles

The framework is built around the following principles:

- Modular
- Extensible
- Configuration-driven
- Algorithm-independent
- Research-oriented
- Maintainable
- Scalable

---

# 🚀 Getting Started

## 1. Clone the Repository

```bash
git clone <repository-url>
cd track1
```

---

## 2. Create Virtual Environment

```bash
python -m venv .venv
```

Activate

Windows

```bash
.venv\Scripts\activate
```

Linux

```bash
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Experiment

Edit

```text
configs/config.yaml
```

Select

- detector
- tracker
- speed estimator
- model weights
- thresholds

---

## 5. Run

```bash
python src/main.py
```

---

# 🔬 Extending the Framework

## Add a Detector

1. Create a detector in `src/detection/`
2. Inherit from `BaseDetector`
3. Register in `DetectorFactory`

---

## Add a Tracker

1. Create a tracker in `src/tracking/`
2. Inherit from `BaseTracker`
3. Register in `TrackerFactory`

---

## Add a Speed Estimator

1. Create a speed estimator in `src/speed/`
2. Inherit from `BaseSpeedEstimator`
3. Register in `SpeedEstimatorFactory`

---

# 📅 Development Roadmap

## ✅ Completed

- Project architecture
- Configuration management
- Video input pipeline
- Detection framework
- Tracking framework
- Speed estimation framework
- Calibration module
- Experiment runner
- Evaluation framework
- Benchmarking framework
- Visualization framework

---

## 🚧 In Progress

- Detector integration
- Tracker integration
- Speed estimation integration

---

## 📌 Planned

- Multi-camera vehicle tracking
- Vehicle Re-identification (ReID)
- Traffic density estimation
- Lane-wise analytics
- Vehicle counting
- Traffic event detection
- Web dashboard
- REST API
- Real-time deployment

---

# 👨‍💻 Technology Stack

- Python 3.12+
- OpenCV
- NumPy
- Ultralytics
- PyTorch
- SciPy
- PyYAML

---

# 📄 License

This project is developed for academic and research purposes.

---

# 👥 Authors

**Traffic Surveillance System**

Minor Project

Megh Nanavati

Pallavi Raghuvanshi

M.Sc. Data Science
