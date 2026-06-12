# test_output

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
