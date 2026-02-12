def test_train_module_importable():
    import importlib

    mod = importlib.import_module("src.models.train")
    assert hasattr(mod, "train_model")
