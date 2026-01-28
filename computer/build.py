import PyInstaller.__main__
import sys
import os
from pathlib import Path

# Determine base directory
BASE_DIR = Path(__file__).parent
dist_path = BASE_DIR / "ui" / "dist"

if not dist_path.exists():
    print("Error: content/ui/dist not found. Please run 'npm run build' in ui/ directory first.")
    sys.exit(1)

print("Starting Build Process...")

PyInstaller.__main__.run([
    'chatur/main.py',
    '--name=ChaturAssistant',
    '--onefile',
    '--clean',
    '--add-data=ui/dist;ui/dist',
    '--add-data=config/config.yaml;config',
    '--hidden-import=comtypes',
    '--hidden-import=comtypes.stream',
    '--hidden-import=pyttsx3.drivers',
    '--hidden-import=pyttsx3.drivers.sapi5',
    '--hidden-import=pystray',
    '--hidden-import=PIL',
    '--hidden-import=engineio.async_drivers.aiohttp',
    '--hidden-import=uvicorn.logging',
    '--hidden-import=uvicorn.loops',
    '--hidden-import=uvicorn.loops.auto',
    '--hidden-import=uvicorn.protocols',
    '--hidden-import=uvicorn.protocols.http',
    '--hidden-import=uvicorn.protocols.http.auto',
    '--hidden-import=uvicorn.lifespan',
    '--hidden-import=uvicorn.lifespan.on',
    '--exclude-module=tensorflow',
    '--exclude-module=torch',
    '--exclude-module=pandas',
    '--exclude-module=numpy',
    '--exclude-module=matplotlib',
    '--exclude-module=scipy',
    '--exclude-module=IPython',
    '--collect-all=chatur',
])

print("Build Complete. Executable is in dist/ChaturAssistant.exe")
