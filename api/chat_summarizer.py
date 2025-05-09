from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        try:
            data = json.loads(body)
            messages = data.get("messages", [])
            summary = data.get("summary", "")
        except:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Invalid JSON')
            return

        reply = {
            "status": "ok",
            "summary_used": summary,
            "message_count": len(messages),
            "response": "Esto es una respuesta de prueba del resumen 🧠"
        }

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(reply).encode())
