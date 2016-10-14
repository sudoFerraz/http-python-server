import socket
import threading
import httpserver
import sys
import fileserver

mutex = threading.Lock()

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
            threading.Thread(target = self.Conexao, args = (client,\
                address)).start()
            print '\n' + str(threading.enumerate())

    def Conexao(self, cliente, address):
        threadmerkle = fileserver.root.merkle_hash()
        print "Conectado com o cliente %s" % str(address)
        metodo, caminhoSplitado, corpo, tamanho = httpserver.recebe_handler\
            (cliente)
        mutex.acquire()
        print str(fileserver.root.hash)
        print str(fileserver.root.merkle_hash())
        while True:
            if threadmerkle == fileserver.root.merkle_hash():
                resultado = httpserver.metodo_handler(metodo, caminhoSplitado,\
                    corpo)
                break
            else:
                threadmerkle = fileserver.root.merkle_hash()
        # try:
            # resultado = httpserver.metodo_handler(metodo, caminhoSplitado,\
                # corpo)
        # finally:
            # mutex.release()
        cliente.send(resultado)
        print resultado
        cliente.close()
        return False


if __name__ == "__main__":
    port_num = int(sys.argv[1])
    ThreadedServer('', port_num).listen()
