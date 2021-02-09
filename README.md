**Arash Bazrafshan**

# Requirements
* Python (ver. >= 3.9.1)
* Python HTTP module Requests (ver. >= 2.25.1)
* Python HTTP caching module Requests-Cache (ver. >= 0.5.2)
* SQLite (ver. >= 3.34.1, included in CPython)
* Docker (ver. >= 20.10.3)

Older version of Python (ver. >= 3) may work. Run the tests to verify
(see below). Older version of Docker may also work. The required Python
modules are installed automatically if you build the Docker image.

# Python virtual environment
It is recommended to use a Python virtual environment with a wrapper to run this
module directly on the host (and not in a Docker container). See
https://realpython.com/python-virtual-environments-a-primer/.

When installing the Virtual Environment Wrapper module, remember that it must
be installed for Python 3.9, so run the following:

```
python3.9 -m pip install virtualenvwrapper
```

# Installing requirements

Run the following to install the required Python modules if the API
relaying server is to be run directly on the host (and not inside the Docker
container):

```
python -m pip install requests
python -m pip install requests-cache
```

SQLite (not a Python module) must also be installed on the system OS if CPython
is not used.

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


# Task 3 - Dish shell tool

A shell tool is available for listing restaurants or the dishes of a selected
one. The API relaying server must be running on localhost:8000 to use the shell
tool.

Start the relaying server in the background by running the following from the
repository root:

```
cd python_source_files
python -m api_relaying_server &
```

List all restaurants by running the following:

```
python dish_shell_tool/list_dishes.py
```

Note the identifier of desired restaurant and list its dishes by running the
following:

```
python dish_shell_tool/list_dishes.py --restaurant [identifier]
```

The shell tool can also be used by running `./list_dishes.py` if no Python
virtual environment is being used.


# Task 4 - Caching HTTP responses

The API relaying server caches HTTP responses from the remote server. This is
verified by unit tests.


# Task 5 - Making relaying server multi-threaded

The API relaying server handles each request in separate thread. This is
verified by unit tests.


# Task 6 - Performing load test

Seven load tests of the API relaying server were performed using Locust. HTTP
caching was extended to one hour for testing purposes.

The URI root http://localhost:8000/ was the target of all load tests. The
HTTP reply is 351 bytes.

The tests were performed on a Intel Core i7-6700HQ CPU, 2.60 GHz, 4 cores.
Primary memory was never fully utilized during testing.

## Pre-analysis

The SQLite database for the HTTP cache was 20.5 kB with its single cache entry.
Since the amount of data to be transferred per connection was nearly minimal,
the main bottle necks of this test were CPU speed, CPU core count and system
memory read/write data speeds (from the cores L1 caches down to RAM memory).

The popular CPython implementation of Python inherently forbids multiple
threads from simultaneously executing Python code. This is due to that CPythons
handling of memory management, including shared global and non-local variables,
is not thread safe.

This limitation can be overcome by spawning processes instead of threads in
a Python app. The use of inter-process shared memory is broken however. E.g.
other processes may not see changes made to a global or nonlocal variable by a
process.

## Results and analysis for multi threads

These are the results of the first five load tests. The spawned users sent
requests concurrently and repeatedly without delays after each response.

| Nr users | Reqs/s handled | Avg resp time |
| - | - | - |
| 10 | 135 | 73 |
| 50 | 433 | 113 |
| 100 | 539 | 182 |
| 150 | 536 | 275 |
| 200 | 529 | 371 |

Optimal number of concurrent users is somewhere between 50 and 100, since
the request handling speed does not increase for 150 and 200 concurrent users
but the average time each user must wait does increase.

Only one CPU core was used to serve the incoming requests since the relaying
server uses multiple threads instead of multiple processes.

## Using multiple processes

To attempt to increase performance, the relaying server and tests were changed
to use multiple processes so all CPU cores could be utilized.

### Changes to relaying server

The app's server class' definition was changed from
```
ThreadedHTTPServer(ThreadingMixIn, HTTPServer)
```
to
```
ThreadedHTTPServer(ForkingMixIn, HTTPServer)
```
(this change is _not_ included in the git repository's master HEAD). In both
cases the first parent class overrides instance methods in the second
`HTTPServer`. In the latter case those overriding methods spawn new processes
instead of threads to handle requests.

### Changes to test run

To avoid Locust hitting the performance limit of a single CPU core in the new
test runs, the Locust test setup was changed to use multiple processes too by
running a master process and four worker processes. This was done by executing
`locust --master` once and `locust --worker` four times from _five different
bash processes_ (e.g. by running them from different console windows).

### Unit test results

One unit test that verifies that the client receives expected response from
the relaying server succeeded. Other unit tests test cache and multiple thread
usage. These fail due to using nonlocal variables for verification.

### Test results and analysis

These are the results of the final two load tests that used multiple processes.

| Nr users | Reqs/s handled | Avg resp time |
| - | - | - |
| 200  | 812 | 49 |
| 300 | 805 | 49 |

Performance has greatly increased by 53% and average response time reduced by
atleast 33%. Optimal number of concurrent users is below 200. The request
handling speed slightly reduced for 300 users and response time did not change.

## Conclusions

Performance greatly increased by all metrics thanks to using multiple processes.
It is strange that average response time did not increase in the multiple
processes tests when going from 200 to 300 users.

Processed request count per second would further increase on a system with
multiple CPUs or greater CPU and core cache sizes. Scaling beyond that would
require a web server cluster setup.

A different database than SQLite can be used for storing the HTTP cache to
achieve greater cache size and performance under heavy load. The Python module
Requests Cache used by the relaying server supports different database
platforms.

When using a web server cluster it would be ideal if they all used the same HTTP
cache reservoir for improved end user experience quality (otherwise one web
server node may have an older HTTP cache entry than other nodes). A separate
Mongo DB cluster could serve the reservoir. Mongo DB provides automatic memory
and performance load balancing among its nodes and is supported by Requests
Cache.

## Test limitations

The main limit of these tests is that all user requested only the same small
amount of data from the server. Larger and more varied data requests  would
cause an increase in CPU and core cache misses and possibly even force secondary
virtual memory access (i.e. hard drive) instead of only primary memory access.
