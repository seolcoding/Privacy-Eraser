"""Privacy Eraser - Entry point for Flet build"""

import sys
from pathlib import Path

# Add src directory to Python path for Flet build
src_path = Path(__file__).parent / "src"
if src_path.exists():
    sys.path.insert(0, str(src_path))

from privacy_eraser.poc.flet_main import main_entry

if __name__ == "__main__":
    main_entry()
