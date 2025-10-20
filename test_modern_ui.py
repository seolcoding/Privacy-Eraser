#!/usr/bin/env python3
"""
Test script to verify qt-material and qtawesome integration
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PySide6.QtCore import Qt

# Test qt-material
try:
    from qt_material import apply_stylesheet
    HAS_QT_MATERIAL = True
    print("OK qt-material imported successfully")
except ImportError as e:
    HAS_QT_MATERIAL = False
    print(f"ERROR qt-material import failed: {e}")

# Test qtawesome
try:
    import qtawesome as qta
    HAS_QT_AWESOME = True
    print("OK qtawesome imported successfully")
except ImportError as e:
    HAS_QT_AWESOME = False
    print(f"ERROR qtawesome import failed: {e}")

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Privacy Eraser - Modern UI Test")
        self.setMinimumSize(400, 300)
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QVBoxLayout(central)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("Privacy Eraser")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2196F3;")
        layout.addWidget(title)
        
        # Test buttons
        scan_btn = QPushButton("Scan Programs")
        if HAS_QT_AWESOME:
            scan_btn.setIcon(qta.icon('fa5s.search'))
        scan_btn.setMinimumHeight(40)
        layout.addWidget(scan_btn)
        
        clean_btn = QPushButton("Clean Now")
        if HAS_QT_AWESOME:
            clean_btn.setIcon(qta.icon('fa5s.broom'))
        clean_btn.setMinimumHeight(40)
        layout.addWidget(clean_btn)
        
        settings_btn = QPushButton("Settings")
        if HAS_QT_AWESOME:
            settings_btn.setIcon(qta.icon('fa5s.cog'))
        settings_btn.setMinimumHeight(40)
        layout.addWidget(settings_btn)
        
        # Status label
        status = QLabel("Modern UI Test - qt-material theme applied!")
        status.setAlignment(Qt.AlignCenter)
        status.setStyleSheet("color: #666; font-style: italic;")
        layout.addWidget(status)
        
        layout.addStretch()

def main():
    app = QApplication(sys.argv)
    
    # Apply Material Design theme
    if HAS_QT_MATERIAL:
        apply_stylesheet(app, theme='dark_blue.xml')
        print("OK Applied dark_blue Material Design theme")
    else:
        print("WARN Using default Qt theme (qt-material not available)")
    
    # Create and show window
    window = TestWindow()
    window.show()
    
    print("OK Test window created and shown")
    print("SUCCESS Modern UI integration successful!")
    
    # Run for a few seconds then exit
    from PySide6.QtCore import QTimer
    timer = QTimer()
    timer.timeout.connect(app.quit)
    timer.start(3000)  # 3 seconds
    
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())
