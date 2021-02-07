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
* Python HTTP library Requests (ver. >= 2.25.1)

Older version of Python (ver. >= 3) may work. Run the tests to verify
(see below).

# Python virtual environment
It is recommended to use a Python virtual environment with a wrapper to run this
module. See https://realpython.com/python-virtual-environments-a-primer/.

When installing the Virtual Environment Wrapper module, remember that it must
be installed for Python 3.9, so run the following:

```
python3.9 -m pip install virtualenvwrapper
```

# How to install Requests
Install the Python HTTP library Requests by running the following:

```
python -m pip install requests
```

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



## Task 2

# Description
The api relaying server can now be placed in a Docker image and run from a
container.

# Requirements
* Docker (ver. >= 20.10.3)

Older version of Docker may work.

# How to build Docker image
Build the Docker image by running the following from the repository root:

```
sudo docker build -t api_relaying_server .
```

# How to run server in container
Start the image in a container by running the following. The command will output
the container id. Copy the id.

```
sudo docker -d --rm -p 8000:8000 api_relaying_server
```

# How to connect to server
Find and copy the IP address of the container's interface by running the
following:

```
sudo docker container inspect [container_id] | grep -i '"ipaddress":'
```

Connect to the server by visiting http://[container_ip_addr]:8000  in a browser.

# Known issues
A Broken Pipe Error may occur in the Python app when sending a request to the
server, especially when requesting http://[container_ip_addr]:8000/restaurant.
The error will not stop the server and it will continue to function.

The error seems to be an unresolved bug in Docker that appears in different
scenarios:

* https://github.com/docker/compose/issues/1509
* https://github.com/docker/docker-py/issues/1824
