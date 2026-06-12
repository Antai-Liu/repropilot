def test_import_model():
    from src.model import SmallCNN

    model = SmallCNN()
    assert model is not None


def test_import_dataset():
    from src.dataset import FakeImageDataset

    ds = FakeImageDataset(n_samples=10)
    assert len(ds) == 10
