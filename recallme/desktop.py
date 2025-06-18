import threading
import webview

try:
    from .app import app, USE_PROXY
except ImportError:  # pragma: no cover - allow running directly
    from app import app, USE_PROXY


def _start_server():
    app.run(debug=False, use_reloader=False)


def run_window(*, no_proxy: bool = False, use_proxy: bool | None = None) -> None:
    """Launch the web interface inside a desktop window."""
    if no_proxy:
        global USE_PROXY
        USE_PROXY = False
    elif use_proxy:
        USE_PROXY = True
    thread = threading.Thread(target=_start_server, daemon=True)
    thread.start()
    webview.create_window("RecallMe", "http://localhost:5000")
    webview.start()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Launch RecallMe in a window")
    parser.add_argument("--no-proxy", action="store_true", help="ignore HTTP(S)_PROXY")
    parser.add_argument("--use-proxy", dest="no_proxy", action="store_false", help="force proxy usage")
    args = parser.parse_args()
    run_window(no_proxy=args.no_proxy, use_proxy=None if args.no_proxy else True)
