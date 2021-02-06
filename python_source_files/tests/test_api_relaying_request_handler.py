#!/usr/bin/python3.9

import unittest
from time import sleep
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
import requests
from api_relaying_server import ApiRelayingRequestHandler



class MockupRequestHandler(BaseHTTPRequestHandler):
	"""
	A class used to create a remote mockup server. The server gives a valid
	HTTP response. The response's text is the path part of the client's
	requested URL.

	Instance methods
	----------------
	do_GET
		Handles the client's GET request.
	"""

	def do_GET(self):
		"""Handles the client's GET request."""

		self.send_response(200)
		self.send_header("Content-type", "text/html; charset=utf-8")
		self.end_headers()
		# The path part of the client's requested URL is sent back so it can be
		# verified that the mockup server received it.
		self.wfile.write(self.path.encode("utf-8"))



class TestApiRelayingServer(unittest.TestCase):
	"""
	A class used to test the module api_relaying_server.

	Static methods
	--------------
	start_server_thread(port_nr, req_handler_cls)
		Starts a thread that runs a server using the provided request handler class.
	"""
	@staticmethod
	def start_server_thread(port_nr, req_handler_cls):
		"""Starts a thread that runs a server using the provided request handler
		class.

		Parameters
		----------
		port_nr : int
			The TCP port where the server should listen to incoming requests.

		req_handler_cls: subclass of BaseHTTPRequestHandler
		 	The request handler class to be used to handle incoming requests.

		Returns
		-------
		(server, thread)
			The created server and thread
		"""
		server = HTTPServer(("localhost", port_nr), req_handler_cls)
		thread = Thread(target=server.serve_forever)
		# The created thread should be stopped when the parent thread stops.
		thread.daemon = True
		thread.start()

		return server, thread

	def test_read_temps_from_file(self):
		"""Tests that the middle server can relay the request and response
		back and forth."""

		# Create the remote mockup server and the middle server.
		test_server, test_thread = \
			TestApiRelayingServer.start_server_thread(8001, MockupRequestHandler)

		ApiRelayingRequestHandler.remote_server_url = "http://localhost:8001"
		middle_server, middle_server_thread = \
			TestApiRelayingServer.start_server_thread(8000, ApiRelayingRequestHandler)

		# Make sure the servers have finished starting up.
		sleep(1)

		response = requests.get("http://localhost:8000/going-back-and-forth")
		self.assertEqual(response.text, "/going-back-and-forth")

		# The servers and threads are automatically stopped when this test
		# finishes.



if __name__ == "__main__":
	unittest.main()
