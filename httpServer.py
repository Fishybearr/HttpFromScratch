import socket

host = '127.0.0.1'
port = '8888'

isListening = True

#Create a socket
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.bind((host,port))

s.listen(5)

print(f"Listening at {s.getsockname()}")

while isListening:
    conn,addr = s.accept()