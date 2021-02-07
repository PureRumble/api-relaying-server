#!/usr/bin/python3.9

from http.server import HTTPServer
from socketserver import ThreadingMixIn

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	"""A class that represents a threaded HTTP server. It has the same API as
	the library class http.server.HTTPServer."""
	pass
