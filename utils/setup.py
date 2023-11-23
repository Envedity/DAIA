from pathlib import Path
import os


def setup():
    paths = [Path("DAIA/Screenshots")]

    for path in paths:
        if not path.exists():
            os.mkdir(path)
