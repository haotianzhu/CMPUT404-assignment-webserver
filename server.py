#  coding: utf-8 
import socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketser    ver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


def get_request_info(data_string):
    # return method address
    return data_string.split()[0:2]


def location_controller(location, method):
    import os
    if method != 'GET':
        respone_dict['HTTP/1.1'] = '405 Method Not Allowed'
        return '''
<html>
<head>
<title>405 Method Not Allowed</title>
</head>
<body>
<h1>Method Not Allowed</h1>
<p>Method Not Allowed</p>
</body>
</html>'''       

    current_location = os.path.dirname(os.path.abspath(__file__))+'/www'

    abs_location = current_location + location

    if os.path.isdir(abs_location):

        if abs_location[-1] == '/':
            abs_location += 'index.html'
        else:
            abs_location = location + '/'

            head = 'HTTP/1.1: 301 Moved Permanently\r\nContent-Type: text/css\r\nConnection: Closed\r\n'
            return head +'Location: '+str(abs_location)+'\r\n\n'


    if os.path.isfile(abs_location):
        if '.css' in abs_location:
            # update css
            head = 'HTTP/1.1: 200 OK\r\nContent-Type: text/css\r\nConnection: Closed\r\n\n'
            with open(abs_location,'r', encoding="utf8") as f:
                return head + f.read()
        elif '.html' in abs_location:
            head = 'HTTP/1.1: 200 OK\r\nContent-Type: text/html\r\nConnection: Closed\r\n\n'
            with open(abs_location,'r', encoding="utf8") as f:
                return  head + f.read()
        
    # 404
    return '''HTTP/1.1: 404 Not FOUND\r
Content-Type: text/html\r
Connection: Closed\r\n

<html>
<head>
<title>404 Not Found</title>
</head>
<body>
<h1>Not Found</h1>
<p>The requested URL was not found on this server.</p>
</body>
</html>'''

class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):

        self.data = self.request.recv(1024).strip()
        data_string = self.data.decode('utf-8')
    
        method, location = get_request_info(data_string)

        send_data = location_controller(location, method)

        self.request.sendall(bytearray(send_data,'utf-8'))




if __name__ == "__main__":

    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
