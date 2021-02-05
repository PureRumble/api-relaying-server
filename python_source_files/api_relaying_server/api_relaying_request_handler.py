#!/usr/bin/python3.9

from http.server import BaseHTTPRequestHandler
import requests



class ApiRelayingRequestHandler(BaseHTTPRequestHandler):
	remote_server_url = "https://menu.dckube.scilifelab.se/api"

	def do_GET(self):
		try:
			response = requests.get(ApiRelayingRequestHandler.remote_server_url + self.path)

			if response.status_code is None or response.headers is None:
				raise ConnectionError()

			self.send_response(response.status_code)

			for key in response.headers:
				self.send_header(key, response.headers[key])

			self.end_headers()

			self.wfile.write(response.content)

		except:
			self.send_error(502, "Remote server didn't provide proper response.")
