# Secure Collaborative Healthcare Learning System - Backend App Package

# Ensure that importing via the legacy "backend.app" namespace
# returns the same module objects as the canonical "app" namespace.
# This avoids duplicate SQLAlchemy declarative base registrations.
import importlib, sys
_main_pkg = importlib.import_module('app')
# Alias the top-level package
sys.modules[__name__] = _main_pkg
# Alias submodules lazily when accessed
def __getattr__(name):
    return getattr(_main_pkg, name)
