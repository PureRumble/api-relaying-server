#!/usr/bin/python3.9

from http.server import BaseHTTPRequestHandler
import requests

class ApiRelayingRequestHandler(BaseHTTPRequestHandler):
	"""
	A class used to create an api relaying middle server.
	This class specifies how the middle server should handle incoming requests.

	When a client request comes in, the server sends its own request
	to a remote server specified by static class variable remote_server_url.
	The server appends the path part of the client's specified URL
	to remote_server_url. The remote server's response is relayed
	back to the client.

	Static variables
	----------------

	remote_server_url : str
		An URL to the remote server. Change it to the desired remote server
		before using this class to create a server. The variable is not an
		instance variable since instances of this class are created internally
		by http.server.HTTPServer() in the Python library.
	"""

	remote_server_url = "https://menu.dckube.scilifelab.se/api"

	def do_GET(self):
		try:
			response = \
				requests.get(ApiRelayingRequestHandler.remote_server_url + self.path)

			# Don't send the raw bytes in the response back to the client since
			# an error occurs in web browsers if the middle server and remote server
			# use different incoming tcp ports. Instead, send all response parts
			# one by one as done here.

			if response.status_code is None or response.headers is None:
				# Type of error isn't important since it is immediately handled here.
				raise ConnectionError()

			self.send_response(response.status_code)

			for key in response.headers:
				self.send_header(key, response.headers[key])

			self.end_headers()

			self.wfile.write(response.content)

		except:
			# This middle server is acting as a gateway so state that a
			# Bad Gateway error occurred.
			self.send_error(502, "Remote server didn't provide a proper response.")
