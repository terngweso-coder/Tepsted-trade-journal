import http.server
import os
os.chdir(r'C:\Users\katak\AppData\Local\Temp\opencode')
http.server.test(HandlerClass=http.server.SimpleHTTPRequestHandler, port=8080)
