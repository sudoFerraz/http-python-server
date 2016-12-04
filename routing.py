import socket
import threading
import uuid
import hashlib
import httpserver
# -*- coding: utf-8 -*-

#threading.Thread(target = self.discovery).start()
#heartbeat = threading.enumerate()
#heartbeat = heartbeat[1]
#threading.Thread(target = self.threadcontroller).start()
#print '\n' + str(threading.enumerate())


def getnodes(aliveport):
    """Retorna uma lista com todos os nos vivos."""
    pass

def updateindex(arqindex):
    """Retorna um dicionario com os arquivos de cada no."""
    pass

def routarq(key):
    """Define em qual nodo um arquivo esta, e devolve o cliente da conexao."""
    pass

def findkey(arq):
    """Acha a chave de um arquivo pelo seu caminho."""
    pass
