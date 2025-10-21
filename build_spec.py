# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Privacy Eraser POC

Builds a single-file Windows executable with all dependencies embedded.

Usage:
    pyinstaller build_spec.py
"""

from PyInstaller.utils.hooks import collect_data_files, collect_submodules
import sys
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent
SRC_PATH = PROJECT_ROOT / "src"

# Entry point script
entry_script = str(SRC_PATH / "privacy_eraser" / "poc" / "main.py")

# Collect all PySide6 modules
pyside6_modules = collect_submodules('PySide6')

# Collect data files
datas = []
datas += collect_data_files('qt_material')  # Qt Material theme files
datas += collect_data_files('qtawesome')    # Font Awesome icons

# Hidden imports (modules not automatically detected)
hidden_imports = [
    'PySide6.QtCore',
    'PySide6.QtWidgets',
    'PySide6.QtGui',
    'qtawesome',
    'qtawesome.iconic_font',
    'loguru',
    'privacy_eraser.detect_windows',
    'privacy_eraser.poc.core.browser_info',
    'privacy_eraser.poc.core.data_config',
    'privacy_eraser.poc.core.poc_cleaner',
    'privacy_eraser.poc.core.backup_manager',
    'privacy_eraser.poc.ui.main_window',
    'privacy_eraser.poc.ui.browser_card',
    'privacy_eraser.poc.ui.progress_dialog',
    'privacy_eraser.poc.ui.undo_dialog',
    'privacy_eraser.poc.ui.styles',
] + pyside6_modules

a = Analysis(
    [entry_script],
    pathex=[str(SRC_PATH)],
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'PyQt5',
        'tkinter',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PrivacyEraser',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window (GUI app)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='file_version_info.txt',  # Will be created if exists
    icon=None,  # TODO: Add icon file later
)
