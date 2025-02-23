import socket
import os
import subprocess


class TCPServer:

    def __init__(self, host='127.0.0.1',port=8888):
        self.host = host
        self.port = port

    def start(self):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

        s.bind((self.host,self.port))

        s.listen(5)

        print(f"Listening at {s.getsockname()}")

        while True:
            conn,addr = s.accept()

            print("Connected by",addr)

            data = conn.recv(1024)

            response = self.handle_request(data)

            conn.sendall(response)

            conn.close()

        
    def handle_request(self, data):
        return data
    

class HTTPServer(TCPServer):

    headers = {
        'Server': 'RADServer',
        'Content-Type': 'text/html',
    }

    status_codes = {
        200: 'OK',
        404: 'Not Found',
        501: 'Not Implemented',
    }

    def handle_request(self, data):

       request = HTTPRequest(data)
       
       try:
        handler = getattr(self,'handle_%s' % request.method)

       except AttributeError:
        handler = self.HTTP_501_handler

       response = handler(request)

       return response
    

   


    def response_line(self,status_code):
        reason = self.status_codes[status_code]
        response_line = "HTTP/1.1 %s %s\r\n" % (status_code,reason)

        return response_line.encode()
    
    def response_headers(self, extra_headers = None):
        headers_copy = self.headers.copy()

        if extra_headers:
            headers_copy.update(extra_headers)
        
        headers = ''

        for h in headers_copy:
            headers += "%s: %s\r\n" % (h,headers_copy[h])

        return headers.encode()
    

    def handle_GET(self,request):
        filename = request.uri.strip('/')

        if os.path.exists(filename):
            response_line = self.response_line(status_code=200)

            response_headers = self.response_headers()

            with open (filename, 'rb') as f:
                response_body = f.read()
        
        else:
            response_line = self.response_line(status_code=404)
            response_headers = self.response_headers()
            response_body = b"<h1>404 Not Found</h1>"

        blank_line = b"\r\n"

        return b"".join([response_line,response_headers,blank_line,response_body])
    
    def handle_POST(self,request):
        
        #print(request.body)

        #command = str(request.body)
        command = str(request.body)

        command = command.replace("+"," ")
        command = command.replace("%2F","/")

        index = command.find("=");
        command = command[index+1:-1]

        print(command)
        rc = ExecuteCode(command)

        #call function here to actually execute the code

        response_line = self.response_line(status_code=501)

        response_headers = self.response_headers()

        blank_line = b'\r\n'

        
        #response_body = "<h1>command output</h1>".join((f"<body>{currentProc}</body>"))

        proc =  str(rc.process)
        proc = proc.replace("\\n","<br>")
        response_body = f"<h1>Command output</h1><p>{proc}</p>"
        
        response_body = response_body.encode()

        return b"".join([response_line,response_headers,blank_line,response_body])

    def HTTP_501_handler(self,request):
       response_line = self.response_line(status_code=501)

       response_headers = self.response_headers()

       blank_line = b'\r\n'

       resonse_body = b"<h1>501 Not Implemented</h1>"

       return b"".join([response_line,response_headers,blank_line,resonse_body])
    
  
    
class HTTPRequest:
    def __init__(self,data):
        self.method = None
        self.uri = None
        self.body = ""
        self.http_version = "1.1"

        self.parse(data)

    def parse(self,data):
        lines = data.split(b"\r\n")

        request_line = lines[0] #body would be lines[1] or something

        words = request_line.split(b" ")

        self.method = words[0].decode()

        if len(words) > 1:
            self.uri = words[1].decode()

        if len(words) > 2:
            self.http_version = words[2]

        if len(lines) > 17:
            self.body = lines[-1] #last line is the body
            #print(body_line)
            #for l in lines:
             #   print("%s\n" % l)

            # here is probably where you would parse the request body


class ExecuteCode:
    process= ""
    def __init__(self,command):
        self.process = subprocess.run(["powershell", "-Command",command], capture_output=True,text=True)
        print(self.process)
        

if __name__ == '__main__':
    server = HTTPServer()
    server.start()

    



