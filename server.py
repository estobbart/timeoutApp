import time
import BaseHTTPServer
from threading import Thread
import time
import socket

HOST = "127.0.0.1"
PORT = 9000

ONCE = False
KILL = False

def non_accepting_socket_server():
    global ONCE
    if ONCE:
        return
    ONCE = True
    serversocket = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((HOST, 9001))
    serversocket.listen(1)
    print "launched non_accepting_socket_server"
    while True and not KILL:
        time.sleep(1)

class TimeoutHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            thread = Thread(target = non_accepting_socket_server)
            thread.start()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(open("index.html", "r").read())
        else:
            self.send_response(404)
            # while True:
            #    pass

if __name__ == '__main__':
    #global KILL
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST, PORT), TimeoutHandler)
    print "listening %s:%s" % (HOST, PORT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        KILL = True
        pass
    httpd.server_close()
