#!/usr/bin/python3.9

from http.server import BaseHTTPRequestHandler, HTTPServer
import requests

HOST_NAME = "localhost"
SERVER_PORT = 80
BASE_URL = "https://menu.dckube.scilifelab.se/api"

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        response = requests.get(BASE_URL + self.path, stream=True)

        for curr_chunk in response.iter_content(chunk_size=256):
            self.wfile.write(curr_chunk)

if __name__ == "__main__":
    webServer = HTTPServer((HOST_NAME, SERVER_PORT), MyServer)

    print("Starting server.")
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    print("Stopping server.")
    webServer.server_close()
