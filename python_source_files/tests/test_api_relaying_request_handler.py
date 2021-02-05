#!/usr/bin/python3.9

import unittest
from time import sleep
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
import requests
from api_relaying_server import ApiRelayingRequestHandler



class TestRequestHandler(BaseHTTPRequestHandler):

	def do_GET(self):

		self.send_response(200)
		self.send_header("Content-type", "text/html; charset=utf-8")
		self.end_headers()
		self.wfile.write(self.path.encode("utf-8"))



class TestApiRelayingServer(unittest.TestCase):

	@staticmethod
	def start_server_thread(port_nr, req_handler_cls):

		server = HTTPServer(("localhost", port_nr), req_handler_cls)
		thread = Thread(target=server.serve_forever)
		thread.setDaemon(True)
		thread.start()

		return thread

	def test_read_temps_from_file(self):
		global remote_server_url

		TestApiRelayingServer.start_server_thread(8001, TestRequestHandler)

		ApiRelayingRequestHandler.remote_server_url = "http://localhost:8001"
		TestApiRelayingServer.start_server_thread(8000, ApiRelayingRequestHandler)

		sleep(1)

		response = requests.get("http://localhost:8000/package-on-the-run")
		self.assertEqual(response.text, "/package-on-the-run")



if __name__ == "__main__":
	unittest.main()
