"""WHOIS lookup utilities."""

from __future__ import annotations

from typing import Any, Dict


def query_whois(domain: str) -> Dict[str, Any]:
    try:
        import whois  # type: ignore
    except Exception as exc:  # pragma: no cover - optional
        raise RuntimeError("Install optional dependency: python-whois") from exc

    data = whois.whois(domain)
    return dict(data)
