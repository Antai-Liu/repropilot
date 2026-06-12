"""File-content templates for the fake-image-detection project skeleton."""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Text / config templates
# ---------------------------------------------------------------------------

_README = """\
# {name}

Binary fake-image detection — fully reproducible on CPU, no external data needed.

> **No GPU required for the default demo.**

## What is this

A minimal end-to-end CNN pipeline that classifies images as real or fake.
By default it runs on randomly generated tensors, so no dataset download is
required and the full pipeline completes on CPU in seconds.

## Quickstart

```
pip install -r requirements.txt
python -m src.train
python -m src.eval
```

## Dataset

Dummy random tensors are used out of the box — no download required.
See [DATA.md](DATA.md) for instructions on substituting a real dataset.

## Training

```
python -m src.train
```

Outputs written to `outputs/`:
- `metrics.json` — final training loss
- `loss_curve.png` — per-epoch loss curve
- `run_config.yaml` — exact config snapshot for the run

## Evaluation

```
python -m src.eval
```

Outputs written to `outputs/`:
- `eval_metrics.json` — validation accuracy
- `confusion_matrix.png` — confusion matrix heatmap

## Results

| Metric   | Dummy-data baseline |
|----------|---------------------|
| Accuracy | ~0.50 (random)      |

## Reproducibility

All random seeds are fixed via `set_seed` in `src/utils.py`.
Every run snapshots its full config to `outputs/run_config.yaml`.
runnable evidence: not assessed in default scoring mode.

## Limitations

- Default data is random tensors — accuracy numbers are not meaningful.
- Replace `src/dataset.py` with a real fake-vs-real image loader for
  a genuine experiment.
"""

_DATA_MD = """\
# Dataset

## Default (dummy data)

`src/dataset.py` generates random tensors via `torch.randn`.
No download is required; labels are assigned randomly.

## Using a real dataset

1. Download your dataset (e.g. FaceForensics++, DFDC).
2. Organise images into `data/real/` and `data/fake/` subfolders.
3. Update `FakeImageDataset` in `src/dataset.py` to read from disk.
4. Set `data_path` in `configs/default.yaml` to point at `data/`.
"""

_REQUIREMENTS_TXT = """\
torch==2.2.0
torchvision==0.17.0
scikit-learn==1.4.0
matplotlib==3.8.3
pyyaml==6.0.1
"""

_DEFAULT_YAML = """\
seed: 42
lr: 0.001
batch_size: 32
epochs: 3
data_path: data/
device: cpu
"""

_MIT_LICENSE = """\
MIT License

Copyright (c) 2024 {name}

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

_REPROPILOT_YML = """\
name: ReproPilot check

on: [push, pull_request]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.10"
      - name: Install repropilot
        run: pip install repropilot
      - name: Check reproducibility score
        run: repropilot check .
"""

# ---------------------------------------------------------------------------
# Python source templates
# ---------------------------------------------------------------------------

_DATASET_PY = """\
from __future__ import annotations

import torch
from torch.utils.data import DataLoader, Dataset, random_split


class FakeImageDataset(Dataset):
    def __init__(
        self,
        n_samples: int = 200,
        img_size: int = 32,
        n_classes: int = 2,
        seed: int = 42,
    ) -> None:
        torch.manual_seed(seed)
        self.images = torch.randn(n_samples, 3, img_size, img_size)
        self.labels = torch.randint(0, n_classes, (n_samples,))

    def __len__(self) -> int:
        return len(self.labels)

    def __getitem__(self, idx: int):
        return self.images[idx], self.labels[idx]


def get_loaders(
    batch_size: int = 32, seed: int = 42
) -> tuple[DataLoader, DataLoader]:
    dataset = FakeImageDataset(seed=seed)
    n_train = int(0.8 * len(dataset))
    n_val = len(dataset) - n_train
    train_set, val_set = random_split(dataset, [n_train, n_val])
    train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_set, batch_size=batch_size)
    return train_loader, val_loader
"""

_MODEL_PY = """\
from __future__ import annotations

import torch.nn as nn


class SmallCNN(nn.Module):
    def __init__(self, n_classes: int = 2) -> None:
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 16, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(16, 32, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(32 * 8 * 8, 64),
            nn.ReLU(),
            nn.Linear(64, n_classes),
        )

    def forward(self, x):
        return self.classifier(self.features(x))
"""

_UTILS_PY = """\
from __future__ import annotations

import random

import torch


def set_seed(seed: int) -> None:
    random.seed(seed)
    torch.manual_seed(seed)
"""

_TRAIN_PY = """\
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import yaml

from .dataset import get_loaders
from .model import SmallCNN
from .utils import set_seed


def train(config_path: str = "configs/default.yaml") -> None:
    plt.switch_backend("Agg")

    with open(config_path) as f:
        cfg = yaml.safe_load(f)

    set_seed(cfg["seed"])
    device = torch.device(cfg.get("device", "cpu"))
    train_loader, _ = get_loaders(
        batch_size=cfg["batch_size"], seed=cfg["seed"]
    )

    model = SmallCNN().to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=cfg["lr"])
    criterion = nn.CrossEntropyLoss()

    losses: list[float] = []
    for epoch in range(cfg["epochs"]):
        model.train()
        total = 0.0
        for x, y in train_loader:
            x, y = x.to(device), y.to(device)
            optimizer.zero_grad()
            loss = criterion(model(x), y)
            loss.backward()
            optimizer.step()
            total += loss.item()
        losses.append(total / len(train_loader))
        print(f"Epoch {epoch + 1}/{cfg['epochs']}  loss={losses[-1]:.4f}")

    out = Path("outputs")
    out.mkdir(exist_ok=True)

    (out / "metrics.json").write_text(
        json.dumps(
            {"final_loss": losses[-1], "epochs": cfg["epochs"]},
            indent=2,
        )
    )

    fig, ax = plt.subplots()
    ax.plot(range(1, len(losses) + 1), losses, marker="o")
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Loss")
    ax.set_title("Training loss")
    fig.tight_layout()
    fig.savefig(out / "loss_curve.png")
    plt.close(fig)

    (out / "run_config.yaml").write_text(yaml.dump(cfg))
    torch.save(model.state_dict(), out / "model.pt")
    print(f"Saved outputs to {out}/")


if __name__ == "__main__":
    train()
"""

_EVAL_PY = """\
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import torch
import yaml
from sklearn.metrics import accuracy_score, confusion_matrix

from .dataset import get_loaders
from .model import SmallCNN
from .utils import set_seed


def evaluate(
    config_path: str = "configs/default.yaml",
    model_path: str = "outputs/model.pt",
) -> None:
    plt.switch_backend("Agg")

    with open(config_path) as f:
        cfg = yaml.safe_load(f)

    set_seed(cfg["seed"])
    device = torch.device(cfg.get("device", "cpu"))
    _, val_loader = get_loaders(
        batch_size=cfg["batch_size"], seed=cfg["seed"]
    )

    model = SmallCNN().to(device)
    model.load_state_dict(
        torch.load(model_path, map_location=device, weights_only=True)
    )
    model.eval()

    all_preds: list[int] = []
    all_labels: list[int] = []
    with torch.no_grad():
        for x, y in val_loader:
            preds = model(x.to(device)).argmax(dim=1).cpu()
            all_preds.extend(preds.tolist())
            all_labels.extend(y.tolist())

    acc = accuracy_score(all_labels, all_preds)
    cm = confusion_matrix(all_labels, all_preds)

    out = Path("outputs")
    out.mkdir(exist_ok=True)

    (out / "eval_metrics.json").write_text(
        json.dumps({"accuracy": acc}, indent=2)
    )

    fig, ax = plt.subplots()
    img = ax.imshow(cm, cmap="Blues")
    fig.colorbar(img, ax=ax)
    ax.set_title("Confusion Matrix")
    ax.set_xlabel("Predicted")
    ax.set_ylabel("True")
    fig.tight_layout()
    fig.savefig(out / "confusion_matrix.png")
    plt.close(fig)
    print(f"Accuracy: {acc:.4f}")


if __name__ == "__main__":
    evaluate()
"""

_TEST_SMOKE_PY = """\
def test_import_model():
    from src.model import SmallCNN

    model = SmallCNN()
    assert model is not None


def test_import_dataset():
    from src.dataset import FakeImageDataset

    ds = FakeImageDataset(n_samples=10)
    assert len(ds) == 10
"""

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def get_templates(project_name: str) -> dict[str, str]:
    n = project_name
    return {
        "README.md": _README.replace("{name}", n),
        "DATA.md": _DATA_MD,
        "requirements.txt": _REQUIREMENTS_TXT,
        "configs/default.yaml": _DEFAULT_YAML,
        "src/__init__.py": "",
        "src/dataset.py": _DATASET_PY,
        "src/model.py": _MODEL_PY,
        "src/utils.py": _UTILS_PY,
        "src/train.py": _TRAIN_PY,
        "src/eval.py": _EVAL_PY,
        "outputs/.gitkeep": "",
        "tests/__init__.py": "",
        "tests/test_smoke.py": _TEST_SMOKE_PY,
        "LICENSE": _MIT_LICENSE.replace("{name}", n),
        ".github/workflows/repropilot.yml": _REPROPILOT_YML,
    }
