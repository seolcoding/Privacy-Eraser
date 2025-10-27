"""Privacy Eraser - Entry point for Flet build

This file is required in the project root for Flet build to work properly.
It imports and runs the main UI from src/privacy_eraser/ui/main.py
"""

import sys
from pathlib import Path

# Add src to Python path so imports work
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from privacy_eraser.ui.main import main_entry

if __name__ == "__main__":
    main_entry()
