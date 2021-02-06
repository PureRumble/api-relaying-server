**Arash Bazrafshan**

## Task 1

# Description
`api_relaying_server` is a Python module for running an API relaying middle
server.

The server fetches an HTTP response from the remote server
https://menu.dckube.scilifelab.se/api
and relays it back to the middle server's client.

The path part of the client's
requested URL is added to the URL of the remote server. For example visiting
http://localhost:8000/restaurant will give the response of
https://menu.dckube.scilifelab.se/api/restaurant.

# Requirements
* Python (ver. >= 3.9.1)
* Python HTTP library Requests (ver. >= 2.25.1, https://requests.readthedocs.io/)

Older version of Python (ver. >= 3) and Requests may work. Run the tests to
verify (see below).

# How to run server
Start the API relaying middle server by running the following from the
repository root:

```
cd python_source_files
# python -m api_relaying_server -h for documentation
python -m api_relaying_server
```

The server now runs on http://localhost:8000 and
http://localhost:8000/restaurant can be visited from a browser.

# How to run tests
Run the tests by running the following from the repository root:

```
cd python_source_files
python -m unittest
```
