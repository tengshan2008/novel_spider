import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1]))

try:
    from novel import book, crawel, fix
    from picture import gif
    from anime import info
except ImportError as e:
    print("import error, error is:", e)
