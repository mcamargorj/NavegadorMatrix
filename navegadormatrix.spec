# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['navegadormatrix.py'],
    pathex=['/home/kali/vens/navegadormatrix/lib/python3.12/site-packages'],  # Adicione o caminho aqui
    binaries=[],
    
    datas=[('imagens/icon.png', 'imagens/')],


    hiddenimports=[
        'PyQt6',
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'PyQt6.QtWebEngineCore',
        'PyQt6.QtWebEngineWidgets',
        'platform',
        'distro',
        'pexpect',
        're'
    ],

    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='navegadormatrix',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='navegadormatrix',
)