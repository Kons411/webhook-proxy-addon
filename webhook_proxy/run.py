from http.server import BaseHTTPRequestHandler, HTTPServer
import requests

WEBHOOK_URL = "http://homeassistant.local:8123/api/webhook/klingel"

class WebhookHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/klingel-bridge":
            print("Webhook empfangen! → sende POST an Home Assistant")
            try:
                requests.post(WEBHOOK_URL, timeout=2)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"OK")
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode())
        else:
            self.send_response(404)
            self.end_headers()

def run():
    server_address = ('', 8888)
    httpd = HTTPServer(server_address, WebhookHandler)
    print("Webhook Proxy läuft auf Port 8888")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
