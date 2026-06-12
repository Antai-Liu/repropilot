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
