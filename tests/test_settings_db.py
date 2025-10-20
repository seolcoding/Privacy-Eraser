from __future__ import annotations

import tempfile
from pathlib import Path

import pytest


def test_settings_db_crud(monkeypatch):
    """Test settings database CRUD operations."""
    # Use a temp DB for testing
    with tempfile.TemporaryDirectory() as tmpdir:
        test_db = Path(tmpdir) / "test_settings.db"
        
        from privacy_eraser import settings_db
        
        # Monkeypatch the DB path
        monkeypatch.setattr(settings_db, "DB_PATH", test_db)
        
        # Initialize DB
        settings_db.init_settings_db()
        assert test_db.exists()
        
        # Save setting
        settings_db.save_setting("ui_mode", "advanced")
        settings_db.save_setting("appearance_mode", "dark")
        
        # Load setting
        assert settings_db.load_setting("ui_mode") == "advanced"
        assert settings_db.load_setting("appearance_mode") == "dark"
        assert settings_db.load_setting("nonexistent", "default") == "default"
        
        # Update existing
        settings_db.save_setting("ui_mode", "easy")
        assert settings_db.load_setting("ui_mode") == "easy"


def test_settings_db_default():
    """Test settings database returns default for missing keys."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_db = Path(tmpdir) / "test_settings2.db"
        
        from privacy_eraser import settings_db
        import importlib
        
        # Reload module to reset state
        importlib.reload(settings_db)
        
        # Monkeypatch
        original_path = settings_db.DB_PATH
        settings_db.DB_PATH = test_db
        
        try:
            settings_db.init_settings_db()
            
            # Missing key returns default
            assert settings_db.load_setting("missing_key", "my_default") == "my_default"
        finally:
            settings_db.DB_PATH = original_path

