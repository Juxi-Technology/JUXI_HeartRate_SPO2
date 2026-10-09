# -*- mode: python ; coding: utf-8 -*-
# 单文件打包（onefile）：构建结果只有 dist/HeartRateOximeter.exe 一个文件
# 如需改回文件夹模式（onedir），把 EXE 的 a.binaries, a.datas 移到 COLLECT 并恢复 exclude_binaries=True


a = Analysis(
    ['上位机源代码/HeartRateOximeter.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
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
    a.binaries,
    a.datas,
    [],
    name='HeartRateOximeter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
