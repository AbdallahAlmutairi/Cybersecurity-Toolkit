# Cybersecurity Toolkit

[![CI](https://github.com/example/cybersecurity-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/example/cybersecurity-toolkit/actions/workflows/ci.yml)
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.11%2B-blue)

Simple command line cybersecurity helper built with Python and Typer.

![demo](docs/demo.gif)

## Features
- Port scanning
- DNS lookup and subdomain brute force
- HTTP header inspection and directory brute force
- Hashing, cracking, encoding/decoding
- AES-GCM file encryption

## Quickstart
```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -e .[dev]
cybertool --help
cybertool version
```

## Lint & Test
```bash
ruff check .
isort --check-only .
black --check .
pytest -q
```

## Examples
```bash
cybertool scan-ports --host scanme.nmap.org --ports 20-1024
cybertool dns --domain example.com --type A,MX,TXT --json
cybertool subdomains --domain example.com --wordlist data/subdomains.txt
cybertool http-headers --url https://example.com
cybertool dirbust --url https://example.com --wordlist data/dirs.txt
cybertool hash --algo sha256 --text "hello"
cybertool crack --algo md5 --hash 5d41402abc4b2a76b9719d911017c592 --wordlist data/rockyou-mini.txt
cybertool b64-encode --text "admin:admin"
cybertool encrypt --in secrets.txt --out secrets.enc --password "StrongPass#1"
cybertool decrypt --in secrets.enc --out secrets.txt --password "StrongPass#1"
```

## Development
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pre-commit install
```

## Docker
```bash
docker build -t cybertool .
docker run --rm -it cybertool --help
```

## Troubleshooting
On Windows, line ending issues can cause noisy diffs. This repository includes a `.gitattributes` file that enforces LF endings.
If `cybertool` isn't found, ensure the project is installed with `pip install -e .` or invoke with `python -m cybertool.cli`.
WHOIS support requires the optional `python-whois` package.

## Disclaimer
Use responsibly on systems you own or have permission to test.

## Contributing
PRs welcome. Run tests and linters before submitting.

## Roadmap
- Result saving
- Web UI
