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
from thrift import Thrift


from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
import socket
import threading
import sys
import merkletree
import threading
mutex = threading.Lock()


class CalculatorHandler:
  def __init__(self):
    self.log = {}
    self.nodes = {}
    self.tableindex = {}
    self.arqindex = []
    self.keyindex = []
    self.host = 'localhost'
    self.port = portr
    self.tableindex = {}
    self.tableindex[self.port] = self.arqindex
    #routing.teste(5556)
    self.tableindex.update(routing.getnodes(self.port, 5))

  def update_table(self):
      print "atualizando a tabela"
      self.tableindex.update(routing.getnodes(self.port, 5))
      self.tableindex[self.port] = self.keyindex

  def check_arq_present(self, arqkey):
      """Checa se um arquivo esta presente."""
      print "CHECKARQPRESENT"
      for i in range(0, len(self.keyindex), 1):
          key = self.keyindex[i]
          if arqkey == key:
              print "teste"
              return 1
      return 0

  def addhandler(self, parentslist, level, arqdir):
      """Cria os diretorios parents do arquivo."""
      for i in range(level+1, len(parentslist), 1):
          print "printando no addhandler"
          self.addson(parentslist[i], routing.findkey(parentslist[i-1]), arqdir, level, i)



  def addson(self, name, parentkey, arqdir, level, i):
      mutex.acquire()
      nivel = level + i
      arqdir = arqdir.split("/")
      arqdir = arqdir[0:nivel]
      arqdir = ''.join(arqdir)

      #Cria o novo arquivo
      newarq = fileserver.arquivo(name)
      #Faz o hash do nome de cada arquivo e compara com o hash do nome do pai
      for arq in self.arqindex:
          print "Printando no addson"
          print routing.findkey(arq.nome)
          print parentkey
          if routing.findkey(arq.nome) == parentkey:
              print "Inserindo como filho"
              arq.insere(newarq)
      self.arqindex.append(newarq)
      self.keyindex.append(newarq.hash)
      self.tableindex[portr] = self.keyindex
      mutex.release()


  def addarq(self, path):
      mutex.acquire()
      newarq = fileserver.arquivo(path)
      self.arqindex.append(newarq)
      #pegando o hash do caminho inteiro
      arqkey = newarq.hash
      self.keyindex.append(arqkey)
      self.tableindex[portr] = self.keyindex
      print "Printando no add arq, lista de chaves:"
      print self.keyindex
      mutex.release()

  def heartbeat(self, host, port):
      #testar as outras portas para ver a que nao esta sendo usada
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      self.sock.bind((self.host, self.port))
      host = ''
      self.sock.listen(host)
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


  def heartbeat(self):
      """Deifinir o heartbeat de cada no comunicando."""

      pass

  def stop(self):
      exit(1)

  def nodediscovery(self):
      self.update_table()
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


  def return_key_index(self, foo):
      doido = foo
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

  def update_table(self):
      self.tableindex = routing.getnodes(portr, 5)
      self.tableindex[self.port] = self.keyindex

  def ping(self):
      print 'ping()'


#Nao esquecer de declarar as funcoes no tutorial.thrift

  def checkparent(self, directory):
      """Verifica até qual nível de raiz está presente e retorna um indice."""
      dirlist = httpserver.Parsing(directory)
      level = 0
      parentname = "/" + dirlist[0]
      parentkey = routing.findkey(parentname)
      print "checkparent"
      for i in range(0, len(dirlist), 1):
          if not level < i:
              parentname = parentname + "/" + dirlist[i]
              parentkey = routing.findkey(parentname)
          if self.check_arq_present(parentkey):
              level = level + 1
      print "printando level"
      print level
      return level

  def get(self, requested):
      print "teste2"
      self.update_table()
      print self.tableindex
      arqkey = routing.findkey(requested)
      if self.check_arq_present(arqkey):
          answer = self.getr(arqkey)
          return answer
      else:
          rightnode = routing.findnodetable(arqkey, self.tableindex)
          rightnode = int(rightnode)
          #rightnode = routing.distribute_arq(requested, self.tableindex)
          print "Achando nodo certo:"
          print rightnode
          cliente, transporte = self.novaconexao(rightnode)
          if transporte == 1:
              return "Arquivo nao esta presente no servidor"
          print "Printando as tabelas:"
          print self.tableindex
          cliente.ping()
          resp = cliente.check_arq_present(arqkey)
          if resp == 1:
              answer = cliente.getr(arqkey)
              transporte.close()
              return answer
          else:
              transporte.close()
              return 'Arquivo nao esta presente no servidor'

  def getr(self, arqkey):
      for pos in self.arqindex:
          if pos.hash == arqkey:
              nomecerto = httpserver.Parsing(pos.nome)
              nomecerto = nomecerto[-1]
              answer = "\nNome:" + str(nomecerto) + "\nCreated:" + \
              str(pos.created) + "\nModified:" + str(pos.modified) + "\nVersion:"\
              + str(pos.version) + "\nHash:" + str(pos.hash)
              return answer
      return "deu ruim"

  def listr(self, arqkey):
      nomesfilhos = []
      for pos in self.arqindex:
          if pos.hash == arqkey:
              filhos = pos.filhos
              print "Dentro do laco do listr"
              print pos.hash
              print arqkey
              print filhos

              for filho in filhos:
                  nomesfilhos = nomesfilhos.append(filho.nome)
              answer = ''.join(nomesfilhos)
      print "Printando answer no listr"
      print answer
      return answer

  def list1(self, requested):
      print "teste3"
      self.update_table()
      arqkey = routing.findkey(requested)
      if self.check_arq_present(arqkey):
          answer = self.listr(arqkey)
          return answer
      else:
          rightnode = routing.distribute_arq(requested, self.tableindex)
          print "Achando nodo certo:"
          print rightnode
          cliente, transporte = self.novaconexao(rightnode)
          answer = cliente.listr(arqkey)
          transporte.close()
          return answer

  def updater(self, arqkey, arqdata):
      for pos in self.arqindex:
          if pos.hash == arqkey:
              pos.insere_dados(arqdata)
              answer = 'Atualizado com sucesso'
      return answer

  def update(self, requested, arqdata):
      self.update_table()
      arqkey = routing.findkey(requested)
      if self.check_arq_present(arqkey):
          answer = self.updater(arqkey, arqdata)
          return answer
      else:
          rightnode = routing.distribute_arq(requested, self.tableindex)
          print "Achando nodo certo:"
          print rightnode
          cliente, transporte = self.novaconexao(rightnode)
          if transporte == 1:
              print "entrou"
              return "Arquivo nao esta presente no servidor"
          answer = cliente.updater(arqkey, arqdata)
          transporte.close()
          return answer

  def checkglobalparents(self, directory, tableindex):
      """Verifica se existem pais em outros nodos"""
      dirlist = httpserver.Parsing(directory)
      level = 0
      #parentnodelist = []
      parentname = "/" + dirlist[0]
      parentkey = routing.findkey(parentname)
      for i in range(0, len(dirlist), 1):
          if not level < i:
              parentname = parentname + "/" + dirlist[i]
              parentkey = routing.findkey(parentname)
              for port, keylist in tableindex.iteritems():
                  for key in keylist:
                      if parentkey == key:
                          level = level + 1
      return level


  def deleter(self, arqkey, requested):
      level = self.checkglobalparents(requested, self.tableindex)
      if level != 0:
          mutex.acquire()
          print "Operacao modificara outros arquivos [commit/abort]"
          doido = raw_input()
          if doido == "commit":
              for pos in self.arqindex:
                  if pos.hash == arqkey:
                      print "Hash do arquivo"
                      print pos.hash
                      pos.remove_arq()
                      self.arqindex.remove(pos)
                      answer = 'Apagado com sucesso'
                  for pos in self.keyindex:
                      if pos == arqkey:
                      self.keyindex.remove(pos)
          mutex.release()
          if doido == "abort":
              mutex.release()
              answer = "Nao apagado"
      elif level == 0:
          for pos in self.arqindex:
              if pos.hash == arqkey:
                  print "Hash do arquivo"
                  print pos.hash
                  pos.remove_arq()
                  self.arqindex.remove(pos)
                  answer = 'Apagado com sucesso'
              for pos in self.keyindex:
                  if pos == arqkey:
                  self.keyindex.remove(pos)
      return answer

  def delete1(self, requested):
      self.update_table()
      arqkey = routing.findkey(requested)
      if self.check_arq_present(arqkey):
          answer = self.deleter(arqkey, requested)
          return answer
      else:
          rightnode = routing.findnodetable(arqkey, self.tableindex)
          rightnode = int(rightnode)
          #rightnode = routing.distribute_arq(requested, self.tableindex)
          print "Achando nodo certo:"
          print rightnode
          cliente, transporte = self.novaconexao(rightnode)
          answer = cliente.deleter(arqkey)
          transporte.close()
          return answer

  def updatexr(self, arqkey, arqdata, arqversion):
      for pos in self.arqindex:
          if pos.hash == arqkey:
              if pos.version == arqversion:
                  pos.insere_dados(arqdata)
                  answer = 'Atualizado com sucesso'
              else:
                  answer = 'Nao Atualizado'
      return answer

  def updatex(self, requested, arqkeyversion , arqdata):
      self.update_table()
      arqkey = routing.findkey(requested)
      if self.check_arq_present(arqkey):
          answer = self.updatexr(arqkey, arqdata, arqkeyversion)
          return answer
      else:
          rightnode = routing.distribute_arq(requested, self.tableindex)
          print "Achando nodo certo:"
          print rightnode
          cliente, transporte = self.novaconexao(rightnode)
          answer = cliente.updatexr(arqkey, arqdata, arqkeyversion)
          transporte.close()
          return answer

  def deletexr(self, arqkey, arqversion):
      level = self.checkglobalparents(requested, self.tableindex)
      if level != 0:
          mutex.acquire()
          print "Operacao modificara outros arquivos [commit/abort]"
          doido = raw_input()
          if doido == "commit":
              for pos in self.arqindex:
                  if pos.hash == arqkey:
                      if pos.version == arqversion:
                          print "Hash do arquivo"
                          print pos.hash
                          pos.remove_arq()
                          self.arqindex.remove(pos)
                          answer = 'Apagado com sucesso'
                          for pos in self.keyindex:
                              if pos == arqkey:
                                  self.keyindex.remove(pos)
          mutex.release()
          if doido == "abort":
              mutex.release()
              answer = "Nao apagado"
      elif level == 0:
          for pos in self.arqindex:
              if pos.hash == arqkey:
                  print "Hash do arquivo"
                  print pos.hash
                  pos.remove_arq()
                  self.arqindex.remove(pos)
                  answer = 'Apagado com sucesso'
              for pos in self.keyindex:
                  if pos == arqkey:
                  self.keyindex.remove(pos)
      return answer



  def deletex(self, requested, arqversion):
      self.update_table()
      arqkey = routing.findkey(requested)
      if self.check_arq_present(arqkey):
          answer = self.deletexr(arqkey, arqversion)
          return answer
      else:
          rightnode = routing.distribute_arq(requested, self.tableindex)
          print "Achando nodo certo:"
          print rightnode
          cliente, transporte = self.novaconexao(rightnode)
          answer = cliente.deletexr(arqkey, arqversion)
          transporte.close()
          return answer

  def novaconexao(self, port):
      """Cria uma nova conexao e devolve um cliente e um transporte."""
      try:
          transport = TSocket.TSocket('localhost', port)
          transport = TTransport.TBufferedTransport(transport)
          protocol = TBinaryProtocol.TBinaryProtocol(transport)
          client = Calculator.Client(protocol)
          transport.open()
      except Thrift.TException, tx:
          print '%s' % (tx.message)
          message = "Arquivo nao esta presente"
          check = 1
          return message, check
      return client, transport

# FAZER O ADD DIREITO.


  def announcement(self):
      """Anuncia que houve uma alteração e necessita uma att."""
      pass

  def add(self, arqname, arqdir, arqdata):
      self.update_table()
      rightnode = routing.distribute_arq(arqdir, self.tableindex)
      print self.tableindex
      print rightnode
      print "PRINTANDO NODO CERTO"
      print rightnode
      if rightnode == portr:
          level = self.checkparent(arqdir)
          #Se nao tiver nenhum pai já adiciona pelo metodo
          if level == 0:
              check = self.addarq(arqdir)
              if check == True:
                  self.announcement()
                  print self.keyindex
                  #self.update_table()
                  return 'Adicionado com sucesso'
          dirlist = httpserver.Parsing(arqdir)
          check = self.addhandler(dirlist, level, arqdir)
          if check == True:
              self.announcement()
              print self.keyindex
              #self.update_table()
              return 'Adicionado com sucesso'

      else:
          cliente, transporte = self.novaconexao(rightnode)
          cliente.ping()
          print "pingo"
          level = cliente.checkparent(arqdir)
          print "recebeu"
          print level
          if level == 0:
              print "addarq"
              cliente.addarq(arqdir)
              #self.tableindex.update(routing.getnodes(portr))
              transporte.close()
              print self.keyindex
              #self.update_table()
              return 'Adicionado com sucesso'
          print "level > 0"
          dirlist = httpserver.Parsing(arqdir)
          print "addhandler"
          cliente.addhandler(dirlist, level)
          transporte.close()
          self.tableindex.update(routing.getnodes(portr, 5))
          self.tableindex[self.port] = self.keyindex
          print self.keyindex
          #self.update_table()
          return 'Adicionado com sucesso'

      return 'Arquivo adicionado com sucesso'

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
global portr
portr = sys.argv[1]
handler = CalculatorHandler()
processor = Calculator.Processor(handler)
transport = TSocket.TServerSocket(port=portr)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

# You could do one of these for a multithreaded server
#server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)
#server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)

print 'Starting the server on port ' + portr + " ..."
server.serve()
print 'done.'
