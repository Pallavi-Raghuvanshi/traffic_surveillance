
# Track 3 – Vehicle Re-Identification

## Overview

Track 3 implements a complete Vehicle Re-Identification (Re-ID) pipeline for intelligent traffic surveillance. The objective is to determine whether two vehicle images captured from different cameras belong to the same physical vehicle.

Unlike object tracking, which assigns temporary IDs within a single camera, Vehicle Re-ID enables matching vehicles across multiple cameras by learning discriminative visual feature embeddings.

The implementation is built on the OSNet (Omni-Scale Network) architecture and fine-tuned on the VeRi-776 dataset.

---

## Objectives

- Learn discriminative feature embeddings for vehicles.
- Match vehicles across different viewpoints and cameras.
- Fine-tune a pretrained OSNet model on VeRi-776.
- Evaluate performance using standard Re-ID metrics.
- Provide an inference pipeline capable of comparing arbitrary vehicle images.
- Demonstrate the model through a Flask-based web interface.

---

## Features

- VeRi-776 dataset support
- Data augmentation pipeline
- OSNet integration
- Fine-tuning using ImageNet pretrained weights
- Cross Entropy training
- Embedding extraction
- Cosine similarity matching
- Rank-1 evaluation
- Rank-5 evaluation
- Mean Average Precision (mAP)
- Checkpoint saving
- Training log generation
- Flask demonstration interface

---

## Project Structure

```
track3/

├── checkpoints/
│   ├── best_model.pth
│   ├── osnet_epoch_1.pth
│   └── training_log.csv
│
├── core/
│
├── data/
│   ├── dataloader.py
│   ├── transforms.py
│   └── veri_dataset.py
│
├── demo/
│   ├── app.py
│   ├── predictor.py
│   ├── static/
│   └── templates/
│
├── evaluation/
│   ├── evaluate.py
│   └── metrics.py
│
├── models/
│   └── osnet.py
│
├── training/
│   ├── losses.py
│   ├── trainer.py
│   ├── train.py
│   └── validator.py
│
├── services/
│
├── tests/
│
└── utils/
```

---

## Pipeline

```
Vehicle Image

        │

        ▼

Image Preprocessing

        │

        ▼

OSNet

        │

        ▼

512-Dimensional Embedding

        │

        ▼

Cosine Similarity

        │

        ▼

Vehicle Match Decision
```

---

## Training Pipeline

```
VeRi Dataset

        │

        ▼

Data Loader

        │

        ▼

OSNet

        │

        ▼

Classification Layer

        │

        ▼

Cross Entropy Loss

        │

        ▼

Backpropagation

        │

        ▼

Updated Model Parameters
```

---

## Inference Pipeline

```
Query Vehicle

        │

        ▼

Embedding Extraction

        │

        ▼

Gallery Vehicle

        │

        ▼

Embedding Extraction

        │

        ▼

Cosine Similarity

        │

        ▼

Similarity Score

        │

        ▼

Same / Different Vehicle
```

---

## Model

Architecture:

- OSNet x1.0

Initialization:

- ImageNet pretrained weights

Embedding Dimension:

- 512

Training Dataset:

- VeRi-776

Loss Function:

- Cross Entropy Loss

Optimizer:

- Adam

Learning Rate Scheduler:

- Cosine Annealing Learning Rate

Mixed Precision Training:

- Automatic Mixed Precision (AMP)

---

## Dataset

Dataset:

VeRi-776

Contains

- 576 training identities
- 200 testing identities
- 37,778 training images
- 11,579 gallery images
- 1,678 query images

Images are captured from 20 non-overlapping traffic cameras.

---

## Evaluation Metrics

Vehicle Re-ID performance is evaluated using:

### Rank-1 Accuracy

Percentage of queries whose correct vehicle appears as the top retrieved result.

### Rank-5 Accuracy

Percentage of queries whose correct vehicle appears within the top five retrieved results.

### Mean Average Precision (mAP)

Measures retrieval quality by considering the ranking positions of all correct matches.

---

## Results

### Baseline (ImageNet Pretrained)

| Metric | Score  |
| ------ | ------ |
| Rank-1 | 55.24% |
| Rank-5 | 69.73% |
| mAP    | 13.12% |

---

### Fine-Tuned Model

| Metric | Score            |
| ------ | ---------------- |
| Rank-1 | **91.06%** |
| Rank-5 | **95.65%** |
| mAP    | **53.60%** |

---

## Demonstration Interface

A Flask-based interface allows users to

- Upload two vehicle images
- Generate embeddings
- Compute cosine similarity
- Predict whether both images belong to the same vehicle
- Display inference statistics

---

## Integration with Overall Project

Track 3 consumes the output of Track 1.

```
Camera Stream

        │

        ▼

Track 1

Vehicle Detection + Tracking

        │

Representative Vehicle Crop

        │

        ▼

Track 3

Vehicle Re-Identification

        │

        ▼

Embedding Database

        │

        ▼

Cross-Camera Vehicle Matching
```

Track 1 assigns temporary track IDs within a camera.

Track 3 links those tracks across different cameras by comparing learned feature embeddings.

---

## Future Improvements

- Triplet Loss training
- Combined Cross Entropy + Triplet Loss
- Batch Hard Mining
- FAISS-based embedding search
- Multi-camera embedding database
- Online Re-Identification
- Cross-camera vehicle trajectory reconstruction
- Real-time deployment with live camera streams

---

## References

Zhou, Kaiyang, et al.

**Omni-Scale Feature Learning for Person Re-Identification**

International Conference on Computer Vision (ICCV), 2019.

Liu, Xinchen, et al.

**Large-scale Vehicle Re-identification in Urban Surveillance Videos**

IEEE International Conference on Multimedia and Expo (ICME), 2016.
