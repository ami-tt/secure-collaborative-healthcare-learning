import os, sys, pkgutil

# Determine the path to the actual backend app package
_current_dir = os.path.abspath(os.path.dirname(__file__))
root_dir = os.path.abspath(os.path.join(_current_dir, '..'))
_backend_app_path = os.path.join(root_dir, 'backend', 'app')

# Ensure the path exists
if os.path.isdir(_backend_app_path):
    # Prepend to sys.path so that imports resolve correctly
    if _backend_app_path not in sys.path:
        sys.path.insert(0, _backend_app_path)
    # Make this a namespace package that points to the backend app directory
    __path__ = [_backend_app_path]
else:
    # Fallback to default package behavior
    __path__ = pkgutil.extend_path(__path__, __name__)
