from pathlib import Path

import pytest
from pytest_httpserver import HTTPServer

from cybertool.http_tools import dir_bruteforce, fetch_headers


def test_fetch_headers(httpserver: HTTPServer):
    httpserver.expect_request("/").respond_with_data("ok", headers={"X-Test": "1"})
    url = httpserver.url_for("/")
    headers = fetch_headers(url)
    assert headers["X-Test"] == "1"


@pytest.mark.asyncio
async def test_dir_bruteforce(httpserver: HTTPServer, tmp_path: Path):
    httpserver.expect_request("/admin").respond_with_data("ok")
    httpserver.expect_request("/login").respond_with_data("ok")
    wl = tmp_path / "wl.txt"
    wl.write_text("admin\nfoo\nlogin\n")
    results = await dir_bruteforce(httpserver.url_for("/"), wl, {200}, concurrency=5)
    urls = {r["url"] for r in results}
    assert httpserver.url_for("/admin") in urls
    assert httpserver.url_for("/login") in urls
