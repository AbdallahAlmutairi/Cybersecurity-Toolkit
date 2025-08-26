"""WHOIS lookup utilities."""

from __future__ import annotations

try:
    import whois  # type: ignore
except Exception:  # noqa: BLE001
    whois = None


def do_whois(domain: str) -> dict:
    """Perform a WHOIS lookup for a domain."""
    if whois is None:
        raise RuntimeError(
            "Optional dependency missing. Install: pip install python-whois"
        )
    data = whois.whois(domain)
    return {k: str(v) for k, v in data.items()}
