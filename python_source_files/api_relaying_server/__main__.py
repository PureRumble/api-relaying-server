from argparse import ArgumentParser
from http.server import HTTPServer
from .api_relaying_request_handler import ApiRelayingRequestHandler

arg_parser = ArgumentParser(
	description="""
	Starts the api relaying middle server and begins to listen for incoming
	requests on the specified port. Stop with Ctrl+C."""
)

arg_parser.add_argument(
	"--port",
	action="store",
	type=int,
	default=8000,
	help="The port nr that the server should listen on. Default value is 8000."
)

port = arg_parser.parse_args().port

relay_server = HTTPServer(("localhost", port), ApiRelayingRequestHandler)

print("Starting server.")
try:
    relay_server.serve_forever()
except KeyboardInterrupt:
    pass

print("Stopping server.")
relay_server.server_close()
