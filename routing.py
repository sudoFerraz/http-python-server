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


def getnodes(myport):
    """Retorna um dicionario com os nos vivos e seus keyindex."""
    print "Digite o range de portas que voce gostaria de checar:"
    port_range = input()
    found = {}
    for i in range(5050, 5050+port_range, 1):
        if i is not myport:
            try:
                transport = TSocket.TSocket('localhost, i')
                transport = TTransport.TBufferedTransport(transport)
                protocol = TBinaryProtocol.TBinaryProtocol(transport)
                client = Calculator.Client(protocol)
                transport.open()
                foundkeyindex = client.return_key_index()
                found[i] = foundkeyindex
                transport.close()
            except Thrift.TException, tx:
                pass
    return found


def updateindex(arqindex):
    """Retorna um dicionario com os arquivos de cada no."""
    pass

def findarq2(key):
    """Define em qual nodo um arquivo esta, e devolve o cliente da conexao."""
    pass

def findkey(arq):
    """Acha a chave de um arquivo pelo seu nome."""
    hasher = merkletree.merkle()
    arqkey = hasher.findkey(arq)
    return arqkey

def findarq(myport, targetarq, tableindex):
    """Checa todas as portas em que servidores podem estar vivo, devolve porta."""
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
                        return client, transport
                    except Thrift.TException, tx:
                        pass
    return 'Arquivo nao esta presente no servidor'

    for i in range(0, len(tableindex), 1):
        if i is not myport:
            try:
                transport = TSocket.TSocket('localhost', i)
                transport = TTransport.TBufferedTransport(transport)
                protocol = TBinaryProtocol.TBinaryProtocol(transport)
                client = Calculator.Client(protocol)
                transport.open()
                if client.check_arq_present(targetarq):
                    return client, transport
                if not client.check_arq_present(targetarq):
                    transport.close()
            except Thrift.TException, tx:
                pass
    return 'Arquivo nao esta presente no servidor'
