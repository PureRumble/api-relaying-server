"""
A module for running an API relaying middle server.

The server fetches an HTTP response from the remote server
https://menu.dckube.scilifelab.se/api
and relays it back to the middle server's client. The path part of the client's
requested URL is added to the URL of the remote server. For example visiting
http://localhost:8000/restaurant will give the response of
https://menu.dckube.scilifelab.se/api/restaurant.

Exported items
--------------

ApiRelayingRequestHandler : class
	An HTTP request handler used to run the middle server.
"""

from .api_relaying_request_handler import ApiRelayingRequestHandler
