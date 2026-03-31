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

exe_name = 'ChaturAssistant'
print(f"Starting Build Process (target: {exe_name}{'.exe' if IS_WINDOWS else ''})...")

build_args = [
    'chatur/main.py',
    f'--name={exe_name}',
    '--onefile',
    '--noconsole',
    '--clean',
    '--strip',  # Strip debug symbols (significant size reduction)
    f'--add-data=ui/dist{os.pathsep}ui/dist',
    f'--add-data=config/config.yaml{os.pathsep}config',

    # ── Only import what we actually need ────────────────────────────────────
    # TTS
    '--hidden-import=pyttsx3.drivers',
    # System tray
    '--hidden-import=pystray',
    '--hidden-import=PIL',
    # FastAPI / Uvicorn
    '--hidden-import=uvicorn.logging',
    '--hidden-import=uvicorn.loops',
    '--hidden-import=uvicorn.loops.auto',
    '--hidden-import=uvicorn.protocols',
    '--hidden-import=uvicorn.protocols.http',
    '--hidden-import=uvicorn.protocols.http.auto',
    '--hidden-import=uvicorn.lifespan',
    '--hidden-import=uvicorn.lifespan.on',
    # Hotkeys
    '--hidden-import=pynput',
    '--hidden-import=pynput.keyboard',
    # Audio
    '--hidden-import=pyaudio',
    # Core app
    '--collect-all=chatur',

    # ── Exclude heavy packages ───────────────────────────────────────────────
    '--exclude-module=tensorflow',
    '--exclude-module=torch',
    '--exclude-module=pandas',
    '--exclude-module=matplotlib',
    '--exclude-module=scipy',
    '--exclude-module=IPython',
    '--exclude-module=notebook',
    '--exclude-module=jupyter',
    '--exclude-module=pytest',
    '--exclude-module=setuptools',
    '--exclude-module=pip',
    '--exclude-module=wheel',
    '--exclude-module=distutils',
    '--exclude-module=tkinter',
    '--exclude-module=unittest',
    '--exclude-module=doctest',
    '--exclude-module=pdb',
    '--exclude-module=lib2to3',
    # Azure Speech SDK is ~100MB — exclude from bundle, users install separately
    '--exclude-module=azure',
    '--exclude-module=azure.cognitiveservices',
    '--exclude-module=azure.cognitiveservices.speech',
    # PyQt is ~150MB on Linux — use system GTK instead
    '--exclude-module=PyQt6',
    '--exclude-module=PyQt5',
    '--exclude-module=qtpy',
    '--exclude-module=PyQt6.QtWebEngineWidgets',
    '--exclude-module=PyQt6.QtWebEngineCore',
    # Don't bundle all pvporcupine platform models
    '--exclude-module=pvporcupine',
    # openwakeword pulls onnxruntime (~50MB) + numpy
    '--exclude-module=openwakeword',
    '--exclude-module=onnxruntime',
    # Vosk native libs
    '--exclude-module=vosk',
    # Google API client (users set up OAuth separately)
    '--exclude-module=googleapiclient',
    '--exclude-module=google.auth',
    '--exclude-module=google.oauth2',
    '--exclude-module=google_auth_httplib2',
    '--exclude-module=google_auth_oauthlib',
    # Crypto (pulled by various deps but not needed at runtime)
    '--exclude-module=nacl',
]

# ── Platform-specific ────────────────────────────────────────────────────────
if IS_WINDOWS:
    build_args += [
        '--hidden-import=pyttsx3.drivers.sapi5',
        '--hidden-import=comtypes',
        '--hidden-import=comtypes.stream',
        '--hidden-import=webview',
        '--hidden-import=webview.platforms',
        '--hidden-import=webview.platforms.winforms',
        '--noupx',  # UPX on Windows can trigger false antivirus positives
    ]
else:
    build_args += [
        '--hidden-import=pyttsx3.drivers.espeak',
        # Only import GTK backend, not Qt (saves ~150MB)
        '--hidden-import=webview',
        '--hidden-import=webview.platforms',
        '--hidden-import=webview.platforms.gtk',
    ]

PyInstaller.__main__.run(build_args)

print("\n" + "=" * 50)
print("Build Complete!")
suffix = '.exe' if IS_WINDOWS else ''
print(f"Executable: dist/{exe_name}{suffix}")
print("=" * 50)
