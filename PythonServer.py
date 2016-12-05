#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership. The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.
#

import sys, glob
sys.path.append('gen-py')
#sys.path.insert(0, glob.glob('../../lib/py/build/lib.*')[0])

from tutorial import Calculator
from tutorial.ttypes import *
import routing
import httpserver
import fileserver

from shared.ttypes import SharedStruct

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
import socket
import threading
import sys
import merkletree


class CalculatorHandler:
  def __init__(self):
    self.log = {}
    self.nodes = {}
    self.tableindex = {}
    self.arqindex = []
    self.keyindex = []
    self.host = 'localhost'
    self.port = 0
    self.tableindex = routing.getnodes(9090)

  def check_arq_present(self, arqkey):
      """Checa se um arquivo esta presente neste nodo."""
      for i in range(0, len(self.keyindex), 1):
          key = self.keyindex[i]
          if arqkey == key:
              return True
      return False

  def addhandler(self, parsedmessage):
      """Cria os diretorios parents do arquivo."""
      pass



  def addarq(self, name):
      newarq = fileserver.arquivo(name)
      self.arqindex.append(newarq)
      print self.arqindex[0].hash
      arqkey = newarq.hash
      self.keyindex.append(arqkey)
      self.tableindex[9090] = self.keyindex
      return "doido"

  def heartbeat(self, host, port):
      #testar as outras portas para ver a que nao esta sendo usada
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      self.sock.bind((self.host, self.port))
      # retornar uma lista com todos os nos vivos
      #self.nodes = routing.getnodes(self.port)
      # pegar uma tabela com os respectivos arquivos de cada nó
      #self.tableindex = routing.updateindex(self.arqindex)
      pass

  def threadcontroller(self):
      main = threading.enumerate()
      heartbeat = main[1]
      main = main[0]
      while main.isAlive():
          self.nodediscovery()
          pass


  def stop(self):
      exit()

  def nodediscovery(self):
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.settimeout(2)
      for i in xrange(1, 5556, 5560):
          port = i
          try:
              s.connect((self.host, port))
              s.sendall("sup")
              self.nodes.append(port)
              s.close()
          except socket.timeout, e:
              for portx in xrange(1, 0, len(self.nodes)):
                  if self.nodes[portx] == port:
                      del self.nodes[portx]
          except socket.gaierror, e:
              pass


  def return_key_index(self):
      return self.keyindex


  def discovery(self):
      while True:
          self.sock.listen(10)
          client, address = self.sock.accept()
          client.send("wazzup")
          client.close()


  def request(self, requested):
      print "funcionando"
      doido = requested
      return doido

  def ping(self):
      print 'ping()'

  def getr(self, arqkey):
      for pos in self.arqindex:
          if pos.hash == arqkey:
              answer = "\nNome:" + str(pos.nome) + "\nCreated:" + \
              str(pos.created) + "\nModified:" + str(pos.modified) + "\nVersion:"\
              + str(pos.version) + "\nHash:" + str(pos.hash)
              return answer
      return "deu ruim"
#Nao esquecer de declarar as funcoes no tutorial.thrift

  def checkparent(self, directory):
      """Verifica até qual nível de raiz está presente e retorna um indice."""
      dirlist = httpserver.Parsing(directory)
      level = 0
      parentkey = "/" + routing.findkey(dirlist[0])
      for i in range(0, len(dirlist), 1):
          if not level < i:
              parentkey = parentkey + "/" + routing.findkey(dirlist[i])
          if self.check_arq_present(parentkey):
              level = level + 1
      return level

  def get(self, requested):
      print "teste2"
      arqkey = routing.findkey(requested)
      if self.check_arq_present(arqkey):
          answer = self.getr(arqkey)
          return answer
      else:
          cliente, transporte = routing.findarq(9090, arqkey, self.tableindex)
          if cliente == 1:
              return 'Arquivo nao esta presente no servidor'
          else:
              answer = cliente.getr(arqkey)
              transporte.close()
              return answer

  def listr(self, arqkey):
      pass

  def list(self, requested):
      print "teste3"
      arqkey = routing.findkey(requested)
      cliente, transporte = routing.findarq(9090, arqkey)
      answer = cliente.listr(arqkey)
      transporte.close()
      return answer

  def updater(self, arqkey):
      pass

  def update(self, requested):
      arqkey = routing.findkey(requested)
      cliente, transporte = routing.findarq(arqkey)
      answer = cliente.updater(arqkey)
      transporte.close()
      return answer

  def delete(self, requested):
      arqkey = routing.findkey(requested)
      cliente, transporte = routing.findarq(arqkey)
      answer = cliente.deleter(arqkey)
      transporte.close()
      return answer

  def updatexr(self, arqkey):
      pass

  def updatex(self, requested):
      arqkey = routing.findkey(requested)
      cliente, transporte = routing.findarq(arqkey)
      answer = cliente.updatexr(arqkey)
      transporte.close()
      return answer

  def deletexr(self, arqkey):
      pass

  def deletex(self, requested):
      arqkey = routing.findkey(requested)
      cliente, transporte = routing.findarq(arqkey)
      answer = cliente.deletexr(arqkey)
      transporte.close()
      return answer

# FAZER O ADD DIREITO.

  def add(self, requested):
      arqkey = routing.findkey(requested)
      answer = cliente.addr(arqkey)
      return True

  def calculate(self, logid, work):
    print 'calculate(%d, %r)' % (logid, work)

    if work.op == Operation.ADD:
      val = work.num1 + work.num2
    elif work.op == Operation.SUBTRACT:
      val = work.num1 - work.num2
    elif work.op == Operation.MULTIPLY:
      val = work.num1 * work.num2
    elif work.op == Operation.DIVIDE:
      if work.num2 == 0:
        x = InvalidOperation()
        x.whatOp = work.op
        x.why = 'Cannot divide by 0'
        raise x
      val = work.num1 / work.num2
    else:
      x = InvalidOperation()
      x.whatOp = work.op
      x.why = 'Invalid operation'
      raise x

    log = SharedStruct()
    log.key = logid
    log.value = '%d' % (val)
    self.log[logid] = log

    return val

  def getStruct(self, key):
    print 'getStruct(%d)' % (key)
    return self.log[key]

  def zip(self):
    print 'zip()'

handler = CalculatorHandler()
processor = Calculator.Processor(handler)
transport = TSocket.TServerSocket(port=9090)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

# You could do one of these for a multithreaded server
#server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)
#server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)

print 'Starting the server...'
server.serve()
print 'done.'
