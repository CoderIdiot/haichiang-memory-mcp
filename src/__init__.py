"""
hc-mem package initialization
"""

import sys
from pathlib import Path

# Add project root to Python path for package imports
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Export common modules
from conf import logger

__version__ = "0.1.0"