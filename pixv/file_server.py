
from http.server import BaseHTTPRequestHandler, HTTPServer
import os

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

class FileServer(BaseHTTPRequestHandler):
    def _set_headers(self, status_code=200, content_type='text/plain'):
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        filename = self.headers['File-Name']
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        with open(file_path, 'wb') as f:
            f.write(self.rfile.read(content_length))
        self._set_headers(status_code=201)
        self.wfile.write(b'File uploaded successfully')

    def do_GET(self):
        filename = self.path[1:]
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(file_path):
            self._set_headers(content_type='application/octet-stream')
            with open(file_path, 'rb') as f:
                self.wfile.write(f.read())
        else:
            self._set_headers(status_code=404)
            self.wfile.write(b'File not found')

def run(server_class=HTTPServer, handler_class=FileServer, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting file server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()