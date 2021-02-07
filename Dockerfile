FROM python:3.9.1

WORKDIR /python_source_files

COPY python_source_files/requirements.txt .

RUN pip install -r requirements.txt

ADD python_source_files/api_relaying_server api_relaying_server

# Make server to listen on all interfaces (i.e. 0.0.0.0) so it can run in a
# container that uses a bridged network connection to its host.
ENTRYPOINT ["python", "-m", "api_relaying_server", "--interface", "0.0.0.0"]
