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

# Locate Azure Speech SDK DLLs
try:
    import azure.cognitiveservices.speech as speechsdk
    speech_sdk_dir = Path(speechsdk.__file__).parent
    print(f"Found Azure Speech SDK at: {speech_sdk_dir}")
except ImportError:
    print("Warning: Azure Speech SDK not found. STT may not work in the built executable.")
    speech_sdk_dir = None

print("Starting Build Process...")

build_args = [
    'chatur/main.py',
    '--name=ChaturAssistant',
    '--onefile',
    '--noconsole',  # Hide the console window (GUI mode)
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
    '--hidden-import=webview',
    '--hidden-import=pywebview',
    '--hidden-import=webview.platforms',
    '--hidden-import=webview.platforms.winforms',
    '--hidden-import=clr_loader',
    '--hidden-import=pythonnet',
    '--exclude-module=tensorflow',
    '--exclude-module=torch',
    '--exclude-module=pandas',
    '--exclude-module=numpy',
    '--exclude-module=matplotlib',
    '--exclude-module=scipy',
    '--exclude-module=IPython',
    '--collect-all=chatur',
    '--collect-all=webview',
]

# Add Azure Speech SDK DLLs if found
if speech_sdk_dir and speech_sdk_dir.exists():
    dll_files = list(speech_sdk_dir.glob('*.dll'))
    for dll in dll_files:
        build_args.append(f'--add-binary={dll};azure/cognitiveservices/speech')
        print(f"  Adding DLL: {dll.name}")

PyInstaller.__main__.run(build_args)

print("Build Complete. Executable is in dist/ChaturAssistant.exe")
