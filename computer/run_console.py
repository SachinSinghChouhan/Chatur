"""
Launch the Computer Voice Assistant in Console mode
"""

import sys
from chatur.main import main

if __name__ == "__main__":
    # Add --console flag
    sys.argv.append('--console')
    main()
