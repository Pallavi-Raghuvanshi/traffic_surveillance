## **Pipelines**

1. #### Faster R-CNN

Initialize Detector (once)

│

├── Read config

├── Load pretrained Faster R-CNN

├── Load preprocessing transforms

├── Move model to CPU/GPU

└── Store COCO class names

&#x20;         │

&#x20;         ▼

For every video frame

│

├── Receive OpenCV frame (BGR)

├── Convert BGR → RGB (Faster R-CNN is trained on RGB images only)

├── Convert NumPy → PIL (Since pretrained weights' transform pipeline accepts PIL image only as input)

├── Apply preprocessing

│     ├── PIL → Tensor

│     ├── Convert to float

│     ├── Normalize

│     └── HWC → CHW

├── Move tensor to CPU/GPU

├── Run Faster R-CNN inference

├── Receive boxes, scores, and labels

├── Remove low-confidence detections

├── Remove unwanted classes

├── Convert results into `Detection` objects

└── Return the final list of detections to the tracker

#### 2\. Ultralytics Detector ----------------------------------------------------

Initialize Detector (once)

│

├── Read configuration

├── Read backend (YOLO or RT-DETR)

├── Validate model path

├── Load the selected Ultralytics model

├── Store confidence threshold

├── Store IoU threshold (used only for YOLO)

├── Store execution device

└── Store allowed classes

&#x20;         │

&#x20;         ▼

For every video frame

│

├── Receive OpenCV frame (NumPy, BGR)

├── Call Ultralytics `predict()`

│     ├── Internal preprocessing

│     │     ├── Convert image format if required

│     │     ├── Resize

│     │     ├── Normalize

│     │     ├── Convert to tensor

│     │     └── Move to CPU/GPU

│     ├── Run YOLO or RT-DETR inference

│     ├── Apply NMS (YOLO only)

│     └── Return prediction results

├── Iterate over detected objects

├── Convert class IDs to class names

├── Filter unwanted classes

├── Convert Ultralytics outputs into project `Detection` objects

└── Return detections to the tracker

#### 3\. BoTSORT Tracker -------------------------------------------------------

Video Frame

&#x20;     │

&#x20;     ▼

Detector

&#x20;     │

&#x20;     ▼

list\[Detection]

&#x20;     │

&#x20;     ▼

TrackingResults Adapter

&#x20;     │

&#x20;     ▼

Ultralytics BoTSORT

────────────────────────────

Kalman Prediction

Appearance Embeddings

IoU Computation

Appearance Similarity

Similarity Fusion

Hungarian Matching

Track Update

New Track Creation

Lost Track Removal

────────────────────────────

&#x20;     │

&#x20;     ▼

Tracked NumPy Array

&#x20;     │

&#x20;     ▼

Convert to Track objects

&#x20;     │

&#x20;     ▼

list\[Track]

#### 4. Pipeline ----------------------------------------------------------------------

ExperimentRunner

&#x20;       │

&#x20;       ▼

Pipeline.run()

&#x20;       │

&#x20;       ▼

Read next frame

&#x20;       │

&#x20;       ▼

Detection

&#x20;       │

&#x20;       ▼

Tracking

&#x20;       │

&#x20;       ▼

Trajectory Update

&#x20;       │

&#x20;       ▼

Speed Estimation

&#x20;       │

&#x20;       ▼

Visualization

&#x20;       │

&#x20;       ▼

Write annotated frame

&#x20;       │

&#x20;       ▼

Update Metrics

&#x20;       │

&#x20;       ▼

Update Evaluator

&#x20;       │

&#x20;       ▼

Repeat for next frame

&#x20;       │

&#x20;       ▼

Close resources

&#x20;       │

&#x20;       ▼

Return BenchmarkSummary

#### 5. Benchmark Visualizer --------------------------------------------------------------------------------------

BenchmarkRunner
        │
        ▼
Detector detects objects
        │
        ▼
BenchmarkVisualizer.draw()
        │
        ├── Copy frame
        ├── Draw bounding boxes
        ├── Draw class labels
        ├── Draw detector name
        ├── Draw FPS
        ├── Draw frame number
        └── Draw detection count
        │
        ▼
Annotated frame
        │
        ▼
BenchmarkVisualizer.write()
        │
        ▼
Frame written to MP4
        │
        ▼
After last frame
        │
        ▼
BenchmarkVisualizer.close()

#### 6. Visualizer --------------------------------------------------------------------------------------------------------------------------------

Pipeline
│
▼
Detector
│
▼
Tracker
│
▼
Trajectory Manager
│
▼
Speed Estimator
│
▼
Visualizer
│
├── Draw bounding boxes
├── Draw Track ID
├── Draw Class Name
├── Draw FPS
├── Draw Frame Number
└── Save video

#### 7. Evaluation -------------------------------------------------------------------------------------------------------------------------------

main.py
    │
    ▼
ExperimentRunner
    │
    ├── Metrics()                  ← created
    ├── Evaluator()                ← created
    ├── MetricsExporter()          ← created
    └── Pipeline
            │
            ▼
       For every frame
            │
            ├── Metrics.update()
            └── Evaluator.update()
            │
            ▼
      End of video
            │
            ▼
      Metrics.summary()
            │
            ▼
     BenchmarkSummary
            │
      ┌─────┴──────────┐
      ▼                ▼
Evaluator.print()   MetricsExporter.export()
