import urllib.request
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 1. 允许跨域（CORS），保证您的 Android 客户端能正常读取数据
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        try:
            # 2. 从海外 Vercel 服务器抓取官方公共节点源
            url = "http://vpngate.net"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            
            with urllib.request.urlopen(req, timeout=8) as response:
                csv_data = response.read().decode('utf-8')
                
                # 3. 数据清洗：去掉空行和无用注释，帮国内用户的 App 节省加载流量
                cleaned_lines = []
                for line in csv_data.split('\n'):
                    if line.startsWith('*') or line.strip() == "":
                        continue
                    cleaned_lines.append(line)
                
                # 4. 把干净的节点列表发给手机客户端
                result = "\n".join(cleaned_lines)
                self.wfile.write(result.encode('utf-8'))
                
        except Exception as e:
            self.wfile.write(f"Error connecting to data source: {str(e)}".encode('utf-8'))
