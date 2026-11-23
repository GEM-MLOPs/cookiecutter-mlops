"""Only removes the generated license when explicitly opted out."""
from pathlib import Path

if "{{ cookiecutter.open_source_license }}" == "No license file":
    Path("LICENSE").unlink(missing_ok=True)
