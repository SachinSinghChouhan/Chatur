"""
First-run setup checks.
Runs once at startup to verify local dependencies are ready
and guide the user if anything is missing.
"""

import sys
import urllib.request
from pathlib import Path
from chatur.utils.logger import setup_logger
from chatur.utils.config import config

logger = setup_logger('chatur.setup')

_FLAG_FILE = Path.home() / '.config' / 'chatur' / '.first_run_done'


def _ollama_running() -> bool:
    """Return True if Ollama's HTTP API is reachable."""
    base_url = config.get('llm.ollama_base_url', 'http://localhost:11434/v1')
    health_url = base_url.replace('/v1', '') + '/api/tags'
    try:
        with urllib.request.urlopen(health_url, timeout=2) as resp:
            return resp.status == 200
    except Exception:
        return False


def _check_ollama():
    """Warn if Ollama is not running."""
    if _ollama_running():
        model = config.get('llm.ollama_model', 'llama3')
        logger.info(f"Ollama is running (model: {model})")
        return

    model = config.get('llm.ollama_model', 'llama3')
    logger.warning(
        "Ollama is not running. Chatur needs Ollama for answering questions.\n"
        "  Install : https://ollama.com\n"
        f"  Then run: ollama pull {model}\n"
        "  Finally : ollama serve"
    )
    print(
        "\n[Chatur] Ollama not found — question answering will be unavailable.\n"
        "  1. Install Ollama from https://ollama.com\n"
        f"  2. Run: ollama pull {model}\n"
        "  3. Run: ollama serve\n"
        "  Then restart Chatur.\n"
    )


def _check_whisper_model():
    """
    If local_whisper is the configured STT engine, pre-warm the model so the
    download happens at startup rather than on the first voice command.
    """
    if config.get('stt.engine', 'local_whisper') != 'local_whisper':
        return

    try:
        from faster_whisper import WhisperModel
        model_size = config.get('whisper.model', 'base')
        device = config.get('whisper.device', 'cpu')
        compute_type = config.get('whisper.compute_type', 'int8')

        logger.info(
            f"Pre-loading Whisper model '{model_size}' "
            "(downloads ~300 MB on first run — this only happens once)..."
        )
        print(
            f"\n[Chatur] Loading speech recognition model '{model_size}'...\n"
            "  (Downloads ~300 MB on first run — won't happen again)\n"
        )
        WhisperModel(model_size, device=device, compute_type=compute_type)
        logger.info("Whisper model ready")
        print("[Chatur] Speech recognition model ready.\n")

    except ImportError:
        logger.error(
            "faster-whisper is not installed but stt.engine=local_whisper.\n"
            "  Fix: pip install faster-whisper"
        )
        print(
            "\n[Chatur] ERROR: faster-whisper package not found.\n"
            "  Run: pip install faster-whisper\n"
        )
    except Exception as e:
        logger.warning(f"Whisper model pre-load failed: {e}")


def run_if_needed():
    """
    Run first-run checks once.  After the first successful run a flag file is
    written so subsequent launches skip the slow checks.
    """
    # Always check Ollama (it might have been stopped since last run)
    if config.get('llm.provider', 'ollama') == 'ollama':
        _check_ollama()

    # Model download only needs to happen once
    if not _FLAG_FILE.exists():
        _check_whisper_model()
        try:
            _FLAG_FILE.parent.mkdir(parents=True, exist_ok=True)
            _FLAG_FILE.touch()
        except Exception:
            pass  # Non-fatal
