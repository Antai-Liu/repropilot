# Dataset

## Default (dummy data)

`src/dataset.py` generates random tensors via `torch.randn`.
No download is required; labels are assigned randomly.

## Using a real dataset

1. Download your dataset (e.g. FaceForensics++, DFDC).
2. Organise images into `data/real/` and `data/fake/` subfolders.
3. Update `FakeImageDataset` in `src/dataset.py` to read from disk.
4. Set `data_path` in `configs/default.yaml` to point at `data/`.
