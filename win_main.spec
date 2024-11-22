# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_submodules, collect_data_files

# Collect all submodules from 'ui' and 'models'
hidden_imports = (
    collect_submodules('ui') + 
    collect_submodules('models') +
    ['tkinter', 'Pillow', 'PIL._imagingtk', 'PIL._tkinter_finder']
)

# Specify non-Python data files to include
datas = [
    ('src/ui/image.png', '.'),       # image.png in src/ui directory
    ('src/tasks.json', '.'),         # tasks.json in src directory
    ('src/events.json', '.')         # events.json in src directory
]

# Add Pillow's additional data files (e.g., image format handlers)
datas += collect_data_files('PIL')

# Specify binaries to include (e.g., Python DLL)
binaries = [
    ('C:\\Users\\willm\\AppData\\Local\\Programs\\Python\\Python310\\python310.dll', '.')
]

# Analysis step: define all inputs
a = Analysis(
    ['src/main.py'],               # Entry point in src directory
    pathex=['src'],                # Include src directory in search path
    binaries=binaries,             # Include Python DLL and other binaries
    datas=datas,                   # Include non-Python files (image, json files)
    hiddenimports=hidden_imports,  # Include submodules from ui and models
    hookspath=['.'],               # Custom hooks (none in this case)
    hooksconfig={},                # Hook configurations
    runtime_hooks=[],              # Runtime hook files (none in this case)
    excludes=[],                   # Modules to exclude (none in this case)
    noarchive=False,               # Do not bundle as a single .pyz archive
    optimize=0,                    # Optimization level (0 = none)
    onefile=True,                  # Enable onefile mode
)

# Create a PYZ archive (Python files as a single ZIP)
pyz = PYZ(
    a.pure, 
    a.zipped_data,
    cipher=None,                   # No encryption for the archive
)

# Create an EXE (the executable file)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,         # Exclude binaries here; included in COLLECT
    name='EasyCal',             # Name of the executable
    debug=False,                   # Debugging disabled
    bootloader_ignore_signals=False,
    strip=False,                   # Do not strip debug symbols
    upx=True,                      # Compress binaries with UPX
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,          # MacOS-specific, safe to leave as False
    target_arch='amd64',           # Ensure the architecture matches (64-bit)
    codesign_identity=None,        # MacOS-specific
    entitlements_file=None,        # MacOS-specific
)

# Final step: collect all outputs into a single directory
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,                   # Do not strip symbols from collected files
    upx=True,                      # Compress collected files with UPX
    upx_exclude=[],                # Exclude specific files from UPX (none here)
    name='Innovators',             # Output directory name
)