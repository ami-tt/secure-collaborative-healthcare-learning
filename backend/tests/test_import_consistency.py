def test_no_backend_app_modules_loaded():
    """Ensure the test suite does not import any module with the
    ``backend.app.`` prefix, confirming a single import namespace.
    """
    import sys
    backend_modules = [m for m in sys.modules if m.startswith("backend.app.")]
    assert not backend_modules, f"Unexpected modules loaded: {backend_modules}"
