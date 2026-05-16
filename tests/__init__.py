from pathlib import Path
import sys

# Always ensure the repository root is on sys.path when running tests.
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
