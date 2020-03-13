import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1]))

try:
    from novel import book, crawel, check
    from picture import gif
except ImportError as e:
    print("import error, error is:", e)
