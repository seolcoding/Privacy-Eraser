# Quick UI Upgrade Guide - Add Modern Design in 5 Minutes

**Goal:** Upgrade Privacy Eraser to modern Material Design look with minimal code changes

---

## ⚡ Quick Start (5 Minutes)

### Step 1: Install qt-material
```bash
cd d:/priv
uv pip install qt-material
```

### Step 2: Update Your GUI Code

Add **just 2 lines** to your existing GUI:

```python
# src/privacy_eraser/gui.py (or wherever your GUI starts)

from PySide6.QtWidgets import QApplication
from qt_material import apply_stylesheet  # ← ADD THIS

def run_gui():
    app = QApplication([])
    
    # ADD THIS LINE - that's it!
    apply_stylesheet(app, theme='dark_blue.xml')
    
    # Your existing code continues...
    window = create_main_window()
    window.show()
    app.exec()
```

### Step 3: Run and See!
```bash
uv run privacy_eraser
```

**Result:** Instant modern Material Design UI! 🎉

---

## 🎨 Available Themes

Try different themes by changing the theme parameter:

```python
# Dark themes (recommended for privacy tools)
apply_stylesheet(app, theme='dark_blue.xml')      # ← Recommended
apply_stylesheet(app, theme='dark_teal.xml')
apply_stylesheet(app, theme='dark_cyan.xml')
apply_stylesheet(app, theme='dark_purple.xml')

# Light themes
apply_stylesheet(app, theme='light_blue.xml')
apply_stylesheet(app, theme='light_cyan.xml')
```

---

## 🎯 Next Level (Optional)

### Add Icons (Material Design Icons)

```bash
uv pip install qtawesome
```

```python
import qtawesome as qta

# Add icons to buttons
scan_btn.setIcon(qta.icon('fa5s.search'))
clean_btn.setIcon(qta.icon('fa5s.broom'))
settings_btn.setIcon(qta.icon('fa5s.cog'))
```

### Add Theme Switcher

```python
# Create theme selector in settings
from qt_material import list_themes

themes = list_themes()
for theme in themes:
    combo_box.addItem(theme)

def on_theme_change(theme):
    apply_stylesheet(app, theme=theme)
```

---

## 📊 Before & After

**Before (Default Qt):**
```
┌────────────────────────────┐
│ Privacy Eraser             │  ← Plain gray
├────────────────────────────┤
│ [Scan]  [Clean]            │  ← Basic buttons
└────────────────────────────┘
```

**After (qt-material):**
```
┌────────────────────────────┐
│ 🛡️ Privacy Eraser          │  ← Modern blue
├────────────────────────────┤
│ [Scan] 🔍  [Clean] 🧹      │  ← Colored buttons with hover
│ ─────────────────────────  │  ← Clean lines
│ [Card-style content]       │  ← Material cards
└────────────────────────────┘
```

---

## ✅ Why This Works

- **Zero breaking changes** - works with existing code
- **Professional look** - Material Design is industry standard
- **Free & open source** - BSD license
- **5 minutes to implement** - literally 2 lines of code
- **Instant upgrade** - users will notice immediately

---

## 🚀 Ready to Go?

Just run:
```bash
uv pip install qt-material
```

Then add this to your GUI startup:
```python
from qt_material import apply_stylesheet
apply_stylesheet(app, theme='dark_blue.xml')
```

Done! 🎉

