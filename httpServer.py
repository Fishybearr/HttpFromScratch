import socket

host = '127.0.0.1'
port = 8888

isListening = True

def handle_request(data):
    response_line = b"HTTP/1.1 200 OK\r\n"

    headers = b"".join([
        b"Server: RAD Server\r\n",
        b"Content-Type: text/html\r\n"
        ])

    blank_line = b"\r\n"

    response_body = b"""<html> 
    <body>
    <h1>Request Reciveed</h1>
    </body>
    </html>
    """
    return b"".join([response_line,headers,blank_line,response_body])

#Create a socket
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.bind((host,port))

s.listen(5)

print(f"Listening at {s.getsockname()}")

while isListening:
    conn,addr = s.accept()

    print("Connected by",addr)
    
    data = conn.recv(1024)

    response = handle_request(data)

    conn.sendall(response)

    conn.close()



