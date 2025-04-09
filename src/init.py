import os
from pathlib import Path

# Initialize folders
Path("data/cache").mkdir(parents=True, exist_ok=True)
Path("data/outputs").mkdir(parents=True, exist_ok=True)
Path("static").mkdir(exist_ok=True)
Path("templates").mkdir(exist_ok=True)
