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
