"""Cross-platform utility helpers — path resolution, file opening, app defaults."""

import os
import sys
import subprocess
import warnings
from pathlib import Path
from typing import Optional

# ─── OS detection ────────────────────────────────────────────────────────────

IS_WINDOWS = sys.platform == 'win32'
IS_LINUX   = sys.platform.startswith('linux')
IS_MAC     = sys.platform == 'darwin'


# ─── App data directory ──────────────────────────────────────────────────────

def get_app_data_dir() -> Path:
    """
    Return the platform-appropriate directory for storing app data.

    - Windows: %APPDATA%/Computer  (e.g. C:\\Users\\Alice\\AppData\\Roaming\\Computer)
    - Linux:   ~/.config/Computer
    - macOS:   ~/Library/Application Support/Computer
    """
    if IS_WINDOWS:
        base = os.getenv('APPDATA')
        if not base:
            # Fallback if APPDATA is somehow missing
            base = Path.home() / 'AppData' / 'Roaming'
        app_dir = Path(base) / 'Computer'
    elif IS_MAC:
        app_dir = Path.home() / 'Library' / 'Application Support' / 'Computer'
    else:
        # Linux / everything else
        xdg_config = os.getenv('XDG_CONFIG_HOME', str(Path.home() / '.config'))
        app_dir = Path(xdg_config) / 'Computer'

    app_dir.mkdir(parents=True, exist_ok=True)
    return app_dir


# ─── Open file / folder ──────────────────────────────────────────────────────

def open_path(path: str) -> bool:
    """
    Open a file or folder using the system default application.

    - Windows: os.startfile()
    - Linux:   xdg-open
    - macOS:   open
    """
    try:
        if IS_WINDOWS:
            os.startfile(path)  # type: ignore[attr-defined]
        elif IS_MAC:
            subprocess.Popen(['open', path])
        else:
            subprocess.Popen(['xdg-open', path])
        return True
    except Exception as e:
        warnings.warn(f"Failed to open path '{path}': {e}")
        return False


# ─── Default app paths ───────────────────────────────────────────────────────

def get_default_apps() -> list:
    """
    Return a list of default app tuples compatible with init_db.py:
    (name, display_name, path, app_type, aliases, is_default)
    """
    home = str(Path.home())

    if IS_WINDOWS:
        username = os.getenv('USERNAME', 'User')
        return [
            ('brave',      'Brave Browser',   r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe', 'exe', 'browser,brave',          1),
            ('chrome',     'Google Chrome',   r'C:\Program Files\Google\Chrome\Application\chrome.exe',              'exe', 'browser,google',         1),
            ('firefox',    'Mozilla Firefox', r'C:\Program Files\Mozilla Firefox\firefox.exe',                       'exe', 'browser,mozilla',        1),
            ('edge',       'Microsoft Edge',  r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',       'exe', 'browser,microsoft',      1),
            ('gmail',      'Gmail',           'https://mail.google.com',                                             'url', 'email,mail',             1),
            ('calculator', 'Calculator',      'calc.exe',                                                            'exe', 'calc',                   1),
            ('notepad',    'Notepad',         'notepad.exe',                                                         'exe', 'text,editor',            1),
            ('explorer',   'File Explorer',   'explorer.exe',                                                        'exe', 'files,folder',           1),
            ('whatsapp',   'WhatsApp',        rf'C:\Users\{username}\AppData\Local\WhatsApp\WhatsApp.exe',           'exe', 'chat,messaging',         1),
            ('spotify',    'Spotify',         rf'C:\Users\{username}\AppData\Roaming\Spotify\Spotify.exe',           'exe', 'music,audio',            1),
        ]
    else:
        # Linux (and macOS)
        return [
            ('brave',      'Brave Browser',   'brave-browser',            'exe', 'browser,brave',          1),
            ('chrome',     'Google Chrome',   'google-chrome',            'exe', 'browser,google',         1),
            ('firefox',    'Mozilla Firefox', 'firefox',                  'exe', 'browser,mozilla',        1),
            ('gmail',      'Gmail',           'https://mail.google.com',  'url', 'email,mail',             1),
            ('calculator', 'Calculator',      'gnome-calculator',         'exe', 'calc',                   1),
            ('notepad',    'Text Editor',     'gedit',                    'exe', 'text,editor',            1),
            ('explorer',   'File Manager',    'nautilus',                 'exe', 'files,folder',           1),
            ('spotify',    'Spotify',         'spotify',                  'exe', 'music,audio',            1),
            ('whatsapp',   'WhatsApp Web',    'https://web.whatsapp.com', 'url', 'chat,messaging',         1),
        ]


# ─── Volume control (Linux) ──────────────────────────────────────────────────

def set_volume_linux(percent: int) -> bool:
    """Set system volume on Linux using pactl (PulseAudio) or amixer (ALSA)."""
    percent = max(0, min(100, percent))
    # Try pactl first (PulseAudio / PipeWire-pulse)
    try:
        subprocess.run(
            ['pactl', 'set-sink-volume', '@DEFAULT_SINK@', f'{percent}%'],
            check=True, capture_output=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    # Fallback: amixer (ALSA)
    try:
        subprocess.run(
            ['amixer', '-q', 'sset', 'Master', f'{percent}%'],
            check=True, capture_output=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        warnings.warn("Neither pactl nor amixer available for volume control")
        return False


def get_default_file_search_paths() -> list:
    """Return platform-appropriate default file search locations."""
    home = Path.home()
    paths = [
        str(home / 'Desktop'),
        str(home / 'Documents'),
        str(home / 'Downloads'),
        str(home),
    ]
    if IS_WINDOWS:
        paths += ['C:\\', 'D:\\']
    return paths
