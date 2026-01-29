# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = [('ui/dist', 'ui/dist'), ('config/config.yaml', 'config')]
binaries = [('C:\\Users\\sachi\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\site-packages\\azure\\cognitiveservices\\speech\\Microsoft.CognitiveServices.Speech.core.dll', 'azure/cognitiveservices/speech'), ('C:\\Users\\sachi\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\site-packages\\azure\\cognitiveservices\\speech\\Microsoft.CognitiveServices.Speech.extension.audio.sys.dll', 'azure/cognitiveservices/speech'), ('C:\\Users\\sachi\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\site-packages\\azure\\cognitiveservices\\speech\\Microsoft.CognitiveServices.Speech.extension.codec.dll', 'azure/cognitiveservices/speech'), ('C:\\Users\\sachi\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\site-packages\\azure\\cognitiveservices\\speech\\Microsoft.CognitiveServices.Speech.extension.kws.dll', 'azure/cognitiveservices/speech'), ('C:\\Users\\sachi\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\site-packages\\azure\\cognitiveservices\\speech\\Microsoft.CognitiveServices.Speech.extension.lu.dll', 'azure/cognitiveservices/speech')]
hiddenimports = ['comtypes', 'comtypes.stream', 'pyttsx3.drivers', 'pyttsx3.drivers.sapi5', 'pystray', 'PIL', 'engineio.async_drivers.aiohttp', 'uvicorn.logging', 'uvicorn.loops', 'uvicorn.loops.auto', 'uvicorn.protocols', 'uvicorn.protocols.http', 'uvicorn.protocols.http.auto', 'uvicorn.lifespan', 'uvicorn.lifespan.on', 'webview', 'pywebview', 'webview.platforms', 'webview.platforms.winforms', 'clr_loader', 'pythonnet']
tmp_ret = collect_all('chatur')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('webview')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['chatur\\main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tensorflow', 'torch', 'pandas', 'numpy', 'matplotlib', 'scipy', 'IPython'],
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
    name='ChaturAssistant',
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
