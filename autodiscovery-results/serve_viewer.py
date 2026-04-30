#!/usr/bin/env python3
"""
Local server for experiment card viewer with auto-saving notes.
Notes are stored as timestamped entries in ## 7. Notes section of each *_card.md.

Usage:
    python3 autodiscovery-results/serve_viewer.py
    # Opens http://localhost:8765 automatically
"""
import json, re, sys, threading, webbrowser
from datetime import datetime, timezone
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler

BASE = Path(__file__).parent
CARDS_DIR = BASE / "experiment-cards"
NOTES_FALLBACK = BASE / "notes.json"  # for experiments without a card yet
FAVORITES_FILE = BASE / "favorites.json"

NOTE_RE = re.compile(r"<!-- note ([\d\-T:\.Z]+) -->\n([\s\S]*?)(?=\n<!-- note |\Z)")


def parse_notes(section: str) -> list:
    """Parse timestamped entries from the notes section."""
    return [
        {"ts": m.group(1), "text": m.group(2).rstrip()}
        for m in NOTE_RE.finditer(section)
    ]


def render_notes(entries: list) -> str:
    """Render entries back to markdown."""
    parts = []
    for e in entries:
        parts.append(f"<!-- note {e['ts']} -->\n{e['text']}")
    return "\n\n".join(parts)


def get_notes_section(card_content: str) -> str:
    m = re.search(r"\n## 7\. Notes\n\n([\s\S]*?)$", card_content)
    return m.group(1) if m else ""


def read_notes(eid: str) -> list:
    card_path = CARDS_DIR / f"{eid}_card.md"
    if not card_path.exists():
        try:
            raw = json.loads(NOTES_FALLBACK.read_text()).get(eid, "")
            return parse_notes(raw) if raw else []
        except Exception:
            return []
    return parse_notes(get_notes_section(card_path.read_text()))


def append_note(eid: str, text: str) -> dict:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
    new_entry = {"ts": ts, "text": text.strip()}

    card_path = CARDS_DIR / f"{eid}_card.md"
    if not card_path.exists():
        try:
            raw = json.loads(NOTES_FALLBACK.read_text()) if NOTES_FALLBACK.exists() else {}
            entries = parse_notes(raw.get(eid, ""))
            entries.append(new_entry)
            raw[eid] = render_notes(entries)
            NOTES_FALLBACK.write_text(json.dumps(raw, indent=2, ensure_ascii=False))
        except Exception:
            return {"ok": False}
        return {"ok": True, "entry": new_entry}

    content = card_path.read_text()
    entries = parse_notes(get_notes_section(content))
    entries.append(new_entry)
    body = render_notes(entries)
    content = re.sub(r"\n## 7\. Notes\n[\s\S]*$", "", content).rstrip()
    content += "\n\n## 7. Notes\n\n" + body + "\n"
    card_path.write_text(content)
    return {"ok": True, "entry": new_entry}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/index.html"):
            content = (BASE / "viewer.html").read_bytes()
            self._respond(200, "text/html; charset=utf-8", content)
        elif self.path.startswith("/api/notes/"):
            eid = self.path[len("/api/notes/"):]
            self._json({"notes": read_notes(eid)})
        elif self.path == "/api/favorites":
            favs = json.loads(FAVORITES_FILE.read_text()) if FAVORITES_FILE.exists() else []
            self._json(favs)
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        if self.path.startswith("/api/notes/"):
            eid = self.path[len("/api/notes/"):]
            result = append_note(eid, json.loads(body).get("text", ""))
            self._json(result)
        elif self.path == "/api/favorites":
            favs = json.loads(body)
            FAVORITES_FILE.write_text(json.dumps(favs, indent=2, ensure_ascii=False))
            self._json({"ok": True})
        else:
            self.send_response(404)
            self.end_headers()

    def _respond(self, code, ctype, body: bytes):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", len(body))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, obj):
        body = json.dumps(obj).encode()
        self._respond(200, "application/json", body)

    def log_message(self, fmt, *args):
        pass


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    server = HTTPServer(("localhost", port), Handler)
    url = f"http://localhost:{port}"
    print(f"Viewer:      {url}")
    print(f"Notes saved to: *_card.md  (## 7. Notes section)")
    print("Press Ctrl-C to stop.\n")

    def open_browser():
        import time; time.sleep(0.4)
        webbrowser.open(url)

    threading.Thread(target=open_browser, daemon=True).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
