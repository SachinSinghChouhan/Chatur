"""
Launch the Computer Voice Assistant in System Tray mode
"""

import sys
from chatur.main import main

if __name__ == "__main__":
    # Add --tray flag
    sys.argv.append('--tray')
    main()
