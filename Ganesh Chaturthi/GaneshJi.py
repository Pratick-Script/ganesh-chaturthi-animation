"""
================================================================================
                    GANESH CHATURTHI CELEBRATION ANIMATION
================================================================================
Run this file directly or run main.py to start the full animation!
"""

import os
import sys

# Ensure root directory is in sys.path so it can find assets and modules easily
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

# Import and execute main animation
from main import GaneshAnimationApp

if __name__ == "__main__":
    app = GaneshAnimationApp()
    app.run()
