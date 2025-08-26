"""Utility helpers for Cybersecurity Toolkit."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Set

from rich.console import Console

console = Console()


@dataclass
class OutputOptions:
    json: bool = False


def load_wordlist(path: Path) -> List[str]:
    words: List[str] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                words.append(line)
    return words


def parse_ports(spec: str) -> Set[int]:
    ports: Set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-", 1)
            ports.update(range(int(start), int(end) + 1))
        else:
            ports.add(int(part))
    return ports


def rich_or_json(data: dict, options: OutputOptions) -> None:
    if options.json:
        console.print_json(data=data)
    else:
        from rich.table import Table

        table = Table(show_header=True, header_style="bold magenta")
        for key in data.keys():
            table.add_column(key)
        table.add_row(*[str(v) for v in data.values()])
        console.print(table)
