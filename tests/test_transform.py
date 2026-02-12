def test_transform_module_importable():
    import importlib

    mod = importlib.import_module("src.transform.feature_pipeline")
    assert hasattr(mod, "build_features")
