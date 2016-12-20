import socket
import threading
import uuid
import hashlib
import httpserver
import merkletree
# -*- coding: utf-8 -*-
from tutorial import Calculator
from tutorial.ttypes import *
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol


#threading.Thread(target = self.discovery).start()
#heartbeat = threading.enumerate()
#heartbeat = heartbeat[1]
#threading.Thread(target = self.threadcontroller).start()
#print '\n' + str(threading.enumerate())

#Testar se o nodo achando esta certo
#Inserir no arquivo certo, tentar achar o nodo em que o arquivo se encontra
#Quando inserir um filho:
# Procurar aonde esta o pai
#Inserir no pai
#No delete tambem deletar no pai e passar os filhos para elements



def teste(porta):
    """Metodo de testes para conectar um nodo a outro."""
    transport = TSocket.TSocket('localhost', porta)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = Calculator.Client(protocol)
    transport.open()
    client.ping()
    found = client.return_key_index("teste")
    print found
    transport.close()

def getnodes(myport, otanto):
    """Retorna um dicionario com os nos vivos e seus keyindex."""
    print "tentando getnodes"
    #print "Digi
    #te o tanto ai fdp"
    #otanto = input()
    myport = int(myport)
    print type(myport)
    print myport
    found = {}
    for i in xrange(5555, 5555+otanto, 1):
        print type(i)
        if i != myport:
            try:
                print i
                transport = TSocket.TSocket('localhost', i)
                transport = TTransport.TBufferedTransport(transport)
                protocol = TBinaryProtocol.TBinaryProtocol(transport)
                client = Calculator.Client(protocol)
                transport.open()
                foundkeyindex = client.return_key_index("foo")
                found[i] = foundkeyindex
                client.ping()
                transport.close()
                print i
            except Thrift.TException, tx:
                pass

    print "passou getnodes"
    return found


def findnodetable(dirkey, tableindex):
    """Retorna o rightnode se tiver com o hash dentro."""
    for port, arqlist in tableindex.iteritems():
        for arq in arqlist:
            if dirkey == arq:
                return port
    return 0

def distribute_arq(arqdir, tableindex):
    """Procura o nodo certo para armazenar este arquivo e devolve sua porta."""
    nodenr = 0
    rightnode = 0
    root = httpserver.Parsing(arqdir)
    #Pegando o primeiro caminho para achar sua chave
    root = root[0]
    #Definindo o hash sendo o primeiro diretorio para colocar os filhos no msm no
    roothash = hash(root)
    #hash do caminho inteiro (hash do arquivo especifico)
    arqkey = hash(arqdir)
    portlist = []
    portcounter = 0
    for port, keylist in tableindex.iteritems():
        nodenr = nodenr + 1
        portlist.append(port)
        portcounter = portcounter + 1
    mod = arqkey % nodenr
    rightnodeport = portlist[mod]
    return rightnodeport


#fazer a distribuicao de arquivos direito
#fazer os testes corretos para os servidores em nodos diferentes

    pass




def updateindex(arqindex):
    """Retorna um dicionario com os arquivos de cada no."""
    pass

def findarq2(key):
    """Define em qual nodo um arquivo esta, e devolve o cliente da conexao."""
    pass

def findkey(arq):
    """Acha a chave de um arquivo pelo seu nome."""
    arqkey = hash(arq)
    print arqkey
    print "AQUI"
    return arqkey

def findarq(myport, targetarq, tableindex):
    """Checa todas as portas em que servidores podem estar vivo, cliente."""
    #definindo o range de portas a serem checadas e os ips
    for port, keylist in tableindex.iteritems():
        if port is not myport:
            for i in range(0, len(keylist), 1):
                if keylist[i] == targetarq:
                    try:
                        transport = TSocket.TSocket('localhost', port)
                        transport = TTransport.TBufferedTransport(transport)
                        protocol = TBinaryProtocol.TBinaryProtocol(transport)
                        client = Calculator.Client(protocol)
                        transport.open()
                        client.ping()
                        return client, transport
                    except Thrift.TException, tx:
                        pass
    return 1, 0
