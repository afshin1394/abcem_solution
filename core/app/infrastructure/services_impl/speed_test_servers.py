#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2012 Matt Martz
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import argparse
import csv
import datetime
import errno
import math
import os
import platform
import re
import signal
import socket
import sys
import threading
import timeit
import xml.etree.ElementTree as ET
from hashlib import md5
from io import BytesIO, StringIO
import gzip
import ssl
import json

from queue import Queue
from typing import Dict, Any
from urllib.error import URLError, HTTPError
from urllib.parse import urlparse, parse_qs
from urllib.request import (
    urlopen, Request,
    ProxyHandler, HTTPDefaultErrorHandler, HTTPRedirectHandler,
    HTTPErrorProcessor, OpenerDirector, AbstractHTTPHandler
)
from http.client import HTTPConnection, HTTPSConnection, BadStatusLine

__version__ = '2.1.4b1'


# Exceptions
class SpeedtestException(Exception):
    """Base exception for this module"""


class SpeedtestCLIError(SpeedtestException):
    """Generic exception for raising errors during CLI operation"""


class SpeedtestHTTPError(SpeedtestException):
    """Base HTTP exception for this module"""


class SpeedtestConfigError(SpeedtestException):
    """Configuration XML is invalid"""


class SpeedtestServersError(SpeedtestException):
    """Servers XML is invalid"""


class ConfigRetrievalError(SpeedtestHTTPError):
    """Could not retrieve config.php"""


class ServersRetrievalError(SpeedtestHTTPError):
    """Could not retrieve speedtest-servers.php"""


class InvalidServerIDType(SpeedtestException):
    """Server ID used for filtering was not an integer"""


class NoMatchedServers(SpeedtestException):
    """No servers matched when filtering"""


class SpeedtestMiniConnectFailure(SpeedtestException):
    """Could not connect to the provided speedtest mini server"""


class InvalidSpeedtestMiniServer(SpeedtestException):
    """Server provided as a speedtest mini server does not actually appear
    to be a speedtest mini server
    """


class ShareResultsConnectFailure(SpeedtestException):
    """Could not connect to speedtest.net API to POST results"""


class ShareResultsSubmitFailure(SpeedtestException):
    """Unable to successfully POST results to speedtest.net API after
    connection
    """


class SpeedtestUploadTimeout(SpeedtestException):
    """testlength configuration reached during upload
    Used to ensure the upload halts when no additional data should be sent
    """


class SpeedtestBestServerFailure(SpeedtestException):
    """Unable to determine best server"""


class SpeedtestMissingBestServer(SpeedtestException):
    """get_best_server not called or not able to determine best server"""


# HTTP/Network errors to catch in one tuple
HTTP_ERRORS = (
    HTTPError,
    URLError,
    socket.error,
    ssl.SSLError,
    BadStatusLine,
    ssl.CertificateError
)


def get_exception():
    """Helper for retrieving the current exception info in an except block."""
    return sys.exc_info()[1]


class FakeShutdownEvent:
    """Class to fake a threading.Event.isSet so that users of this module
    are not required to register their own threading.Event()
    """

    @staticmethod
    def is_set():
        return False


# Debug printing
DEBUG = False


def printer(string, quiet=False, debug=False, error=False, **kwargs):
    """
    Helper function that prints a string, optionally hiding output if `quiet`
    is True, or using stderr if `error` is True.
    """
    global DEBUG
    if debug and not DEBUG:
        return

    if debug:
        # Show debug prefix in color if terminal
        if sys.stdout.isatty():
            out = f"\033[1;30mDEBUG: {string}\033[0m"
        else:
            out = f"DEBUG: {string}"
    else:
        out = string

    if not quiet:
        if error:
            print(out, file=sys.stderr, **kwargs)
        else:
            print(out, **kwargs)


def build_user_agent():
    """Build a Mozilla/5.0 compatible User-Agent string"""
    ua_tuple = (
        "Mozilla/5.0",
        f"({platform.platform()}; U; {platform.architecture()[0]}; en-us)",
        f"Python/{platform.python_version()}",
        "(KHTML, like Gecko)",
        f"speedtest-cli/{__version__}"
    )
    user_agent = " ".join(ua_tuple)
    printer(f"User-Agent: {user_agent}", debug=True)
    return user_agent


def distance(origin, destination):
    """Determine distance between 2 sets of [lat,lon] in km"""
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371.0  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
            math.sin(dlat / 2) * math.sin(dlat / 2)
            + math.cos(math.radians(lat1))
            * math.cos(math.radians(lat2))
            * math.sin(dlon / 2)
            * math.sin(dlon / 2)
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d


class SpeedtestHTTPConnection(HTTPConnection):
    """
    Custom HTTPConnection to support source_address and consistent timeouts
    for Python 3.
    """

    def __init__(self, *args, source_address=None, timeout=10, **kwargs):
        super().__init__(*args, **kwargs)
        self._tunnel_host = None
        self.source_address = source_address
        self.timeout = timeout

    def connect(self):
        if self.source_address:
            self.sock = socket.create_connection(
                (self.host, self.port),
                self.timeout,
                self.source_address
            )
        else:
            self.sock = socket.create_connection((self.host, self.port), self.timeout)
        if self._tunnel_host:
            self._tunnel()


class SpeedtestHTTPSConnection(HTTPSConnection):
    """
    Custom HTTPSConnection to support source_address and consistent timeouts
    for Python 3.
    """

    def __init__(self, *args, source_address=None, timeout=10, **kwargs):
        super().__init__(*args, **kwargs)
        self._tunnel_host = None
        self.source_address = source_address
        self.timeout = timeout

    def connect(self):
        if self.source_address:
            self.sock = socket.create_connection(
                (self.host, self.port),
                self.timeout,
                self.source_address
            )
        else:
            self.sock = socket.create_connection((self.host, self.port), self.timeout)

        if self._tunnel_host:
            self._tunnel()

        # Wrap socket for SSL
        if hasattr(self, "_context"):
            # Python 3.4+ style
            kwargs = {}
            server_hostname = self._tunnel_host or self.host
            self.sock = self._context.wrap_socket(self.sock, server_hostname=server_hostname, **kwargs)
        else:
            # Fallback if _context is not available (very old Python 3)
            self.sock = ssl.wrap_socket(self.sock)


def _build_connection(conn_cls, source_address, timeout, context=None):
    """
    Factory returning a callable used by Speedtest(HTTP|HTTPS)Handler's
    do_open() method to produce the custom connection object.
    """

    def inner(host, **kwargs):
        kwargs.update({
            'source_address': source_address,
            'timeout': timeout
        })
        if context:
            kwargs['context'] = context
        return conn_cls(host, **kwargs)

    return inner


class SpeedtestHTTPHandler(AbstractHTTPHandler):
    """
    Custom HTTP handler to build an HTTPConnection with source_address
    and timeout support.
    """

    def __init__(self, debuglevel=0, source_address=None, timeout=10):
        super().__init__(debuglevel=debuglevel)
        self.source_address = source_address
        self.timeout = timeout

    def http_open(self, req):
        return self.do_open(
            _build_connection(SpeedtestHTTPConnection, self.source_address, self.timeout),
            req
        )


class SpeedtestHTTPSHandler(AbstractHTTPHandler):
    """
    Custom HTTPS handler to build an HTTPSConnection with source_address
    and timeout support.
    """

    def __init__(self, debuglevel=0, context=None, source_address=None, timeout=10):
        super().__init__(debuglevel=debuglevel)
        self._context = context
        self.source_address = source_address
        self.timeout = timeout

    def https_open(self, req):
        return self.do_open(
            _build_connection(SpeedtestHTTPSConnection, self.source_address, self.timeout, context=self._context),
            req
        )


def build_opener(source_address=None, timeout=10):
    """Create a specialized OpenerDirector with our custom handlers."""
    printer(f"Timeout set to {timeout}", debug=True)
    if source_address:
        printer(f"Binding to source address: {(source_address, 0)}", debug=True)

    handlers = [
        ProxyHandler(),
        SpeedtestHTTPHandler(source_address=source_address, timeout=timeout),
        SpeedtestHTTPSHandler(source_address=source_address, timeout=timeout),
        HTTPDefaultErrorHandler(),
        HTTPRedirectHandler(),
        HTTPErrorProcessor()
    ]
    opener = OpenerDirector()
    opener.addheaders = [("User-agent", build_user_agent())]

    for h in handlers:
        opener.add_handler(h)
    return opener


class GzipDecodedResponse(gzip.GzipFile):
    """
    A file-like object to decode a response encoded with gzip.
    """

    def __init__(self, response):
        # We read everything into memory (BytesIO) so that GzipFile can seek
        buf = BytesIO(response.read())
        super().__init__(fileobj=buf, mode='rb')

    def close(self):
        super().close()


def get_response_stream(response):
    """
    Return a GzipDecodedResponse if the server sent 'content-encoding: gzip',
    otherwise return `response` as-is.
    """
    if response.getheader('content-encoding') == 'gzip':
        return GzipDecodedResponse(response)
    return response


def build_request(url, data=None, headers=None, bump='0', secure=False):
    """
    Build a Request object (from urllib) with some default headers and a
    query parameter for cache-busting.
    """
    if headers is None:
        headers = {}

    scheme = "https" if secure else "http"
    if url.startswith("://"):
        full_url = f"{scheme}{url}"
    else:
        full_url = url

    delim = '&' if '?' in full_url else '?'
    # Add a cache-buster to the URL
    final_url = f"{full_url}{delim}x={int(timeit.time.time() * 1000)}.{bump}"

    headers.update({"Cache-Control": "no-cache"})

    printer(f"{'POST' if data else 'GET'} {final_url}", debug=True)
    return Request(final_url, data=data, headers=headers)


def catch_request(request, opener=None):
    """Catch common exceptions while attempting to open a request."""
    _open = opener.open if opener else urlopen
    try:
        uh = _open(request)
        if request.full_url != uh.geturl():
            printer(f"Redirected to {uh.geturl()}", debug=True)
        return uh, False
    except HTTP_ERRORS:
        return None, get_exception()


def print_dots(shutdown_event):
    """A simple status callback that prints '.' during threaded tests."""

    def inner(current, total, start=False, end=False):
        if shutdown_event.is_set():
            return
        sys.stdout.write('..')
        if current + 1 == total and end is True:
            sys.stdout.write('\n')
        sys.stdout.flush()

    return inner


def do_nothing(*_args, **_kwargs):
    """Callback that does nothing (for quiet mode)."""
    pass


class HTTPDownloader(threading.Thread):
    """Thread that downloads data for the speed test."""

    def __init__(self, i, request, start, timeout, opener=None, shutdown_event=None):
        super().__init__()
        self.request = request
        self.result = [0]
        self.starttime = start
        self.timeout = timeout
        self.i = i
        self._opener = opener.open if opener else urlopen
        self._shutdown_event = shutdown_event or FakeShutdownEvent()

    def run(self):
        try:
            if (timeit.default_timer() - self.starttime) <= self.timeout:
                with self._opener(self.request) as f:
                    while (not self._shutdown_event.is_set() and
                           (timeit.default_timer() - self.starttime) <= self.timeout):
                        chunk = f.read(10240)
                        self.result.append(len(chunk))
                        if len(chunk) == 0:
                            break
        except (IOError, *HTTP_ERRORS):
            pass


class HTTPUploaderData:
    """File-like object for controlling how data is read during an upload."""

    def __init__(self, length, start, timeout, shutdown_event=None):
        self.length = length
        self.start = start
        self.timeout = timeout
        self._shutdown_event = shutdown_event or FakeShutdownEvent()
        self._data = None
        self.total = [0]

    def pre_allocate(self):
        chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        multiplier = int(round(int(self.length) / 36.0))
        # Pre-allocate data
        try:
            self._data = BytesIO(
                f"content1={(chars * multiplier)[0: self.length - 9]}".encode('utf-8')
            )
        except MemoryError:
            raise SpeedtestCLIError(
                "Insufficient memory to pre-allocate upload data. "
                "Use --no-pre-allocate if needed."
            )

    @property
    def data(self):
        if self._data is None:
            self.pre_allocate()
        return self._data

    def read(self, n=10240):
        if (timeit.default_timer() - self.start) <= self.timeout and not self._shutdown_event.is_set():
            chunk = self.data.read(n)
            self.total.append(len(chunk))
            return chunk
        raise SpeedtestUploadTimeout()

    def __len__(self):
        return self.length


class HTTPUploader(threading.Thread):
    """Thread that uploads data for the speed test."""

    def __init__(self, i, request, start, size, timeout, opener=None, shutdown_event=None):
        super().__init__()
        self.request = request
        self.request.data.start = self.starttime = start
        self.size = size
        self.result = 0
        self.timeout = timeout
        self.i = i
        self._opener = opener.open if opener else urlopen
        self._shutdown_event = shutdown_event or FakeShutdownEvent()

    def run(self):
        try:
            if ((timeit.default_timer() - self.starttime) <= self.timeout and
                    not self._shutdown_event.is_set()):
                # Some older servers might expect direct read
                with self._opener(self.request) as f:
                    f.read(11)
                self.result = sum(self.request.data.total)
            else:
                self.result = 0
        except (IOError, SpeedtestUploadTimeout):
            self.result = sum(self.request.data.total)
        except HTTP_ERRORS:
            self.result = 0


class SpeedtestResults:
    """
    Holds the results of a Speedtest:
    - Download speed
    - Upload speed
    - Ping
    - Server data
    - Client data
    """

    def __init__(self, download=0, upload=0, ping=0, server=None, client=None,
                 opener=None, secure=False):
        self.download = download
        self.upload = upload
        self.ping = ping
        self.server = server or {}
        self.client = client or {}
        self._share = None
        self.timestamp = f"{datetime.datetime.now().isoformat()}Z"
        self.bytes_received = 0
        self.bytes_sent = 0
        self._opener = opener or build_opener()
        self._secure = secure

    def __repr__(self):
        return repr(self.dict())

    def dict(self):
        """Return a dict representation of the results."""
        return {
            "download": self.download,
            "upload": self.upload,
            "ping": self.ping,
            "server": self.server,
            "timestamp": self.timestamp,
            "bytes_sent": self.bytes_sent,
            "bytes_received": self.bytes_received,
            "share": self._share,
            "client": self.client,
        }

    @staticmethod
    def csv_header(delimiter=","):
        """Return CSV header row."""
        row = [
            "Server ID", "Sponsor", "Server Name", "Timestamp", "Distance",
            "Ping", "Download", "Upload", "Share", "IP Address"
        ]
        out = StringIO()
        writer = csv.writer(out, delimiter=delimiter, lineterminator="")
        writer.writerow(row)
        return out.getvalue()

    def csv(self, delimiter=","):
        """Return data as a CSV row."""
        data = self.dict()
        out = StringIO()
        writer = csv.writer(out, delimiter=delimiter, lineterminator="")
        row = [
            data["server"].get("id", ""),
            data["server"].get("sponsor", ""),
            data["server"].get("name", ""),
            data["timestamp"],
            data["server"].get("d", ""),
            data["ping"],
            data["download"],
            data["upload"],
            self._share or "",
            self.client.get("ip", "")
        ]
        writer.writerow(row)
        return out.getvalue()

    def json(self, pretty=False):
        """Return data in JSON format."""
        if pretty:
            return json.dumps(self.dict(), indent=4, sort_keys=True)
        return json.dumps(self.dict())

    def share(self):
        """POST results to the speedtest.net API to get a shareable link."""
        if self._share:
            return self._share

        download = int(round(self.download / 1000.0, 0))
        upload = int(round(self.upload / 1000.0, 0))
        ping = int(round(self.ping, 0))

        # Build the payload for speedtest.net
        api_data = [
            f"recommendedserverid={self.server.get('id', 0)}",
            f"ping={ping}",
            "screenresolution=",
            "promo=",
            f"download={download}",
            "screendpi=",
            f"upload={upload}",
            "testmethod=http",
            f"hash={md5(f'{ping}-{upload}-{download}-297aae72'.encode()).hexdigest()}",
            "touchscreen=none",
            "startmode=pingselect",
            "accuracy=1",
            f"bytesreceived={self.bytes_received}",
            f"bytessent={self.bytes_sent}",
            f"serverid={self.server.get('id', 0)}",
        ]

        headers = {"Referer": "http://c.speedtest.net/flash/speedtest.swf"}
        request = build_request(
            "://www.speedtest.net/api/api.php",
            data="&".join(api_data).encode(),
            headers=headers,
            secure=self._secure
        )
        f, e = catch_request(request, opener=self._opener)
        if e:
            raise ShareResultsConnectFailure(e)

        response = f.read().decode()
        code = f.code
        f.close()

        if code != 200:
            raise ShareResultsSubmitFailure(
                "Could not submit results to speedtest.net"
            )

        qsargs = parse_qs(response)
        resultid = qsargs.get("resultid")
        if not resultid or len(resultid) != 1:
            raise ShareResultsSubmitFailure(
                "Could not parse result ID from speedtest.net share response."
            )

        self._share = f"http://www.speedtest.net/result/{resultid[0]}.png"
        return self._share


class Speedtest:
    """Main class that performs a Speedtest against speedtest.net servers."""

    def __init__(self, config=None, source_address=None, timeout=10,
                 secure=False, shutdown_event=None):
        self.config = {}
        self._source_address = source_address
        self._timeout = timeout
        self._opener = build_opener(source_address, timeout)
        self._secure = secure
        self._shutdown_event = shutdown_event or threading.Event()

        self.servers = {}
        self.closest = []
        self._best = {}

        self.get_config()
        if config is not None:
            self.config.update(config)

        self.results = SpeedtestResults(
            client=self.config["client"],
            opener=self._opener,
            secure=secure
        )

    @property
    def best(self):
        """Return the best server (lowest latency)."""
        if not self._best:
            self.get_best_server()
        return self._best

    def get_config(self):
        """Retrieve speedtest.net configuration."""
        headers = {}
        headers["Accept-Encoding"] = "gzip"
        request = build_request("://www.speedtest.net/speedtest-config.php",
                                headers=headers, secure=self._secure)
        uh, e = catch_request(request, opener=self._opener)
        if e:
            raise ConfigRetrievalError(e)

        stream = get_response_stream(uh)
        configxml = b""
        while True:
            chunk = stream.read(1024)
            if not chunk:
                break
            configxml += chunk
        stream.close()
        uh.close()

        if uh.code != 200:
            return None

        printer(f"Config XML:\n{configxml}", debug=True)
        try:
            root = ET.fromstring(configxml)
        except ET.ParseError as ex:
            raise SpeedtestConfigError(
                f"Malformed speedtest.net configuration: {ex}"
            )

        server_config = root.find("server-config").attrib
        download = root.find("download").attrib
        upload = root.find("upload").attrib
        client = root.find("client").attrib

        ignore_servers = [
            int(x) for x in server_config.get("ignoreids", "").split(",")
            if x.strip()
        ]
        ratio = int(upload["ratio"])
        upload_max = int(upload["maxchunkcount"])

        # Some typical sizes
        up_sizes = [32768, 65536, 131072, 262144, 524288, 1048576, 7340032]
        sizes = {
            "upload": up_sizes[ratio - 1:],
            "download": [350, 500, 750, 1000, 1500, 2000, 2500, 3000, 3500, 4000],
        }

        size_count = len(sizes["upload"])
        upload_count = math.ceil(upload_max / size_count)

        counts = {
            "upload": int(upload_count),
            "download": int(download["threadsperurl"]),
        }

        threads = {
            "upload": int(upload["threads"]),
            "download": int(server_config["threadcount"]) * 2,
        }

        length = {
            "upload": int(upload["testlength"]),
            "download": int(download["testlength"]),
        }

        self.config.update({
            "client": client,
            "ignore_servers": ignore_servers,
            "sizes": sizes,
            "counts": counts,
            "threads": threads,
            "length": length,
            "upload_max": upload_count * size_count,
        })

        try:
            self.lat_lon = (float(client["lat"]), float(client["lon"]))
        except ValueError:
            raise SpeedtestConfigError(
                f"Unknown location: lat={client.get('lat')} lon={client.get('lon')}"
            )

        printer(f"Config:\n{self.config}", debug=True)
        return self.config

    def get_servers(self, servers=None, exclude=None):
        """Retrieve the list of Speedtest.net servers, optionally filtered."""
        if servers is None:
            servers = []
        if exclude is None:
            exclude = []

        self.servers.clear()

        # Convert server IDs to int
        for lst in (servers, exclude):
            for i, s in enumerate(lst):
                try:
                    lst[i] = int(s)
                except ValueError:
                    raise InvalidServerIDType(
                        f"{s} is an invalid server type, must be int"
                    )

        urls = [
                "://www.speedtest.net/speedtest-servers-static.php",
            "http://c.speedtest.net/speedtest-servers-static.php",
            "://www.speedtest.net/speedtest-servers.php",
            "http://c.speedtest.net/speedtest-servers.php",
        ]

        headers = {"Accept-Encoding": "gzip"}
        errors = []

        for url in urls:
            try:
                request = build_request(
                    f"{url}?threads={self.config['threads']['download']}",
                    headers=headers,
                    secure=self._secure
                )
                uh, e = catch_request(request, opener=self._opener)
                if e:
                    errors.append(str(e))
                    raise ServersRetrievalError()

                stream = get_response_stream(uh)
                serversxml = b""
                while True:
                    chunk = stream.read(1024)
                    if not chunk:
                        break
                    serversxml += chunk
                stream.close()
                uh.close()

                if uh.code != 200:
                    raise ServersRetrievalError()

                printer(f"Servers XML:\n{serversxml}", debug=True)
                try:
                    root = ET.fromstring(serversxml)
                except ET.ParseError as ex:
                    raise SpeedtestServersError(
                        f"Malformed speedtest.net server list: {ex}"
                    )

                for server in root.iter("server"):
                    attrib = server.attrib
                    sid = int(attrib.get("id", 0))
                    if servers and sid not in servers:
                        continue
                    if sid in self.config["ignore_servers"] or sid in exclude:
                        continue
                    try:
                        d = distance(self.lat_lon, (float(attrib["lat"]), float(attrib["lon"])))
                    except Exception:
                        continue
                    attrib["d"] = d
                    self.servers.setdefault(d, []).append(attrib)

                break
            except ServersRetrievalError:
                continue

        if (servers or exclude) and not self.servers:
            raise NoMatchedServers()

        return self.servers

    def set_mini_server(self, server):
        """
        Use a Speedtest Mini server instead of the main speedtest.net list.
        """
        urlparts = urlparse(server)
        path_dir, ext = os.path.splitext(urlparts.path)
        if ext:
            url_base = os.path.dirname(server)
        else:
            url_base = server.rstrip("/")

        # Check connectivity
        request = build_request(url_base)
        uh, e = catch_request(request, opener=self._opener)
        if e:
            raise SpeedtestMiniConnectFailure(f"Failed to connect to {server}")
        text = uh.read().decode()
        uh.close()

        # Attempt to figure out the upload extension
        extension = re.findall(r'upload_?[Ee]xtension:\s*"([^"]+)"', text)
        if not extension:
            for x in ['php', 'asp', 'aspx', 'jsp']:
                try:
                    f = self._opener.open(f"{url_base}/speedtest/upload.{x}")
                except Exception:
                    pass
                else:
                    data = f.read().strip().decode()
                    f.close()
                    if f.code == 200 and len(data.splitlines()) == 1 and re.match(r"size=\d+", data):
                        extension = [x]
                        break

        if not extension:
            raise InvalidSpeedtestMiniServer(
                f"Invalid Speedtest Mini Server: {server}"
            )

        self.servers = [{
            "sponsor": "Speedtest Mini",
            "name": urlparts.netloc,
            "d": 0,
            "url": f"{url_base}/speedtest/upload.{extension[0]}",
            "latency": 0,
            "id": 0
        }]

        return self.servers

    def get_closest_servers(self, limit=5):
        """Return up to `limit` servers that are closest geographically."""
        if not self.servers:
            self.get_servers()

        self.closest.clear()
        for d in sorted(self.servers):
            for s in self.servers[d]:
                self.closest.append(s)
                if len(self.closest) == limit:
                    break
            else:
                continue
            break

        printer(f"Closest Servers:\n{self.closest}", debug=True)
        return self.closest

    def get_best_server(self, servers=None):
        """
        Perform a quick "ping" (HTTP HEAD or small GET) to find the
        server with the lowest latency.
        """
        if not servers:
            if not self.closest:
                servers = self.get_closest_servers()
            else:
                servers = self.closest

        user_agent = build_user_agent()
        results = {}

        for server in servers:
            cum = []
            url_base = os.path.dirname(server["url"])
            stamp = int(timeit.time.time() * 1000)
            latency_url = f"{url_base}/latency.txt?x={stamp}"
            for i in range(3):
                this_url = f"{latency_url}.{i}"
                printer(f"GET {this_url}", debug=True)
                urlparts = urlparse(this_url)

                try:
                    if urlparts.scheme == "https":
                        conn = SpeedtestHTTPSConnection(urlparts.netloc, source_address=(
                        self._source_address, 0) if self._source_address else None)
                    else:
                        conn = SpeedtestHTTPConnection(urlparts.netloc, source_address=(
                        self._source_address, 0) if self._source_address else None)
                    conn.timeout = 10

                    path = urlparts.path
                    if urlparts.query:
                        path = f"{urlparts.path}?{urlparts.query}"

                    start = timeit.default_timer()
                    conn.request("GET", path, headers={"User-Agent": user_agent})
                    r = conn.getresponse()
                    total = timeit.default_timer() - start
                    data = r.read(9)
                    if r.status == 200 and data == b"test=test":
                        cum.append(total)
                    else:
                        cum.append(3600)
                    conn.close()
                except HTTP_ERRORS as exc:
                    printer(f"ERROR: {exc}", debug=True)
                    cum.append(3600)

            avg = round((sum(cum) / 6) * 1000.0, 3)
            results[avg] = server

        try:
            fastest = sorted(results.keys())[0]
        except IndexError:
            raise SpeedtestBestServerFailure("Unable to connect to servers to test latency.")

        best = results[fastest]
        best["latency"] = fastest
        self.results.ping = fastest
        self.results.server = best
        self._best.update(best)

        printer(f"Best Server:\n{best}", debug=True)
        return best

    def download(self, callback=do_nothing, threads=None):
        """
        Test download speed against the chosen server.
        A threads value of None uses the config default.
        """
        urls = []
        for size in self.config["sizes"]["download"]:
            for _ in range(self.config["counts"]["download"]):
                urls.append(f"{os.path.dirname(self.best['url'])}/random{size}x{size}.jpg")

        request_count = len(urls)
        requests = [
            build_request(url, bump=i, secure=self._secure)
            for i, url in enumerate(urls)
        ]

        max_threads = threads or self.config["threads"]["download"]
        in_flight = {"threads": 0}
        q = Queue(max_threads)

        finished = []

        def producer(q_, reqs, total_reqs):
            for idx, req in enumerate(reqs):
                thread = HTTPDownloader(
                    idx,
                    req,
                    start_time,
                    self.config["length"]["download"],
                    opener=self._opener,
                    shutdown_event=self._shutdown_event
                )
                while in_flight["threads"] >= max_threads:
                    timeit.time.sleep(0.001)
                thread.start()
                q_.put(thread, True)
                in_flight["threads"] += 1
                callback(idx, total_reqs, start=True)

        def consumer(q_, total_reqs):
            while len(finished) < total_reqs:
                t = q_.get(True)
                while t.is_alive():
                    t.join(timeout=0.001)
                in_flight["threads"] -= 1
                finished.append(sum(t.result))
                callback(t.i, total_reqs, end=True)

        start_time = timeit.default_timer()
        prod_thread = threading.Thread(target=producer, args=(q, requests, request_count))
        cons_thread = threading.Thread(target=consumer, args=(q, request_count))

        prod_thread.start()
        cons_thread.start()

        while prod_thread.is_alive():
            prod_thread.join(timeout=0.001)
        while cons_thread.is_alive():
            cons_thread.join(timeout=0.001)

        stop_time = timeit.default_timer()
        self.results.bytes_received = sum(finished)
        self.results.download = (self.results.bytes_received / (stop_time - start_time)) * 8.0

        # If download is quite high, increase upload thread count
        if self.results.download > 100000:
            self.config["threads"]["upload"] = 8
        return self.results.download

    def upload(self, callback=do_nothing, pre_allocate=True, threads=None):
        """
        Test upload speed against the chosen server.
        A threads value of None uses the config default.
        """
        sizes = []
        for size in self.config["sizes"]["upload"]:
            for _ in range(self.config["counts"]["upload"]):
                sizes.append(size)

        request_count = self.config["upload_max"]
        requests = []
        for i, size in enumerate(sizes):
            data = HTTPUploaderData(
                size,
                0,
                self.config["length"]["upload"],
                shutdown_event=self._shutdown_event
            )
            if pre_allocate:
                data.pre_allocate()
            headers = {"Content-length": str(size)}
            req = build_request(self.best["url"], data, secure=self._secure, headers=headers)
            requests.append((req, size))

        max_threads = threads or self.config["threads"]["upload"]
        in_flight = {"threads": 0}
        q = Queue(max_threads)
        finished = []

        def producer(q_, reqs, total_reqs):
            for idx, (req, sz) in enumerate(reqs[:total_reqs]):
                thread = HTTPUploader(
                    idx,
                    req,
                    start_time,
                    sz,
                    self.config["length"]["upload"],
                    opener=self._opener,
                    shutdown_event=self._shutdown_event
                )
                while in_flight["threads"] >= max_threads:
                    timeit.time.sleep(0.001)
                thread.start()
                q_.put(thread, True)
                in_flight["threads"] += 1
                callback(idx, total_reqs, start=True)

        def consumer(q_, total_reqs):
            while len(finished) < total_reqs:
                t = q_.get(True)
                while t.is_alive():
                    t.join(timeout=0.001)
                in_flight["threads"] -= 1
                finished.append(t.result)
                callback(t.i, total_reqs, end=True)

        start_time = timeit.default_timer()
        prod_thread = threading.Thread(target=producer, args=(q, requests, request_count))
        cons_thread = threading.Thread(target=consumer, args=(q, request_count))

        prod_thread.start()
        cons_thread.start()

        while prod_thread.is_alive():
            prod_thread.join(timeout=0.1)
        while cons_thread.is_alive():
            cons_thread.join(timeout=0.1)

        stop_time = timeit.default_timer()
        self.results.bytes_sent = sum(finished)
        self.results.upload = (self.results.bytes_sent / (stop_time - start_time)) * 8.0
        return self.results.upload


def ctrl_c(shutdown_event):
    """Helper to catch Ctrl-C and set a shutdown event."""

    def inner(signum, frame):
        shutdown_event.set()
        printer("\nCancelling...", error=True)
        sys.exit(0)

    return inner


def version():
    """Print version info and exit."""
    printer(f"speedtest-cli {__version__}")
    printer(f"Python {sys.version.replace(os.linesep, '')}")
    sys.exit(0)


def csv_header(delimiter=","):
    """Print CSV header row and exit."""
    printer(SpeedtestResults.csv_header(delimiter=delimiter))
    sys.exit(0)


def parse_args():
    """Parse command-line arguments."""
    description = (
        "Command line interface for testing internet bandwidth using "
        "speedtest.net.\n"
        "https://github.com/sivel/speedtest-cli"
    )
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("--no-download", dest="download", action="store_false",
                        default=True,
                        help="Do not perform download test")
    parser.add_argument("--no-upload", dest="upload", action="store_false",
                        default=True,
                        help="Do not perform upload test")
    parser.add_argument("--single", action="store_true", default=False,
                        help="Use a single connection instead of multiple")
    parser.add_argument("--bytes", dest="units", action="store_const",
                        const=("byte", 8), default=("bit", 1),
                        help="Display values in bytes instead of bits")
    parser.add_argument("--share", action="store_true",
                        help="Generate and provide a URL to the share results image")
    parser.add_argument("--simple", action="store_true", default=False,
                        help="Suppress verbose output, only show basic info")
    parser.add_argument("--csv", action="store_true", default=False,
                        help="Output in CSV format (bit/s), overrides verbose")
    parser.add_argument("--csv-delimiter", default=",",
                        help="Single character delimiter to use in CSV output")
    parser.add_argument("--csv-header", action="store_true", default=False,
                        help="Print CSV headers")
    parser.add_argument("--json", action="store_true", default=False,
                        help="Output in JSON format (bit/s), overrides verbose")
    parser.add_argument("--list", action="store_true",
                        help="Display a list of speedtest.net servers, sorted by distance")
    parser.add_argument("--server", type=int, action="append",
                        help="Specify a server ID to test against (repeatable)")
    parser.add_argument("--exclude", type=int, action="append",
                        help="Exclude a server from selection (repeatable)")
    parser.add_argument("--mini", help="URL of the Speedtest Mini server")
    parser.add_argument("--source", help="Source IP address to bind to")
    parser.add_argument("--timeout", default=10, type=float,
                        help="HTTP timeout in seconds. Default 10")
    parser.add_argument("--secure", action="store_true",
                        help="Use HTTPS for speedtest.net (if possible)")
    parser.add_argument("--no-pre-allocate", dest="pre_allocate",
                        action="store_false", default=True,
                        help="Do not pre-allocate upload data")
    parser.add_argument("--version", action="store_true",
                        help="Show the version number and exit")
    parser.add_argument("--debug", action="store_true", default=False,
                        help=argparse.SUPPRESS)

    return parser.parse_args()


def shell():
    """Entry point that runs the command-line interface."""
    global DEBUG
    shutdown_event = threading.Event()
    signal.signal(signal.SIGINT, ctrl_c(shutdown_event))

    args = parse_args()

    if args.version:
        version()

    if not args.download and not args.upload:
        raise SpeedtestCLIError("Cannot supply both --no-download and --no-upload")

    if len(args.csv_delimiter) != 1:
        raise SpeedtestCLIError("--csv-delimiter must be a single character")

    if args.csv_header:
        csv_header(args.csv_delimiter)

    # Check if modules are available (ssl, etc.) – typically these are in stdlib
    if args.secure and HTTPSConnection is None:
        raise SystemExit("SSL support is not installed, --secure is unavailable.")

    if args.debug:
        DEBUG = True

    quiet = bool(args.simple or args.csv or args.json)
    machine_format = bool(args.csv or args.json)

    callback = do_nothing if (quiet or args.debug) else print_dots(shutdown_event)

    printer("Retrieving speedtest.net configuration...", quiet)
    try:
        speedtest = Speedtest(
            source_address=args.source,
            timeout=args.timeout,
            secure=args.secure,
            shutdown_event=shutdown_event
        )
    except (ConfigRetrievalError, *HTTP_ERRORS) as exc:
        printer("Cannot retrieve speedtest configuration", error=True)
        raise SpeedtestCLIError(exc) from exc

    if args.list:
        try:
            speedtest.get_servers()
        except (ServersRetrievalError, *HTTP_ERRORS) as exc:
            printer("Cannot retrieve speedtest server list", error=True)
            raise SpeedtestCLIError(exc) from exc

        sorted_servers = sorted(speedtest.servers.items(), key=lambda x: x[0])
        for distance_km, servers_list in sorted_servers:
            for srv in servers_list:
                line = (
                    f"{srv['id']:>5}) {srv['sponsor']} ({srv['name']}, {srv.get('country', '')}) "
                    f"[{srv['d']:.2f} km]"
                )
                try:
                    printer(line)
                except IOError as e:
                    if e.errno != errno.EPIPE:
                        raise
        sys.exit(0)

    printer(f"Testing from {speedtest.config['client']['isp']} ({speedtest.config['client']['ip']})...", quiet)

    if not args.mini:
        printer("Retrieving speedtest.net server list...", quiet)
        try:
            speedtest.get_servers(servers=args.server, exclude=args.exclude)
        except NoMatchedServers:
            raise SpeedtestCLIError(
                "No matched servers: " + ", ".join(str(s) for s in args.server or [])
            )
        except (ServersRetrievalError, *HTTP_ERRORS) as exc:
            printer("Cannot retrieve speedtest server list", error=True)
            raise SpeedtestCLIError(exc) from exc
        except InvalidServerIDType as exc:
            raise SpeedtestCLIError(str(exc)) from exc

        if args.server and len(args.server) == 1:
            printer("Retrieving information for the selected server...", quiet)
        else:
            printer("Selecting best server based on ping...", quiet)
        speedtest.get_best_server()
    else:
        speedtest.get_best_server(speedtest.set_mini_server(args.mini))

    results = speedtest.results
    printer(
        f"Hosted by {results.server['sponsor']} ({results.server['name']}) "
        f"[{results.server['d']:.2f} km]: {results.server['latency']} ms", quiet
    )

    if args.download:
        printer("Testing download speed", quiet, end=("\n" if DEBUG else ""))
        speedtest.download(callback=callback, threads=(1 if args.single else None))
        printer(
            f"Download: {(results.download / 1_000_000) / args.units[1]:0.2f} M{args.units[0]}/s",
            quiet
        )
    else:
        printer("Skipping download test", quiet)

    if args.upload:
        printer("Testing upload speed", quiet, end=("\n" if DEBUG else ""))
        speedtest.upload(
            callback=callback,
            pre_allocate=args.pre_allocate,
            threads=(1 if args.single else None)
        )
        printer(
            f"Upload: {(results.upload / 1_000_000) / args.units[1]:0.2f} M{args.units[0]}/s",
            quiet
        )
    else:
        printer("Skipping upload test", quiet)

    printer(f"Results:\n{results.dict()}", debug=True)

    # --share if not quiet-machine format
    if not args.simple and args.share:
        results.share()

    if args.simple:
        printer(
            f"Ping: {results.ping} ms\n"
            f"Download: {(results.download / 1_000_000) / args.units[1]:0.2f} M{args.units[0]}/s\n"
            f"Upload: {(results.upload / 1_000_000) / args.units[1]:0.2f} M{args.units[0]}/s"
        )
    elif args.csv:
        printer(results.csv(delimiter=args.csv_delimiter))
    elif args.json:
        printer(results.json())
    if args.share and not machine_format:
        printer(f"Share results: {results.share()}")


def main():
    """Main entry point."""
    try:
        shell()
    except KeyboardInterrupt:
        printer("\nCancelling...", error=True)
    except (SpeedtestException, SystemExit) as exc:
        if getattr(exc, "code", 1) not in (0, 2):
            msg = str(exc) if str(exc) else repr(exc)
            raise SystemExit(f"ERROR: {msg}") from exc


if __name__ == "__main__":
    main()
