**Arash Bazrafshan**

# Requirements
* Python (ver. >= 3.9.1)
* Python HTTP library Requests (ver. >= 2.25.1)
* Python HTTP caching library Requests-Cache (ver. >= 0.5.2)
* Docker (ver. >= 20.10.3)

Older version of Python (ver. >= 3) may work. Run the tests to verify
(see below). Older version of Docker may also work. The required Python
libraries are installed automatically if you build the Docker image.

# Python virtual environment
It is recommended to use a Python virtual environment with a wrapper to run this
module directly on the host (and not in a Docker container). See https://realpython.com/python-virtual-environments-a-primer/.

When installing the Virtual Environment Wrapper module, remember that it must
be installed for Python 3.9, so run the following:

```
python3.9 -m pip install virtualenvwrapper
```

# Installing requirements

Run the following to install the required Python libraries if the API
relaying server is to be run directly on the host (and not inside the Docker
container):

```
python -m pip install requests
python -m pip install requests-cache
```

# Task 1 - API relaying server

## Description
`api_relaying_server` is a Python module for running an API relaying middle
server.

The server fetches an HTTP response from the remote server
https://menu.dckube.scilifelab.se/api
and relays it back to the middle server's client.

The path part of the client's
requested URL is added to the URL of the remote server. For example visiting
http://localhost:8000/restaurant will give the response of
https://menu.dckube.scilifelab.se/api/restaurant.

## How to run server
Start the API relaying middle server by running the following from the
repository root:

```
cd python_source_files
# python -m api_relaying_server -h for documentation
python -m api_relaying_server
```

The server now runs on http://localhost:8000 and
http://localhost:8000/restaurant can be visited from a browser.

## How to run tests
Run the tests by running the following from the repository root:

```
cd python_source_files
python -m unittest
```

## Known issues
A Broken Pipe Error may occur in the Python app when sending a request to
http://localhost:8000/restaurant. The error will not stop the server and it will continue to function.


# Task 2 - Docker container

## Description
The api relaying server can now be placed in a Docker image and run from a
container.

## How to build Docker image
Build the Docker image by running the following from the repository root:

```
sudo docker build -t api_relaying_server .
```

## How to run server in container
Start the image in a container by running the following. The command will output
the container id. Copy the id.

```
sudo docker -d --rm -p 8000:8000 api_relaying_server
```

## How to connect to server
Find and copy the IP address of the container's interface by running the
following:

```
sudo docker container inspect [container_id] | grep -i '"ipaddress":'
```

Connect to the server by visiting http://[container_ip_addr]:8000  in a browser.


# Task 4 - Caching HTTP responses

The api relaying server caches HTTP responses from the remote server. This is
verified by unit tests.


# Task 5 - Making relaying server multi-threaded

The API relaying server handles each request in separate thread. This is
verified by unit tests.
