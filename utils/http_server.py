#!/usr/bin/env python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

try:
    from urllib.parse import urlparse, parse_qs
except ImportError:
    from urlparse import urlparse, parse_qs


class JKHttpHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

    def do_GET(self):
        o = urlparse(self.path)
        print(parse_qs(o.query))

        self._set_headers()
        self.wfile.write("Ok")

    def do_HEAD(self):
        self._set_headers()


def parse_query_params(handler):
    o = urlparse(handler.path)
    return parse_qs(o.query)


def run_http_server(server_class=HTTPServer, handler_class=JKHttpHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print ('Starting httpd on %s...' % port)
    httpd.serve_forever()


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run_http_server(port=int(argv[1]))
    else:
        run_http_server()
