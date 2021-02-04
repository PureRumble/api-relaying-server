#!/usr/bin/python3.9

from http.server import BaseHTTPRequestHandler
import requests

remote_server_url = "https://menu.dckube.scilifelab.se/api"

class ApiRelayingRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        response = requests.get(remote_server_url + self.path, stream=True)

        for curr_chunk in response.iter_content(chunk_size=256):
            self.wfile.write(curr_chunk)
