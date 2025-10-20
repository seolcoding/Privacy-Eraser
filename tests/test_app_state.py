from __future__ import annotations


def test_app_state_defaults():
    """Test app_state has correct default values."""
    from privacy_eraser.app_state import app_state
    
    # Reset state to defaults for test
    app_state.ui_mode = "easy"
    app_state.debug_enabled = False
    app_state.appearance_mode = "system"
    app_state.wizard_step = 0
    app_state.wizard_selected_browsers = []
    app_state.active_browser = None
    app_state.scanned_programs = []
    
    assert app_state.ui_mode == "easy"
    assert app_state.debug_enabled is False
    assert app_state.appearance_mode == "system"
    assert app_state.wizard_step == 0
    assert app_state.wizard_selected_browsers == []
    assert app_state.active_browser is None
    assert app_state.scanned_programs == []


def test_app_state_mutation():
    """Test app_state can be mutated."""
    from privacy_eraser.app_state import app_state
    
    # Mutate
    app_state.ui_mode = "advanced"
    app_state.wizard_step = 2
    app_state.scanned_programs = [{"name": "Chrome"}]
    
    assert app_state.ui_mode == "advanced"
    assert app_state.wizard_step == 2
    assert len(app_state.scanned_programs) == 1
    
    # Reset for other tests
    app_state.ui_mode = "easy"
    app_state.wizard_step = 0
    app_state.scanned_programs = []


def test_switch_ui_mode():
    """Test switch_ui_mode function changes app_state."""
    from privacy_eraser.gui import switch_ui_mode
    from privacy_eraser.app_state import app_state
    
    # Test switching to advanced
    switch_ui_mode("advanced")
    assert app_state.ui_mode == "advanced"
    
    # Test switching to easy
    switch_ui_mode("easy")
    assert app_state.ui_mode == "easy"
    
    # Test normalization
    switch_ui_mode("adv")  # Should normalize to "advanced"
    assert app_state.ui_mode == "advanced"
    
    switch_ui_mode("anything_else")  # Should default to "easy"
    assert app_state.ui_mode == "easy"


def test_app_state_signals():
    """Test app_state emits Qt signals on property changes."""
    from privacy_eraser.app_state import app_state
    
    # Track signal emissions
    ui_mode_changes = []
    wizard_step_changes = []
    
    def on_ui_mode_changed(mode):
        ui_mode_changes.append(mode)
    
    def on_wizard_step_changed(step):
        wizard_step_changes.append(step)
    
    # Connect signals
    app_state.ui_mode_changed.connect(on_ui_mode_changed)
    app_state.wizard_step_changed.connect(on_wizard_step_changed)
    
    # Change properties
    app_state.ui_mode = "advanced"
    app_state.wizard_step = 1
    
    # Verify signals were emitted
    assert "advanced" in ui_mode_changes
    assert 1 in wizard_step_changes
    
    # Cleanup
    app_state.ui_mode_changed.disconnect(on_ui_mode_changed)
    app_state.wizard_step_changed.disconnect(on_wizard_step_changed)
    
    # Reset
    app_state.ui_mode = "easy"
    app_state.wizard_step = 0
