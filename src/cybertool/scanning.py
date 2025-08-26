"""Network scanning utilities."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Dict, List, Set

SERVICE_MAP: Dict[int, str] = {
    22: "ssh",
    80: "http",
    443: "https",
    8000: "http-alt",
}


@dataclass
class PortScanResult:
    port: int
    open: bool
    service: str | None = None


async def _check_port(host: str, port: int, timeout: float) -> PortScanResult:
    try:
        conn = asyncio.open_connection(host, port)
        reader, writer = await asyncio.wait_for(conn, timeout=timeout)
        writer.close()
        await writer.wait_closed()
        return PortScanResult(port=port, open=True, service=SERVICE_MAP.get(port))
    except Exception:  # pragma: no cover - network errors
        return PortScanResult(port=port, open=False)


async def scan_ports(
    host: str, ports: Set[int], timeout: float, concurrency: int
) -> List[PortScanResult]:
    sem = asyncio.Semaphore(concurrency)
    results: List[PortScanResult] = []

    async def worker(p: int) -> None:
        async with sem:
            res = await _check_port(host, p, timeout)
            results.append(res)

    await asyncio.gather(*(worker(p) for p in ports))
    results.sort(key=lambda r: r.port)
    return results
