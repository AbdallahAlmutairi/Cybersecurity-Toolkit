"""Cryptographic utilities."""

from __future__ import annotations

import base64
import hashlib
import os
from pathlib import Path
from typing import Optional
from urllib.parse import quote, unquote

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


def hash_text(algo: str, text: str) -> str:
    h = hashlib.new(algo)
    h.update(text.encode())
    return h.hexdigest()


def crack_hash(algo: str, target_hash: str, wordlist: Path) -> Optional[str]:
    with wordlist.open("r", encoding="utf-8", errors="ignore") as f:
        for word in f:
            word = word.strip()
            if not word:
                continue
            if hash_text(algo, word) == target_hash:
                return word
    return None


def b64_encode(text: str) -> str:
    return base64.b64encode(text.encode()).decode()


def b64_decode(text: str) -> str:
    return base64.b64decode(text.encode()).decode()


def url_encode(text: str) -> str:
    return quote(text)


def url_decode(text: str) -> str:
    return unquote(text)


def _derive_key(password: str, salt: bytes) -> bytes:
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
    return kdf.derive(password.encode())


def encrypt_file(inp: Path, outp: Path, password: str) -> None:
    salt = os.urandom(16)
    key = _derive_key(password, salt)
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    data = inp.read_bytes()
    cipher = aesgcm.encrypt(nonce, data, None)
    outp.write_bytes(salt + nonce + cipher)


def decrypt_file(inp: Path, outp: Path, password: str) -> None:
    data = inp.read_bytes()
    salt, nonce, cipher = data[:16], data[16:28], data[28:]
    key = _derive_key(password, salt)
    aesgcm = AESGCM(key)
    plain = aesgcm.decrypt(nonce, cipher, None)
    outp.write_bytes(plain)
