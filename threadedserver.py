import socket
import threading
import httpserver
import sys

class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(30)
            threading.Thread(target = httpserver.Conexao, args = (client,\
                address)).start()
            print '\n' + str(threading.enumerate())

""" def listenToClient(self, client, address):
        size = 1024
        while True:
            try:
                data = client.recv(size)
                if data:
                    # set the response to echo back
                    response = data
                    print ("Enviando resposta")
                    client.send(response)
                else:
                    raise error('Client Disconnected')
            except:
                client.close()
                return False
"""


if __name__ == "__main__":
    port_num = int(sys.argv[1])
    ThreadedServer('', port_num).listen()
