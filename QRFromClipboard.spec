# -*- mode: python ; coding: utf-8 -*-
# QRFromClipboard.spec - PyInstaller Konfiguration für PyQt6 QR-App

import os
from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

# Analyse - alle Abhängigkeiten finden
a = Analysis(
    ['main.py'],                             # Einstiegspunkt
    pathex=[],                               # Leerer Pfad (aktuelles Verzeichnis)
    binaries=[],
    datas=[
        ('icon.ico', '.'),                    # Icon falls vorhanden
        # Füge weitere Dateien hier hinzu:
        # ('ui/*.ui', 'ui'),
        # ('images/*', 'images')
    ],
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtGui', 
        'PyQt6.QtWidgets',
        'PIL._tkinter_finder',                # Pillow Fix
        'qrcode', 
        'qrcode.constants'
    ],
    hookspath=[]:
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',                            # Nicht benötigt
        'matplotlib',
        'numpy'                               # Falls nicht verwendet
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Python-Archive (komprimiert)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# EXE für Windows (GUI-App ohne Konsole)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='QRFromClipboard',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,                                 # UPX-Kompression (optional)
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,                            # Kein Konsolenfenster
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico'                           # App-Icon
)
