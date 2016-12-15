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

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

class Menu(object):
    def __init__(self):
        pass


    def user_menu(self, client):
        print "[+] Escolha uma opcao [+]"
        print "[1]GET - Retorna dados e metadados do arquivo"
        print "[2]Lista - Retorna lista de filhos do arquivo"
        print "[3]Add - Adiciona arquivo"
        print "[4]Update - Atualiza arquivos"
        print "[5]Delete - Apaga arquivo"
        print "[6]Updatex - Atualiza arquivo se versao for a mesma"
        print "[7]Deletex - Apaga arquivo se versao for a mesma "
        selected = input()

        if selected == 0:
            exit()
        if selected == 1:
            print "Digite o caminho do arquivo"
            arq = raw_input()
            #print arq
            answer = client.get(arq)
            print answer
        if selected == 2:
            print "Digite o caminho do arquivo"
            arq = raw_input()
            answer = client.list(arq)
            print answer
        if selected == 3:
            print "Digite o nome do novo arquivo"
            arq = raw_input()
            print "Digite os dados do arquivo"
            data = raw_input()
            print "Digite o diretorio do arquivo"
            directory = raw_input()
            request = arq + data + directory
            answer = client.add(arq, directory, data)
            print answer
        if selected == 4:
            print "Digite o caminho do arquivo que deseja atualizar"
            arq = raw_input()
            print "Digite os dados novos do arquivo"
            data = raw_input()
            answer = client.update(arq, data)
            print answer
        if selected == 5:
            print "Digite o caminho do arquivo que deseja deletar"
            arq = raw_input()
            answer = client.delete1(arq)
            print answer
        if selected == 6:
            print "Digite o nome do arquivo que deseja atualizar"
            arq = raw_input()
            print "Digite a versao de target"
            version = raw_input()
            print "Digite os dados que deseja atualizar"
            data = raw_input()
            answer = client.updatex(arq, version, data)
            print answer
        if selected == 7:
            print "Digite o nome do arquivo que deseja deletar"
            arq = raw_input()
            print "Digite a versao de target"
            version = raw_input()
            answer = client.deletex(arq, version)
            print answer

global portr
portr = sys.argv[1]
try:

  # Make socket
  transport = TSocket.TSocket('localhost', portr)

  # Buffering is critical. Raw sockets are very slow
  transport = TTransport.TBufferedTransport(transport)

  # Wrap in a protocol
  protocol = TBinaryProtocol.TBinaryProtocol(transport)

  # Create a client to use the protocol encoder
  client = Calculator.Client(protocol)

  # Connect!
  transport.open()

  #client.ping()
  print 'ping()'
  # Close!

except Thrift.TException, tx:
  print '%s' % (tx.message)



#requisicao = client.request("doido")
#print requisicao
menu = Menu()
menu.user_menu(client)
transport.close()
