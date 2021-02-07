#!/usr/bin/python3.9

import unittest
from time import sleep
from io import BytesIO
from gzip import GzipFile
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
import requests_cache
import requests
from api_relaying_server import ApiRelayingRequestHandler



def setUpModule():
	# Start the relaying server and the mockup remote server for tests
	start_server_thread(8000, ApiRelayingRequestHandler)
	start_server_thread(8001, MockupRequestHandler)
	ApiRelayingRequestHandler.remote_server_url = "http://localhost:8001"

	# Make sure servers have finished starting up before running tests.
	sleep(1)



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

class MockupRequestHandler(BaseHTTPRequestHandler):
	"""
	A class that handles incoming requests to the remote mockup server. How the
	requests are handled for each test can be changed by redefining the static
	class method handle_request().

	Static methods
	----------------
	handle_request
		Handles an incoming request. Does nothing per default.

	Instance methods
	----------------
	do_GET
		Handles the client's GET request.
	"""

	@staticmethod
	def handle_request(req):
		"""Handles an incoming request by using the provided request handler.
		This method does nothing per default. Redefine it in each test to decide
		how the remote mockup server should respond to a request.

		Parameters
		----------
		req : MockupRequestHandler
			The request handler to be used to handle the incoming request.
		"""
		pass

	def do_GET(self):
		"""Handles the client's GET request."""
		MockupRequestHandler.handle_request(self)



class TestApiRelayingServer(unittest.TestCase):
	"""
	A class used to test the module api_relaying_server.
	"""

	def test_receive_resp_from_relaying_server(req):
		"""Tests that the server can relay the request and response
		back and forth."""

		# This is a locally defined func. Make the remote mockup server to send
		# back the path part of the client's requested URL so it can be verified
		# that the server received it. Compress the reply with gzip to verify
		# that the relaying server can handle this.
		def handle_request(req):
			req.send_response(200)
			req.send_header("Content-Type", "text/html; charset=utf-8")
			req.send_header("Content-Encoding", "gzip")
			req.end_headers()

			bytesIO = BytesIO()
			with GzipFile(fileobj=bytesIO, mode='w', compresslevel=5) as p:
				p.write(req.path.encode("utf-8"))

			req.wfile.write(bytesIO.getvalue())
			req.wfile.flush()


		MockupRequestHandler.handle_request = staticmethod(handle_request)

		response = requests.get("http://localhost:8000/going-back-and-forth")
		requests_cache.clear()
		req.assertEqual(response.text, "/going-back-and-forth")


	def test_relaying_server_checks_cache(req):
		"""Tests that the server uses the cache for repeated lookups."""

		# This is a locally defined func. Make the remote mockup server to count
		# the number of incoming requests, since each request means the relaying
		# server got a cache miss.
		nr_cache_misses = 0
		def handle_request(req):
			nonlocal nr_cache_misses
			# This func is called when remote mockup server receives a request.
			# So a cache miss has occurred.
			nr_cache_misses += 1

			req.send_response(200)
			req.send_header("Content-Type", "text/html; charset=utf-8")
			req.send_header("Content-Encoding", "identity")
			req.end_headers()

			req.wfile.write("Nothing to see here!".encode("utf-8"))
			req.wfile.flush()

		MockupRequestHandler.handle_request = staticmethod(handle_request)

		requests.get("http://localhost:8000")
		sleep(1)
		requests.get("http://localhost:8000")

		requests_cache.clear()

		req.assertEqual(nr_cache_misses, 1)


	def test_relaying_server_skips_cache_for_new_URL(req):
		"""Tests that the server skips cache when new URL is requested."""

		# This is a locally defined func. Make the remote mockup server to count
		# the number of incoming requests, since each request means the relaying
		# server got a cache miss.
		nr_cache_misses = 0
		def handle_request(req):
			nonlocal nr_cache_misses
			# This func is called when remote mockup server receives a request.
			# So a cache miss has occurred.
			nr_cache_misses += 1

			req.send_response(200)
			req.send_header("Content-Type", "text/html; charset=utf-8")
			req.send_header("Content-Encoding", "identity")
			req.end_headers()

			req.wfile.write("Nothing to see here!".encode("utf-8"))
			req.wfile.flush()

		MockupRequestHandler.handle_request = staticmethod(handle_request)

		requests.get("http://localhost:8000")
		sleep(1)
		requests.get("http://localhost:8000/request-skips-cache")
		requests_cache.clear()

		req.assertEqual(nr_cache_misses, 2)



if __name__ == "__main__":

	unittest.main()
