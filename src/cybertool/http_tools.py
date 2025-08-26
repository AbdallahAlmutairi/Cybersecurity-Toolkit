"""HTTP related utilities."""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Dict, Iterable, List
from urllib.parse import urljoin

import aiohttp
import requests

from .utils import load_wordlist

SEC_HEADERS = [
    "Content-Security-Policy",
    "X-Content-Type-Options",
    "X-Frame-Options",
    "Referrer-Policy",
    "Strict-Transport-Security",
    "Permissions-Policy",
]


def fetch_headers(
    url: str, timeout: float = 5.0, verify: bool = True
) -> Dict[str, str]:
    resp = requests.get(url, timeout=timeout, verify=verify, allow_redirects=True)
    headers = {k: v for k, v in resp.headers.items()}
    for h in SEC_HEADERS:
        headers.setdefault(h, "<missing>")
    return headers


async def dir_bruteforce(
    base_url: str,
    wordlist: Path,
    codes: Iterable[int],
    concurrency: int,
    timeout: float = 5.0,
) -> List[Dict[str, str]]:
    words = load_wordlist(wordlist)
    sem = asyncio.Semaphore(concurrency)
    results: List[Dict[str, str]] = []

    async with aiohttp.ClientSession(raise_for_status=False) as session:

        async def worker(word: str) -> None:
            url = urljoin(base_url, word)
            try:
                async with sem:
                    async with session.get(url, timeout=timeout) as resp:
                        if resp.status in codes:
                            results.append({"url": url, "status": str(resp.status)})
            except Exception:
                pass

        await asyncio.gather(*(worker(w) for w in words))
    return results


def fetch_robots(url: str) -> str:
    resp = requests.get(url.rstrip("/") + "/robots.txt", timeout=5)
    return resp.text


def fetch_sitemap(url: str, limit: int = 10) -> List[str]:
    resp = requests.get(url, timeout=5)
    urls: List[str] = []
    from xml.etree import ElementTree as ET

    root = ET.fromstring(resp.text)
    for loc in root.findall(".//{*}loc")[:limit]:
        urls.append(loc.text or "")
    return urls
