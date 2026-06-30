from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer


def run_server(host: str = "127.0.0.1", port: int = 8000) -> None:
    """Serve the project directory so index.html can run in a browser."""
    httpd = ThreadingHTTPServer((host, port), SimpleHTTPRequestHandler)
    print(f"Deck Trainer running at http://{host}:{port}")
    print("Press Ctrl+C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()


if __name__ == "__main__":
    run_server()
