#!/usr/bin/env python

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

from shared.ttypes import SharedStruct

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
import socket
import threading
import sys

class CalculatorHandler:
  def __init__(self):
    self.log = {}
    self.nodes = []
    self.host = 'localhost'
    self.port = 5555
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.sock.bind((self.host, self.port))
    threading.Thread(target = self.discovery).start()
    heartbeat = threading.enumerate()
    heartbeat = heartbeat[1]
    threading.Thread(target = self.threadcontroller).start()
    print '\n' + str(threading.enumerate())

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

  def get(self, requested):
      print "teste2"
      return requested

  def list(self, requested):
      pass

  def update(self, requested):
      pass

  def delete(self, requested):
      pass

  def updatex(self, requested):
      pass

  def deletex(self, requested):
      pass

  def add(self, n1, n2):
    print 'add(%d,%d)' % (n1, n2)
    return n1+n2

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
