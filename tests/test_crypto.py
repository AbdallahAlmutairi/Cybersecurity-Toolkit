from pathlib import Path

from cybertool.crypto_tools import (
    b64_decode,
    b64_encode,
    crack_hash,
    decrypt_file,
    encrypt_file,
    hash_text,
    url_decode,
    url_encode,
)


def test_hash_and_crack(tmp_path: Path):
    text = "hello"
    digest = hash_text("md5", text)
    assert digest == "5d41402abc4b2a76b9719d911017c592"

    wl = tmp_path / "wl.txt"
    wl.write_text("foo\nhello\n")
    found = crack_hash("md5", digest, wl)
    assert found == "hello"


def test_encodings(tmp_path: Path):
    assert b64_decode(b64_encode("abc")) == "abc"
    assert url_decode(url_encode("a b")) == "a b"

    inp = tmp_path / "in.txt"
    inp.write_text("secret")
    enc = tmp_path / "out.bin"
    dec = tmp_path / "dec.txt"
    encrypt_file(inp, enc, "pass")
    decrypt_file(enc, dec, "pass")
    assert dec.read_text() == "secret"
