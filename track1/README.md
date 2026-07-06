
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
