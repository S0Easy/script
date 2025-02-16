import socket


def handleRequest(client):
    buf = client.recv(2048)
    print(buf)
    #msg = "HTTP/1.1 200 OK\r\n\r\n"
    msg1 = "Hello, World!"
    #client.send(('%s' % msg).encode())
    client.send(('%s' % msg1).encode())

if __name__ == '__main__':
    ip_port = ('0.0.0.0', 8081)
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.bind(ip_port)
    socket.listen(5)
    
    while True:
        client, addr = socket.accept()
        print('Connected by', addr)
        handleRequest(client)
        client.close()