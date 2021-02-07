#!/usr/bin/python3.9

from http.server import BaseHTTPRequestHandler
import requests
from requests_cache import install_cache

install_cache("api_relaying_server_cache", backend="sqlite", expire_after=300)

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

	Instance methods
	----------------
	do_GET()
		Relays an incoming HTTP GET request to the remote server and sends back
		the response to the client.
	"""

	remote_server_url = "https://menu.dckube.scilifelab.se/api"

	def do_GET(self):
		"""Relays an incoming HTTP GET request to the remote server and sends back
		the response to the client."""
		try:
			# A Requests Cache has been created above. Calls to requests.get()
			# now automatically yield a cache lookup and fetch if the cache
			# entry exists and hasn't expired.
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
				# Response to client won't be compressed even if the remote server's
				# response to this middle server was compressed (the Python library
				# Requests being used automatically decompresses responses).
				if key.lower() == "content-encoding":
					self.send_header("Content-Encoding", "identity")
				else:
					self.send_header(key, response.headers[key])

			self.end_headers()

			# response.content is already decompressed.
			# TODO: Consider compressing large responses with gzip by using library
			# tools io.BytesIO() and gzip.GzipFile().
			self.wfile.write(response.content)
			self.wfile.flush()

		except:
			# This middle server is acting as a gateway so state that a
			# Bad Gateway error occurred.
			self.send_error(502, "Remote server didn't provide a proper response.")
