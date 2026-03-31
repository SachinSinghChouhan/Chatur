import PyInstaller.__main__
import sys
import os
from pathlib import Path

IS_WINDOWS = sys.platform == 'win32'
IS_LINUX   = sys.platform.startswith('linux')

BASE_DIR = Path(__file__).parent
dist_path = BASE_DIR / "ui" / "dist"

if not dist_path.exists():
    print("Error: ui/dist not found. Please run 'npm run build' in ui/ directory first.")
    sys.exit(1)

try:
    import azure.cognitiveservices.speech as speechsdk
    speech_sdk_dir = Path(speechsdk.__file__).parent
    print(f"Found Azure Speech SDK at: {speech_sdk_dir}")
except ImportError:
    print("Warning: Azure Speech SDK not found. STT may not work in the built executable.")
    speech_sdk_dir = None

exe_name = 'ChaturAssistant'
print(f"Starting Build Process (target: {exe_name}{'.exe' if IS_WINDOWS else ''})...")

build_args = [
    'chatur/main.py',
    f'--name={exe_name}',
    '--onefile',
    '--noconsole',
    '--clean',
    f'--add-data=ui/dist{os.pathsep}ui/dist',
    f'--add-data=config/config.yaml{os.pathsep}config',
    # TTS drivers
    '--hidden-import=pyttsx3.drivers',
    # System tray
    '--hidden-import=pystray',
    '--hidden-import=PIL',
    # Uvicorn / FastAPI
    '--hidden-import=uvicorn.logging',
    '--hidden-import=uvicorn.loops',
    '--hidden-import=uvicorn.loops.auto',
    '--hidden-import=uvicorn.protocols',
    '--hidden-import=uvicorn.protocols.http',
    '--hidden-import=uvicorn.protocols.http.auto',
    '--hidden-import=uvicorn.lifespan',
    '--hidden-import=uvicorn.lifespan.on',
    # WebView
    '--hidden-import=webview',
    '--hidden-import=pywebview',
    '--hidden-import=webview.platforms',
    # Wake word / audio
    '--hidden-import=pvporcupine',
    '--hidden-import=pyaudio',
    # Hotkeys
    '--hidden-import=pynput',
    '--hidden-import=pynput.keyboard',
    # Google APIs
    '--hidden-import=google.api_core',
    '--hidden-import=googleapiclient',
    '--hidden-import=googleapiclient.discovery',
    # Exclude heavy unused packages
    '--exclude-module=tensorflow',
    '--exclude-module=torch',
    '--exclude-module=pandas',
    '--exclude-module=matplotlib',
    '--exclude-module=scipy',
    '--exclude-module=IPython',
    '--collect-all=chatur',
    '--collect-all=webview',
    '--collect-all=pvporcupine',
]

# ── Platform-specific hidden imports ──────────────────────────────────────────
if IS_WINDOWS:
    build_args += [
        '--hidden-import=pyttsx3.drivers.sapi5',   # Windows TTS via SAPI
        '--hidden-import=comtypes',
        '--hidden-import=comtypes.stream',
        '--hidden-import=clr_loader',
        '--hidden-import=pythonnet',
        '--hidden-import=webview.platforms.winforms',
    ]
else:
    # Linux: espeak/espeak-ng TTS backend
    build_args += [
        '--hidden-import=pyttsx3.drivers.espeak',
        '--hidden-import=webview.platforms.gtk',
        '--hidden-import=webview.platforms.qt',
    ]

# ── Azure Speech SDK shared libraries ─────────────────────────────────────────
if speech_sdk_dir and speech_sdk_dir.exists():
    # Include both Windows (.dll) and Linux (.so) shared libraries
    shared_libs = (
        list(speech_sdk_dir.glob('*.dll')) +
        list(speech_sdk_dir.glob('*.so')) +
        list(speech_sdk_dir.glob('*.so.*'))
    )
    for lib in shared_libs:
        build_args.append(f'--add-binary={lib}{os.pathsep}azure/cognitiveservices/speech')
        print(f"  Adding shared library: {lib.name}")

PyInstaller.__main__.run(build_args)

print("\n" + "=" * 50)
print("Build Complete!")
suffix = '.exe' if IS_WINDOWS else ''
print(f"Executable: dist/{exe_name}{suffix}")
print("=" * 50)
