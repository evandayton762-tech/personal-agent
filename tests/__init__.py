"""Test package initializer.

This file adjusts the Python path so that the ``orchestrator`` and
``runner_windows`` modules can be imported when tests are run via
``python -m unittest discover``. Without this file, the test discovery
mechanism may fail to locate modules in the project root.
"""

import os
import sys

# Ensure the project root (one level up from this directory) is on sys.path
current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, os.pardir))
if project_root not in sys.path:
    sys.path.insert(0, project_root)