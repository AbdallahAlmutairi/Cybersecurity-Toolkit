"""DNS related utilities."""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Dict, List

import dns.resolver

from .utils import load_wordlist


async def dns_lookup(domain: str, record_types: List[str]) -> Dict[str, List[str]]:
    result: Dict[str, List[str]] = {}
    resolver = dns.resolver.Resolver()
    for rtype in record_types:
        try:
            answers = await asyncio.to_thread(resolver.resolve, domain, rtype)
            result[rtype] = [a.to_text() for a in answers]
        except Exception:
            result[rtype] = []
    return result


async def subdomain_bruteforce(
    domain: str, wordlist: Path, concurrency: int
) -> List[str]:
    words = load_wordlist(wordlist)
    sem = asyncio.Semaphore(concurrency)
    found: List[str] = []
    resolver = dns.resolver.Resolver()

    async def worker(sub: str) -> None:
        fqdn = f"{sub}.{domain}"
        try:
            async with sem:
                await asyncio.to_thread(resolver.resolve, fqdn, "A")
                found.append(fqdn)
        except Exception:
            pass

    await asyncio.gather(*(worker(w) for w in words))
    return sorted(found)
