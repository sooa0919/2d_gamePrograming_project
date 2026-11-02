"""Start the movement demo with: python main.py"""

from pathlib import Path
import sys

# Resolve imports independently of the terminal's working directory.
sys.path.insert(0, str(Path(__file__).resolve().parent / "code"))

from background import main


if __name__ == "__main__":
    main()
