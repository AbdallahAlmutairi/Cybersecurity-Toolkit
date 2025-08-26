import asyncio

from cybertool.scanning import scan_ports


async def open_dummy_server(port: int):
    server = await asyncio.start_server(lambda r, w: None, "127.0.0.1", port)
    return server


def test_scan_ports_event_loop():
    port = 8888
    loop = asyncio.get_event_loop()
    server = loop.run_until_complete(open_dummy_server(port))
    try:
        results = loop.run_until_complete(scan_ports("127.0.0.1", {port, 1}, 0.5, 100))
    finally:
        server.close()
        loop.run_until_complete(server.wait_closed())
    open_ports = [r.port for r in results if r.open]
    assert port in open_ports
