"""Cybersecurity Toolkit package."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("cybertool")
except PackageNotFoundError:  # pragma: no cover - during local development
    __version__ = "0.1.0"

__all__ = ["__version__"]
