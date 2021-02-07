from argparse import ArgumentParser
from http.server import HTTPServer
from .api_relaying_request_handler import ApiRelayingRequestHandler

arg_parser = ArgumentParser(
	description="""
		Starts the api relaying middle server and begins to listen for incoming
		requests on the specified port.

		The server fetches an HTTP response from the remote server
		https://menu.dckube.scilifelab.se/api
		and relays it back to the middle server's client. The path part of the
		client's requested URL is added to the URL of the remote server. For example
		visiting http://localhost:8000/restaurant will give the response of
		https://menu.dckube.scilifelab.se/api/restaurant.

		Stop the server with Ctrl+C."""
)

arg_parser.add_argument(
	"--port",
	action="store",
	type=int,
	default=8000,
	help="The port nr that the server should listen on. Default value is 8000."
)

arg_parser.add_argument(
	"--interface",
	action="store",
	type=str,
	default="localhost",
	help="""The interface that the server should listen on. Value must be a
		valid IP address. Default value is localhost."""
)

parsed_args = arg_parser.parse_args()
port = parsed_args.port
interface = parsed_args.interface

relay_server = HTTPServer((interface, port), ApiRelayingRequestHandler)

print("Starting server. Stop with Ctrl+C.")
try:
    relay_server.serve_forever()
except KeyboardInterrupt:
    pass

print("Stopping server.")
relay_server.server_close()
