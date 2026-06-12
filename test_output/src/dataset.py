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
