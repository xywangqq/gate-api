import urllib.request
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    API_URL = "https://www.vpngate.net/api/iphone/"

    def do_GET(self):
        try:
            req = urllib.request.Request(
                self.API_URL,
                headers={'User-Agent': 'Mozilla/5.0'},
            )
            with urllib.request.urlopen(req, timeout=8) as response:
                csv_data = response.read().decode('utf-8-sig')

            # 清洗：去掉注释行、表头、空行，并清理 CRLF
            cleaned_lines = []
            for line in csv_data.split('\n'):
                line = line.rstrip('\r')
                if not line.strip():
                    continue
                if line.startswith('*') or line.startswith('#'):
                    continue
                cleaned_lines.append(line)

            body = "\n".join(cleaned_lines)
            self._respond(200, body)

        except Exception as e:
            self._respond(502, f"Error connecting to data source: {e}")

    def _respond(self, status, body):
        # 先决定状态码和响应头，再写 body —— 顺序很重要
        self.send_response(status)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(body.encode('utf-8'))
