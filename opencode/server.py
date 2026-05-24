import http.server
import os
import sys
import urllib.request
import json

os.chdir(r'C:\Users\katak\AppData\Local\Temp\opencode')

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/calendar':
            self.proxy_calendar()
        else:
            super().do_GET()

    def proxy_calendar(self):
        try:
            req = urllib.request.Request(
                'https://economic-calendar.tradingview.com/events',
                headers={
                    'User-Agent': 'Mozilla/5.0',
                    'Origin': 'https://www.tradingview.com',
                    'Referer': 'https://www.tradingview.com/'
                }
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = resp.read()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Cache-Control', 'max-age=300')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(data)
        except Exception as e:
            self.send_response(502)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def log_message(self, format, *args):
        msg = format % args if args else format
        sys.stderr.write(f"[{self.log_date_time_string()}] {msg}\n")

http.server.HTTPServer(('0.0.0.0', 8080), Handler).serve_forever()
