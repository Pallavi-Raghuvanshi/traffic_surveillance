# Traffic Surveillance Project - Environment Setup

This guide explains how to set up the development environment on both GPU and CPU systems.

---

# 1. Clone the Repository

```bash
git clone <repository-url>
cd traffic_surveillance
```

---

# 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the virtual environment.

### Windows

```bash
.venv\Scripts\activate
```

Upgrade pip.

```bash
python -m pip install --upgrade pip
```

---

# 3. Install PyTorch

## Option A — NVIDIA GPU (CUDA)

Install the CUDA-enabled build.

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
```

Verify the installation.

```bash
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0))"
```

Example output:

```text
2.5.1+cu124
True
NVIDIA GeForce GTX 1650
```

---

## Option B — CPU Only

```bash
pip install torch torchvision torchaudio
```

Verify.

```bash
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"
```

Example output:

```text
2.5.1
False
```

---

# 4. Install Project Dependencies

```bash
pip install -r requirements.txt
```

---

# 5. Clone Torchreid

Clone the official repository inside the project.

```bash
git clone https://github.com/KaiyangZhou/deep-person-reid.git external/deep-person-reid
```

---

# 6. Install Torchreid

Install it in editable mode.

```bash
pip install -e external/deep-person-reid
```

---

# 7. Verify Torchreid Installation

Run:

```bash
python -c "from torchreid.models import build_model; model = build_model(name='osnet_x1_0', num_classes=1000, pretrained=True); print(type(model))"
```

Expected output:

```text
<class 'torchreid.models.osnet.OSNet'>
```

---

# Final Project Structure

```text
traffic_surveillance/
│
├── requirements.txt
│
├── track1/
├── track2/
├── track3/
│	└── external/
│   	└── deep-person-reid/
└── setup.md
```

---

# Notes

- Install PyTorch before installing the project dependencies.
- GPU users should install the CUDA-enabled PyTorch build.
- CPU users should install the default PyTorch build.
- The project source code is identical for both environments.
- Torchreid is installed from the official GitHub repository in editable mode so that its source code can be inspected, debugged, and studied.
