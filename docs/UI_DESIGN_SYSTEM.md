# Modern UI Design System - Privacy Eraser

**Date:** 2025-10-20  
**Framework:** PySide6 (Qt6)  
**Status:** Production-Ready Reference

---

## 🎨 Design Philosophy

### Core Principles
1. **Simplicity First** - Minimize cognitive load, focus on essential features
2. **Consistency** - Uniform design language across all components
3. **Clarity** - Clear feedback, intuitive interactions, obvious hierarchy
4. **Performance** - Fast, responsive, smooth animations
5. **Accessibility** - Usable by everyone, including users with disabilities

### Design Values
- **Modern & Clean** - Contemporary aesthetics without clutter
- **Professional** - Production-ready, trustworthy appearance
- **User-Centric** - Designed around user workflows, not technology

---

## 🎯 Target Aesthetic

### Visual Style
- **Minimalist** - Clean lines, generous whitespace, focused content
- **Flat Design 2.0** - Subtle shadows for depth, minimal gradients
- **Material Inspired** - Elevation, cards, ripple effects (adapted for Qt)
- **Native Feel** - Respects platform conventions (Windows 11, macOS)

### Reference Applications
Modern desktop apps with excellent UI/UX:
- **Notion** - Clean, card-based layout, excellent typography
- **Slack** - Sidebar navigation, clear sections, consistent colors
- **VS Code** - Tabbed interface, panels, customizable theme
- **Spotify** - Dark theme done right, clear hierarchy, smooth navigation
- **Linear** - Modern, fast, minimalist issue tracker

---

## 🎨 Color System

### Primary Palette
```python
# Brand Colors
PRIMARY = "#2196F3"      # Blue - Main accent color
PRIMARY_DARK = "#1976D2" # Darker blue - Hover states
PRIMARY_LIGHT = "#BBDEFB"# Light blue - Backgrounds

# Semantic Colors
SUCCESS = "#4CAF50"      # Green - Success, completion
WARNING = "#FF9800"      # Orange - Warnings, caution
DANGER = "#F44336"       # Red - Errors, destructive actions
INFO = "#2196F3"         # Blue - Information, tips
```

### Neutral Palette
```python
# Light Theme
BACKGROUND = "#FFFFFF"   # Main background
SURFACE = "#F5F5F5"      # Cards, panels
BORDER = "#E0E0E0"       # Dividers, borders
TEXT_PRIMARY = "#212121" # Primary text
TEXT_SECONDARY = "#757575"# Secondary text, hints

# Dark Theme
BACKGROUND_DARK = "#121212"     # Main background
SURFACE_DARK = "#1E1E1E"        # Cards, panels
BORDER_DARK = "#2C2C2C"         # Dividers, borders
TEXT_PRIMARY_DARK = "#FFFFFF"   # Primary text
TEXT_SECONDARY_DARK = "#B0B0B0" # Secondary text
```

### Usage Guidelines
- **Primary** - Buttons, links, selected states, focus indicators
- **Success** - Completed actions, positive confirmations
- **Warning** - Reversible dangerous actions, important notices
- **Danger** - Irreversible actions, errors, critical warnings
- **Neutrals** - Text, backgrounds, borders, non-interactive elements

---

## 📐 Layout System

### Grid & Spacing
```python
# Base Unit: 8px (0.5rem)
SPACING_XS = 4   # 0.25rem - Compact spacing
SPACING_SM = 8   # 0.5rem  - Small spacing
SPACING_MD = 16  # 1rem    - Default spacing
SPACING_LG = 24  # 1.5rem  - Large spacing
SPACING_XL = 32  # 2rem    - Extra large spacing
SPACING_XXL = 48 # 3rem    - Section spacing

# Container Widths
SIDEBAR_WIDTH = 240      # Navigation sidebar
CONTENT_MAX_WIDTH = 1200 # Main content area
PANEL_WIDTH = 320        # Side panels
```

### Layout Patterns

#### 1. Sidebar + Main Content
```
┌─────────────────────────────────────────────┐
│ [Logo]  Sidebar     │ Main Content         │
│ ─────────────────   │                      │
│ □ Dashboard         │ [Header]             │
│ □ Browser Clean     │ ──────────────────   │
│ □ System Clean      │ [Content Area]       │
│ □ Schedules         │                      │
│ □ Statistics        │                      │
│ ─────────────────   │                      │
│ ⚙ Settings          │ [Footer]             │
└─────────────────────────────────────────────┘
```

#### 2. Card-Based Layout
```
┌─────────────────────────────────────────────┐
│ [Header]                                    │
├─────────────────────────────────────────────┤
│ ┌────────┐  ┌────────┐  ┌────────┐        │
│ │ Card 1 │  │ Card 2 │  │ Card 3 │        │
│ │        │  │        │  │        │        │
│ └────────┘  └────────┘  └────────┘        │
│ ┌────────────────────┐  ┌────────┐        │
│ │ Card 4 (wide)      │  │ Card 5 │        │
│ │                    │  │        │        │
│ └────────────────────┘  └────────┘        │
└─────────────────────────────────────────────┘
```

#### 3. Table/List View
```
┌─────────────────────────────────────────────┐
│ [Header + Controls]                         │
├─────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────┐ │
│ │ Name          Status      Action        │ │
│ ├─────────────────────────────────────────┤ │
│ │ Chrome        Installed   [Clean]       │ │
│ │ Firefox       Installed   [Clean]       │ │
│ │ Edge          Installed   [Clean]       │ │
│ └─────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

---

## 🔤 Typography

### Font Stack
```python
# Primary Font
FONT_FAMILY = "Segoe UI, -apple-system, system-ui, sans-serif"

# Monospace (for code, paths)
FONT_MONO = "Consolas, Monaco, Courier New, monospace"
```

### Type Scale
```python
# Font Sizes (pt)
FONT_XS = 10   # Captions, secondary info
FONT_SM = 11   # Body text (small)
FONT_MD = 12   # Body text (default)
FONT_LG = 14   # Subheadings
FONT_XL = 18   # Headings
FONT_XXL = 24  # Page titles
FONT_XXXL = 32 # Hero titles

# Font Weights
WEIGHT_LIGHT = 300
WEIGHT_REGULAR = 400
WEIGHT_MEDIUM = 500
WEIGHT_SEMIBOLD = 600
WEIGHT_BOLD = 700
```

### Typography Hierarchy
```python
# Title
QFont("Segoe UI", 24, QFont.Bold)

# Heading
QFont("Segoe UI", 18, QFont.Semibold)

# Subheading
QFont("Segoe UI", 14, QFont.Medium)

# Body
QFont("Segoe UI", 12, QFont.Normal)

# Caption
QFont("Segoe UI", 10, QFont.Normal)

# Code/Path
QFont("Consolas", 11, QFont.Normal)
```

---

## 🔘 Component Library

### Buttons

#### Primary Button
```python
# Large Primary Button
QPushButton {
    background-color: #2196F3;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 10px 20px;
    font-size: 12pt;
    font-weight: 500;
}
QPushButton:hover {
    background-color: #1976D2;
}
QPushButton:pressed {
    background-color: #1565C0;
}
QPushButton:disabled {
    background-color: #BDBDBD;
    color: #757575;
}
```

#### Secondary Button
```python
QPushButton {
    background-color: transparent;
    color: #2196F3;
    border: 2px solid #2196F3;
    border-radius: 4px;
    padding: 10px 20px;
    font-size: 12pt;
}
QPushButton:hover {
    background-color: rgba(33, 150, 243, 0.08);
}
```

#### Text Button
```python
QPushButton {
    background-color: transparent;
    color: #2196F3;
    border: none;
    padding: 8px 12px;
    font-size: 12pt;
}
QPushButton:hover {
    background-color: rgba(33, 150, 243, 0.08);
}
```

#### Danger Button
```python
QPushButton {
    background-color: #F44336;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 10px 20px;
}
QPushButton:hover {
    background-color: #D32F2F;
}
```

### Cards
```python
QFrame {
    background-color: white;
    border: 1px solid #E0E0E0;
    border-radius: 8px;
    padding: 16px;
}

# Card with shadow
QFrame {
    background-color: white;
    border: none;
    border-radius: 8px;
    padding: 16px;
}
QGraphicsDropShadowEffect {
    color: rgba(0, 0, 0, 0.1);
    blur-radius: 8px;
    offset: 0, 2px;
}
```

### Input Fields
```python
QLineEdit {
    background-color: #F5F5F5;
    border: 1px solid #E0E0E0;
    border-radius: 4px;
    padding: 8px 12px;
    font-size: 12pt;
}
QLineEdit:focus {
    border: 2px solid #2196F3;
    background-color: white;
}
QLineEdit:disabled {
    background-color: #FAFAFA;
    color: #9E9E9E;
}
```

### Checkboxes
```python
QCheckBox {
    spacing: 8px;
    font-size: 12pt;
}
QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 2px solid #757575;
    border-radius: 3px;
    background-color: white;
}
QCheckBox::indicator:checked {
    background-color: #2196F3;
    border-color: #2196F3;
    image: url(checkmark.svg);
}
QCheckBox::indicator:hover {
    border-color: #2196F3;
}
```

### Tables
```python
QTableWidget {
    background-color: white;
    border: 1px solid #E0E0E0;
    border-radius: 4px;
    gridline-color: #E0E0E0;
    font-size: 12pt;
}
QTableWidget::item {
    padding: 8px;
}
QTableWidget::item:selected {
    background-color: #E3F2FD;
    color: #1976D2;
}
QHeaderView::section {
    background-color: #F5F5F5;
    padding: 10px;
    border: none;
    border-bottom: 1px solid #E0E0E0;
    font-weight: 600;
}
```

### Tabs
```python
QTabWidget::pane {
    border: 1px solid #E0E0E0;
    border-radius: 4px;
    background-color: white;
}
QTabBar::tab {
    padding: 10px 20px;
    margin-right: 2px;
    font-size: 12pt;
    color: #757575;
}
QTabBar::tab:selected {
    background-color: white;
    color: #2196F3;
    border-bottom: 3px solid #2196F3;
}
QTabBar::tab:hover {
    color: #2196F3;
}
```

---

## 🎭 Icons & Graphics

### Icon Style
- **Outlined Icons** - Primary style, clean and modern
- **Size:** 16px, 20px, 24px, 32px (multiples of 4)
- **Color:** Inherit text color or use primary color
- **Source:** Material Icons, Feather Icons, or Lucide Icons

### Icon Usage
```python
# Icon in Button
button = QPushButton()
button.setIcon(QIcon("icons/clean.svg"))
button.setIconSize(QSize(20, 20))

# Icon in List Item
item = QListWidgetItem()
item.setIcon(QIcon("icons/browser.svg"))
```

### Recommended Icons
- **Actions:** clean (broom), scan (search), refresh (rotate)
- **Status:** success (check), warning (alert), error (x)
- **Navigation:** home, settings, help, info
- **Content:** browser, file, folder, trash
- **Controls:** play, pause, stop, edit, delete

---

## 🎬 Animations & Transitions

### Timing
```python
# Duration (milliseconds)
DURATION_FAST = 150    # Quick interactions
DURATION_NORMAL = 250  # Standard transitions
DURATION_SLOW = 400    # Complex animations

# Easing
EASE_IN_OUT = QEasingCurve.InOutCubic
EASE_OUT = QEasingCurve.OutCubic
EASE_IN = QEasingCurve.InCubic
```

### Common Animations
```python
# Fade In/Out
animation = QPropertyAnimation(widget, b"windowOpacity")
animation.setDuration(250)
animation.setStartValue(0.0)
animation.setEndValue(1.0)
animation.setEasingCurve(QEasingCurve.OutCubic)

# Slide In
animation = QPropertyAnimation(widget, b"geometry")
animation.setDuration(250)
animation.setStartValue(QRect(0, -100, 300, 100))
animation.setEndValue(QRect(0, 0, 300, 100))
animation.setEasingCurve(QEasingCurve.OutCubic)

# Scale (Bounce)
animation = QPropertyAnimation(widget, b"geometry")
animation.setDuration(150)
animation.setKeyValueAt(0.5, widget.geometry().scaled(1.1, 1.1))
animation.setEasingCurve(QEasingCurve.OutBounce)
```

### Usage Guidelines
- **Buttons** - Subtle color change on hover (no animation needed)
- **Panels** - Slide in/out when showing/hiding
- **Dialogs** - Fade in with slight scale up
- **Progress** - Smooth progress bar animation
- **Lists** - Fade in items when loading (stagger by 50ms)

---

## 📱 Responsive Design

### Window Sizes
```python
# Minimum Size
MIN_WIDTH = 800
MIN_HEIGHT = 600

# Default Size
DEFAULT_WIDTH = 1000
DEFAULT_HEIGHT = 700

# Maximum Size
MAX_WIDTH = 1600
MAX_HEIGHT = 1200
```

### Breakpoints
```python
COMPACT = 800   # Compact layout (hide sidebar, stack vertically)
MEDIUM = 1000   # Standard layout
LARGE = 1400    # Wide layout (show additional panels)
```

### Responsive Behavior
- **< 800px** - Single column, collapsible sidebar, mobile-like
- **800-1400px** - Standard layout, sidebar + content
- **> 1400px** - Wide layout, show additional panels/info

---

## ♿ Accessibility

### Keyboard Navigation
```python
# Tab Order
widget.setTabOrder(button1, button2)
widget.setTabOrder(button2, input1)

# Shortcuts
action = QAction("&Clean", self)
action.setShortcut("Ctrl+L")

# Focus Indicators (always visible)
QPushButton:focus {
    outline: 2px solid #2196F3;
    outline-offset: 2px;
}
```

### Screen Reader Support
```python
# Accessible Labels
button.setAccessibleName("Clean browser data")
button.setAccessibleDescription("Removes cache, cookies, and history")

# Status Announcements
widget.setAccessibleDescription("Cleaning in progress...")
```

### Color Contrast
- **Normal Text:** 4.5:1 minimum contrast ratio
- **Large Text:** 3:1 minimum contrast ratio
- **UI Components:** 3:1 minimum contrast ratio

---

## 🎨 Theme System

### Light Theme (Default)
```python
LIGHT_THEME = {
    "background": "#FFFFFF",
    "surface": "#F5F5F5",
    "primary": "#2196F3",
    "text_primary": "#212121",
    "text_secondary": "#757575",
    "border": "#E0E0E0",
}
```

### Dark Theme
```python
DARK_THEME = {
    "background": "#121212",
    "surface": "#1E1E1E",
    "primary": "#64B5F6",
    "text_primary": "#FFFFFF",
    "text_secondary": "#B0B0B0",
    "border": "#2C2C2C",
}
```

### Theme Implementation
```python
def apply_theme(app: QApplication, theme: str = "light"):
    if theme == "dark":
        palette = create_dark_palette()
    else:
        palette = create_light_palette()
    
    app.setPalette(palette)
    app.setStyleSheet(load_stylesheet(theme))
```

---

## 📋 Component Examples

### Example: Clean Button
```python
clean_button = QPushButton("Clean Now")
clean_button.setFont(QFont("Segoe UI", 12, QFont.Medium))
clean_button.setStyleSheet("""
    QPushButton {
        background-color: #2196F3;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 12px 24px;
    }
    QPushButton:hover {
        background-color: #1976D2;
    }
    QPushButton:pressed {
        background-color: #1565C0;
    }
""")
clean_button.setCursor(Qt.PointingHandCursor)
```

### Example: Status Card
```python
status_card = QFrame()
status_card.setFrameShape(QFrame.StyledPanel)
status_card.setStyleSheet("""
    QFrame {
        background-color: white;
        border: 1px solid #E0E0E0;
        border-radius: 8px;
        padding: 16px;
    }
""")

layout = QVBoxLayout(status_card)
title = QLabel("Last Clean")
title.setFont(QFont("Segoe UI", 14, QFont.Semibold))
value = QLabel("2 hours ago")
value.setFont(QFont("Segoe UI", 24, QFont.Bold))
value.setStyleSheet("color: #2196F3;")
layout.addWidget(title)
layout.addWidget(value)
```

---

## 🚀 Implementation Guide

### 1. Setup Base Styles
```python
# styles/base.qss
def load_base_stylesheet() -> str:
    return """
        * {
            font-family: "Segoe UI", -apple-system, system-ui, sans-serif;
            font-size: 12pt;
        }
        QMainWindow {
            background-color: #F5F5F5;
        }
        /* ... more base styles ... */
    """
```

### 2. Create Component Modules
```
src/privacy_eraser/ui/
├── components/
│   ├── buttons.py       # Button variants
│   ├── cards.py         # Card components
│   ├── inputs.py        # Input fields
│   └── tables.py        # Table components
├── styles/
│   ├── base.qss         # Base styles
│   ├── light.qss        # Light theme
│   └── dark.qss         # Dark theme
└── utils/
    ├── colors.py        # Color constants
    ├── spacing.py       # Spacing constants
    └── typography.py    # Font helpers
```

### 3. Use Design Tokens
```python
# ui/utils/colors.py
class Colors:
    PRIMARY = "#2196F3"
    PRIMARY_DARK = "#1976D2"
    SUCCESS = "#4CAF50"
    # ...

# ui/utils/spacing.py
class Spacing:
    XS = 4
    SM = 8
    MD = 16
    LG = 24
    XL = 32
```

### 4. Build Components
```python
# ui/components/buttons.py
class PrimaryButton(QPushButton):
    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self.setup_ui()
    
    def setup_ui(self):
        self.setFont(QFont("Segoe UI", 12, QFont.Medium))
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.PRIMARY};
                color: white;
                border: none;
                border-radius: 4px;
                padding: {Spacing.SM}px {Spacing.MD}px;
            }}
            QPushButton:hover {{
                background-color: {Colors.PRIMARY_DARK};
            }}
        """)
        self.setCursor(Qt.PointingHandCursor)
```

---

## 📚 Resources

### Design Inspiration
- **Material Design 3** - https://m3.material.io/
- **Apple Human Interface Guidelines** - https://developer.apple.com/design/
- **Fluent Design System** - https://fluent2.microsoft.design/
- **Atlassian Design System** - https://atlassian.design/

### Icon Libraries
- **Material Icons** - https://fonts.google.com/icons
- **Feather Icons** - https://feathericons.com/
- **Lucide Icons** - https://lucide.dev/
- **Phosphor Icons** - https://phosphoricons.com/

### Qt/PySide6 Resources
- **Qt Style Sheets** - https://doc.qt.io/qt-6/stylesheet.html
- **Qt Examples** - https://doc.qt.io/qt-6/examples.html
- **PySide6 Docs** - https://doc.qt.io/qtforpython-6/

### Color Tools
- **Coolors** - https://coolors.co/ (palette generator)
- **Contrast Checker** - https://webaim.org/resources/contrastchecker/
- **Material Color Tool** - https://material.io/resources/color/

---

## 🎯 Next Steps

1. **Review existing GUI** - `src/privacy_eraser/gui.py`
2. **Refactor to PySide6** - Migrate from CustomTkinter
3. **Apply design system** - Use colors, typography, components
4. **Create component library** - Reusable UI components
5. **Build modern layouts** - Implement sidebar + content pattern
6. **Add animations** - Smooth transitions for better UX
7. **Test accessibility** - Keyboard nav, screen readers, contrast

---

**Status:** ✅ Ready for Implementation  
**Framework:** PySide6 (Qt6)  
**Target:** Modern, Simple, Production-Ready UI

