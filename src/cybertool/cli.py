"""Typer CLI for Cybersecurity Toolkit."""

from __future__ import annotations

import asyncio
from pathlib import Path

import typer
from rich.console import Console

from . import __version__
from .crypto_tools import (
    b64_decode,
    b64_encode,
    crack_hash,
    decrypt_file,
    encrypt_file,
    hash_text,
    url_decode,
    url_encode,
)
from .dns_tools import dns_lookup, subdomain_bruteforce
from .http_tools import dir_bruteforce, fetch_headers, fetch_robots, fetch_sitemap
from .scanning import scan_ports
from .utils import parse_ports
from .whois_tools import query_whois

app = typer.Typer(help="Cybersecurity Toolkit")
console = Console()


@app.callback()
def main() -> None:  # pragma: no cover - CLI entry
    pass


@app.command()
def scan_ports_cmd(
    host: str = typer.Option(..., "--host"),
    ports: str = typer.Option("1-1024"),
    timeout: float = 0.5,
    concurrency: int = 200,
    json: bool = typer.Option(False, "--json"),
) -> None:
    """Asynchronously scan TCP ports."""
    port_set = parse_ports(ports)
    results = asyncio.run(scan_ports(host, port_set, timeout, concurrency))
    if json:
        data = [
            {"port": r.port, "open": r.open, "service": r.service}
            for r in results
            if r.open
        ]
        console.print_json(data)
    else:
        from rich.table import Table

        table = Table(title=f"Open ports for {host}")
        table.add_column("Port")
        table.add_column("Service")
        for r in results:
            if r.open:
                table.add_row(str(r.port), r.service or "?")
        console.print(table)


@app.command("dns")
def dns_cmd(
    domain: str,
    type: str = typer.Option("A"),
    json: bool = typer.Option(False, "--json"),
) -> None:
    types = [t.strip() for t in type.split(",")]
    data = asyncio.run(dns_lookup(domain, types))
    if json:
        console.print_json(data)
    else:
        from rich.table import Table

        table = Table(title=f"DNS records for {domain}")
        table.add_column("Type")
        table.add_column("Values")
        for t, vals in data.items():
            table.add_row(t, ", ".join(vals) or "-")
        console.print(table)


@app.command("subdomains")
def subdomains_cmd(
    domain: str,
    wordlist: Path = typer.Option(...),
    concurrency: int = 200,
    json: bool = typer.Option(False, "--json"),
) -> None:
    found = asyncio.run(subdomain_bruteforce(domain, wordlist, concurrency))
    if json:
        console.print_json(found)
    else:
        for f in found:
            console.print(f)


@app.command("http-headers")
def http_headers_cmd(url: str, json: bool = typer.Option(False, "--json")) -> None:
    headers = fetch_headers(url)
    if json:
        console.print_json(headers)
    else:
        from rich.table import Table

        table = Table(title=f"Headers for {url}")
        table.add_column("Header")
        table.add_column("Value")
        for k, v in headers.items():
            table.add_row(k, v)
        console.print(table)


@app.command("dirbust")
def dirbust_cmd(
    url: str,
    wordlist: Path = typer.Option(...),
    codes: str = "200,204,301,302,403",
    concurrency: int = 200,
    json: bool = typer.Option(False, "--json"),
) -> None:
    code_set = {int(c) for c in codes.split(",")}
    results = asyncio.run(dir_bruteforce(url, wordlist, code_set, concurrency))
    if json:
        console.print_json(results)
    else:
        from rich.table import Table

        table = Table(title="Directory brute force")
        table.add_column("URL")
        table.add_column("Status")
        for r in results:
            table.add_row(r["url"], r["status"])
        console.print(table)


@app.command("robots")
def robots_cmd(url: str) -> None:
    console.print(fetch_robots(url))


@app.command("sitemap")
def sitemap_cmd(
    url: str, limit: int = 10, json: bool = typer.Option(False, "--json")
) -> None:
    urls = fetch_sitemap(url, limit)
    if json:
        console.print_json(urls)
    else:
        for u in urls:
            console.print(u)


@app.command("hash")
def hash_cmd(algo: str, text: str) -> None:
    console.print(hash_text(algo, text))


@app.command("crack")
def crack_cmd(algo: str, hash: str, wordlist: Path = typer.Option(...)) -> None:
    result = crack_hash(algo, hash, wordlist)
    if result:
        console.print(result)
    else:
        raise typer.Exit(code=1)


@app.command("b64-encode")
def b64_encode_cmd(text: str) -> None:
    console.print(b64_encode(text))


@app.command("b64-decode")
def b64_decode_cmd(text: str) -> None:
    console.print(b64_decode(text))


@app.command("url-encode")
def url_encode_cmd(text: str) -> None:
    console.print(url_encode(text))


@app.command("url-decode")
def url_decode_cmd(text: str) -> None:
    console.print(url_decode(text))


@app.command("encrypt")
def encrypt_cmd(inp: Path, out: Path, password: str) -> None:
    encrypt_file(inp, out, password)


@app.command("decrypt")
def decrypt_cmd(inp: Path, out: Path, password: str) -> None:
    decrypt_file(inp, out, password)


@app.command("whois")
def whois_cmd(domain: str) -> None:
    try:
        data = query_whois(domain)
    except RuntimeError as exc:
        console.print(str(exc))
        raise typer.Exit(code=1)
    console.print_json(data)


@app.command("version")
def version_cmd() -> None:  # pragma: no cover - trivial
    console.print(__version__)


if __name__ == "__main__":  # pragma: no cover
    app()
