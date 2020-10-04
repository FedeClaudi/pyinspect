from pathlib import Path

# Make a base folder for pyinspect
base_dir = Path.home() / ".pyinspect"
base_dir.mkdir(exist_ok=True)

error_cache = base_dir / "error_cache.txt"
