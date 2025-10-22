"""Generate Test Data for Development Mode

Creates dummy browser data files in test_data/ directory
to simulate real browser cache, cookies, history files.

Usage:
    python scripts/generate_test_data.py
"""

from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from privacy_eraser.dev_data_generator import generate_all_test_data
from privacy_eraser.config import TEST_DATA_DIR
from loguru import logger


def main():
    """Main entry point"""
    logger.info("=" * 60)
    logger.info("Privacy Eraser - Test Data Generator")
    logger.info("=" * 60)
    logger.info(f"Test data directory: {TEST_DATA_DIR}")

    # Generate test data (force regenerate)
    result = generate_all_test_data(force=True)

    # Summary
    logger.info("=" * 60)
    if result["skipped"]:
        logger.info("Test data already exists (use force=True to regenerate)")
    else:
        logger.success("✅ Test data generation complete!")
        logger.info(f"Total files: {result['total_files']}")
        logger.info(f"Total size: {result['total_size_mb']:.2f} MB")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
