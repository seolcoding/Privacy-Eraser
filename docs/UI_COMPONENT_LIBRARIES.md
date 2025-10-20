# Pre-Built Qt Component Libraries & Design Systems

**Date:** 2025-10-20  
**Purpose:** Reference guide for modern, pre-built UI component libraries for Qt/PySide6

---

## 🎨 Overview

Yes! There are several excellent pre-built component libraries for Qt/PySide6, similar to Material UI or Tailwind CSS for web development. These provide ready-to-use, modern components that can significantly speed up UI development.

---

## 📦 Top Recommended Libraries

### 1. **qt-material** ⭐ Recommended

**Description:** Material Design styling for Qt/PySide6 applications

**Repository:** https://github.com/UN-GCPDS/qt-material  
**PyPI:** `qt-material`  
**License:** BSD-2-Clause  
**Stars:** ~1.1k on GitHub

**Features:**
- ✅ Material Design 3 theming
- ✅ Dark/Light themes with many color variants
- ✅ Works with both PyQt5/6 and PySide2/6
- ✅ Simple one-line theme application
- ✅ Pre-built Material Design components
- ✅ Custom theme builder
- ✅ Icon support (Material Design Icons)

**Installation:**
```bash
uv pip install qt-material
```

**Usage:**
```python
from PySide6.QtWidgets import QApplication, QMainWindow
from qt_material import apply_stylesheet

app = QApplication([])
window = QMainWindow()

# Apply Material Design theme
apply_stylesheet(app, theme='dark_blue.xml')
# Or: 'light_blue.xml', 'dark_teal.xml', 'light_pink.xml', etc.

window.show()
app.exec()
```

**Available Themes:**
- `dark_amber.xml`, `dark_blue.xml`, `dark_cyan.xml`, `dark_lightgreen.xml`
- `dark_pink.xml`, `dark_purple.xml`, `dark_red.xml`, `dark_teal.xml`, `dark_yellow.xml`
- `light_amber.xml`, `light_blue.xml`, `light_cyan.xml`, `light_lightgreen.xml`
- `light_pink.xml`, `light_purple.xml`, `light_red.xml`, `light_teal.xml`, `light_yellow.xml`

**Pros:**
- ✅ Easy to use (one-line setup)
- ✅ Professional Material Design look
- ✅ Many built-in themes
- ✅ Active development
- ✅ Compatible with PySide6

**Cons:**
- ⚠️ Limited to Material Design style
- ⚠️ Customization requires XML editing

---

### 2. **PyQt-Fluent-Widgets** 🔥 Most Modern

**Description:** Microsoft Fluent Design component library for PyQt/PySide

**Repository:** https://github.com/zhiyiYo/PyQt-Fluent-Widgets  
**PyPI:** `PyQt6-Fluent-Widgets` or `PySide6-Fluent-Widgets`  
**License:** GPLv3 (Free) / Commercial available  
**Stars:** ~4.5k on GitHub

**Features:**
- ✅ Microsoft Fluent Design System
- ✅ 200+ beautiful, modern components
- ✅ Acrylic/Mica effects (Windows 11 style)
- ✅ Dark/Light themes
- ✅ Smooth animations
- ✅ Icon library included
- ✅ Navigation components (Sidebar, Tabs, etc.)
- ✅ Modern controls (Cards, Badges, etc.)
- ✅ Excellent documentation

**Installation:**
```bash
# For PySide6
uv pip install PySide6-Fluent-Widgets[full]
```

**Usage:**
```python
from PySide6.QtWidgets import QApplication
from qfluentwidgets import FluentWindow, NavigationItemPosition

class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Privacy Eraser")
        
        # Add navigation items
        self.addSubInterface(dashboard, FluentIcon.HOME, "Dashboard")
        self.addSubInterface(browser_clean, FluentIcon.BROOM, "Browser Clean")

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
```

**Components Include:**
- **Navigation:** FluentWindow, NavigationInterface, Pivot, SegmentedWidget
- **Buttons:** PrimaryPushButton, HyperlinkButton, DropDownPushButton
- **Input:** LineEdit, SearchLineEdit, PasswordLineEdit, ComboBox
- **Lists:** ListView, TableWidget, TreeWidget
- **Cards:** CardWidget, ElevatedCardWidget, SimpleCardWidget
- **Dialogs:** MessageBox, Dialog, FlyoutView
- **Indicators:** ProgressBar, ProgressRing, IndeterminateProgressBar
- **Layout:** FlowLayout, VBoxLayout, HBoxLayout
- **Status:** InfoBar, StateToolTip, Badge

**Pros:**
- ✅ Most comprehensive library (200+ components)
- ✅ Modern Windows 11 style
- ✅ Excellent documentation with examples
- ✅ Very active development
- ✅ Beautiful animations
- ✅ Production-ready

**Cons:**
- ⚠️ GPLv3 license (commercial license required for proprietary apps)
- ⚠️ Larger package size
- ⚠️ Primarily designed for Windows (best on Win11)

---

### 3. **Qt Quick Controls 2** (Built-in)

**Description:** Official Qt component library with Material Design style

**Documentation:** https://doc.qt.io/qt-6/qtquickcontrols-index.html  
**License:** LGPL/Commercial  
**Included:** With Qt/PySide6 installation

**Features:**
- ✅ Official Qt solution
- ✅ Material Design style available
- ✅ Cross-platform native look
- ✅ QML-based (declarative UI)
- ✅ Highly performant
- ✅ Well-documented

**Note:** Requires QML (not pure Python/Qt Widgets)

**Usage:**
```qml
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15

ApplicationWindow {
    Material.theme: Material.Dark
    Material.accent: Material.Blue
    
    Button {
        text: "Clean Now"
        Material.background: Material.Blue
    }
}
```

**Pros:**
- ✅ Official Qt solution
- ✅ Best performance
- ✅ Material Design built-in
- ✅ Free (LGPL)

**Cons:**
- ⚠️ Requires learning QML
- ⚠️ Different paradigm from Qt Widgets
- ⚠️ Mixing QML + Widgets can be complex

---

### 4. **PyQt5-Frameless-Window** / **PyQt-Frameless-Window**

**Description:** Frameless window with custom title bar (modern Windows 11 style)

**Repository:** https://github.com/zhiyiYo/PyQt-Frameless-Window  
**PyPI:** `PyQt5-Frameless-Window`, `PyQt6-Frameless-Window`, `PySide6-Frameless-Window`  
**License:** GPLv3  

**Features:**
- ✅ Modern frameless window
- ✅ Custom title bar
- ✅ Window effects (Acrylic, Mica)
- ✅ Snap layouts (Windows 11)
- ✅ Dark/Light title bar

**Installation:**
```bash
uv pip install PySide6-Frameless-Window
```

**Pros:**
- ✅ Modern Windows 11 appearance
- ✅ Easy to integrate
- ✅ Small footprint

**Cons:**
- ⚠️ Only provides window frame (not full component library)
- ⚠️ Windows-focused

---

## 🎯 Comparison & Recommendations

### For Privacy Eraser Project

| Library | Best For | Complexity | Modern Look | License | Recommendation |
|---------|----------|------------|-------------|---------|----------------|
| **qt-material** | Quick Material Design | ⭐ Easy | ⭐⭐⭐⭐ | BSD (Free) | ✅ **Best for MVP** |
| **PyQt-Fluent-Widgets** | Production App | ⭐⭐ Medium | ⭐⭐⭐⭐⭐ | GPLv3/Commercial | ✅ **Best for Final Product** |
| **Qt Quick Controls** | QML Projects | ⭐⭐⭐ Hard | ⭐⭐⭐⭐ | LGPL (Free) | ⚠️ Different paradigm |
| **Custom (Our template)** | Full Control | ⭐⭐⭐ Hard | ⭐⭐⭐ | Your choice | ✅ **Most flexible** |

---

## 🚀 Recommended Approach for Privacy Eraser

### Phase 1: MVP (Quick Start) - Use `qt-material`

**Why:**
- ✅ Fastest to implement (1-2 hours)
- ✅ Professional Material Design look
- ✅ BSD license (no restrictions)
- ✅ Works with existing Qt Widgets code

**Implementation:**
```python
# src/privacy_eraser/ui/app.py
from PySide6.QtWidgets import QApplication, QMainWindow
from qt_material import apply_stylesheet

def run_app():
    app = QApplication([])
    
    # Apply Material Design theme
    apply_stylesheet(app, theme='dark_blue.xml')
    
    # Your existing window code
    window = MainWindow()
    window.show()
    
    app.exec()
```

**Time to implement:** 1-2 hours  
**Result:** Instant modern look with minimal code changes

---

### Phase 2: Production (Premium) - Use `PyQt-Fluent-Widgets`

**Why:**
- ✅ Most modern and beautiful
- ✅ 200+ pre-built components
- ✅ Windows 11 native look
- ✅ Comprehensive navigation system
- ✅ Best for commercial product

**Implementation:**
```python
# src/privacy_eraser/ui/main_window.py
from PySide6.QtCore import Qt
from qfluentwidgets import FluentWindow, FluentIcon, NavigationItemPosition
from qfluentwidgets import setTheme, Theme

class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Privacy Eraser")
        
        # Set theme
        setTheme(Theme.DARK)
        
        # Add sub-interfaces with navigation
        self.homeInterface = HomeInterface(self)
        self.browserInterface = BrowserCleanInterface(self)
        self.systemInterface = SystemCleanInterface(self)
        
        self.addSubInterface(self.homeInterface, FluentIcon.HOME, "Dashboard")
        self.addSubInterface(self.browserInterface, FluentIcon.BROOM, "Browser Clean")
        self.addSubInterface(self.systemInterface, FluentIcon.SETTING, "System Clean")
        
        # Add settings to bottom
        self.addSubInterface(
            self.settingsInterface, 
            FluentIcon.SETTING, 
            "Settings",
            NavigationItemPosition.BOTTOM
        )
```

**Time to implement:** 1-2 weeks (full migration)  
**Result:** Production-ready, premium UI

**License Note:** GPLv3 (open-source OK) or purchase commercial license (~$200-500) for proprietary distribution

---

## 📚 Installation & Setup Guide

### Option 1: qt-material (Quick Start)

```bash
# Install qt-material
uv pip install qt-material

# Optional: Install Material Design Icons
uv pip install qtawesome
```

**Minimal Example:**
```python
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from qt_material import apply_stylesheet

app = QApplication([])

# Create simple window
window = QMainWindow()
window.setWindowTitle("Privacy Eraser")

central = QWidget()
layout = QVBoxLayout(central)
layout.addWidget(QPushButton("Scan Browsers"))
layout.addWidget(QPushButton("Clean Now"))
window.setCentralWidget(central)

# Apply Material Design theme
apply_stylesheet(app, theme='dark_blue.xml')

window.show()
app.exec()
```

---

### Option 2: PyQt-Fluent-Widgets (Production)

```bash
# Install PySide6-Fluent-Widgets
uv pip install PySide6-Fluent-Widgets[full]
```

**Minimal Example:**
```python
from PySide6.QtWidgets import QApplication
from qfluentwidgets import FluentWindow, PrimaryPushButton, setTheme, Theme

class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        setTheme(Theme.DARK)
        
        # Add a primary button
        button = PrimaryPushButton("Clean Now", self)
        button.clicked.connect(self.on_clean)
    
    def on_clean(self):
        print("Cleaning...")

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
```

---

## 🎨 Visual Comparison

### qt-material
```
┌─────────────────────────────────────────┐
│ Material Design Blue Theme              │
├─────────────────────────────────────────┤
│ [────────────────────]  Search          │
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ Browser Clean                       │ │
│ │                                     │ │
│ │ [Scan Browsers]  [Clean Now]        │ │
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```
**Style:** Google Material Design (Cards, Shadows, Colors)

### PyQt-Fluent-Widgets
```
┌─────────────────────────────────────────┐
│ ☰  Privacy Eraser              🔍 ⚙     │
├─────────────────────────────────────────┤
│ 🏠 Dashboard                            │
│ 🧹 Browser Clean     ← Active           │
│ ⚙️  System Clean                        │
│                                         │
│ Clean browser data                      │
│ Remove cache, cookies, and history      │
│                                         │
│ [Scan Browsers]  [Clean Now]            │
└─────────────────────────────────────────┘
```
**Style:** Microsoft Fluent (Acrylic, Rounded, Navigation)

---

## 💡 Final Recommendation

### For Privacy Eraser:

**Immediate (Next Sprint):**
1. **Install `qt-material`** for instant modern look
2. **Apply dark_blue.xml theme** to existing GUI
3. **Test with current Qt Widgets code**
4. **Estimated time:** 2-3 hours

**Future (v2.0):**
1. **Evaluate `PyQt-Fluent-Widgets`** for premium version
2. **Design with navigation sidebar** (dashboard, browser, system)
3. **Use Fluent components** (Cards, Badges, etc.)
4. **Estimated time:** 1-2 weeks full migration

**Hybrid Approach:**
- Use `qt-material` for base theming
- Add custom components from our template where needed
- Consider `PyQt-Fluent-Widgets` for premium/commercial version

---

## 📦 Quick Integration Script

```python
# src/privacy_eraser/ui/theme.py
"""Theme management for Privacy Eraser"""

from PySide6.QtWidgets import QApplication
from qt_material import apply_stylesheet
import os

AVAILABLE_THEMES = [
    'dark_blue.xml',
    'dark_teal.xml',
    'light_blue.xml',
    'light_cyan.xml',
]

def apply_modern_theme(app: QApplication, theme: str = 'dark_blue.xml'):
    """Apply modern Material Design theme to application"""
    try:
        apply_stylesheet(app, theme=theme)
        print(f"Applied theme: {theme}")
    except Exception as e:
        print(f"Failed to apply theme: {e}")
        print("Using default Qt theme")

def list_available_themes() -> list[str]:
    """Get list of available themes"""
    return AVAILABLE_THEMES
```

**Usage in your main GUI:**
```python
# src/privacy_eraser/gui.py
from PySide6.QtWidgets import QApplication
from .ui.theme import apply_modern_theme

def run_gui():
    app = QApplication([])
    
    # Apply modern theme
    apply_modern_theme(app, theme='dark_blue.xml')
    
    # Your existing window code
    window = create_main_window()
    window.show()
    
    app.exec()
```

---

## 🔗 Resources

- **qt-material GitHub:** https://github.com/UN-GCPDS/qt-material
- **PyQt-Fluent-Widgets GitHub:** https://github.com/zhiyiYo/PyQt-Fluent-Widgets
- **PyQt-Fluent-Widgets Docs:** https://pyqt-fluent-widgets.readthedocs.io/
- **Qt Style Sheets Reference:** https://doc.qt.io/qt-6/stylesheet-reference.html
- **Material Design Guidelines:** https://m3.material.io/

---

**Status:** ✅ Ready to integrate  
**Recommended:** Start with `qt-material`, upgrade to `PyQt-Fluent-Widgets` for v2.0

