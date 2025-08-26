import asyncio
from pathlib import Path
from unittest.mock import MagicMock, patch

from cybertool.dns_tools import dns_lookup, subdomain_bruteforce


def test_dns_lookup_event_loop():
    async def fake_resolve(domain, rtype):
        return [MagicMock(to_text=lambda: "1.2.3.4")]

    with patch("dns.resolver.Resolver.resolve", side_effect=fake_resolve):
        result = asyncio.run(dns_lookup("example.com", ["A"]))
    assert result["A"] == ["1.2.3.4"]


def test_subdomain_bruteforce(tmp_path: Path):
    async def fake_resolve(domain, rtype):
        if domain == "www.example.com":
            return [MagicMock(to_text=lambda: "1.2.3.4")]
        raise Exception

    wordlist = tmp_path / "wl.txt"
    wordlist.write_text("www\nmail\n")

    with patch("dns.resolver.Resolver.resolve", side_effect=fake_resolve):
        found = asyncio.run(subdomain_bruteforce("example.com", wordlist, 10))
    assert found == ["www.example.com"]
