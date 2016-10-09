"""HTTP server with file tree Sistemas Distribuidos 2016-2 UFU.
a
 ____   ____  _________________  _________________      _____
|    | |    |/                 \/                 \ ___|\    \
|    | |    |\______     ______/\______     ______/|    |\    \
|    |_|    |   \( /    /  )/      \( /    /  )/   |    | |    |
|    .-.    |    ' |   |   '        ' |   |   '    |    |/____/|
|    | |    |      |   |              |   |        |    ||    ||
|    | |    |     /   //             /   //        |    ||____|/
|____| |____|    /___//             /___//         |____|
|    | |    |   |`   |             |`   |          |    |
|____| |____|   |____|             |____|          |____|
  \(     )/       \(                 \(              \(
   '     '         '                  '               '
"""

import socket
import sys
import time
import string
import re

# Definindo var. globais
get = "GET"
put = "PUT"
post = "POST"
delete = "DELETE"
header = "HEAD"
__metaclass__ = type


def main():
    """Funcao principal para conexao."""
    # Define o host que pode ser qualquer um, estamos servindo...
    host = ''
    # Porta e passada pelo argumento da funcao
    port = int(sys.argv[1])
    # Define familha de enderecos IPV4, e que estamos usando streaming()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Faz o bind do socket para pode escutar
    s.bind((host, port))
    print "Servidor rodando na porta %d" % port
    print "Aguardando conexao"
    s.listen(10)
    while 1:
        Conexao(s)


def Conexao(Socketcliente):
    """Abrindo conexao com cliente quando conectado."""
    sockcliente, addrcliente = Socketcliente.accept()
    print "Conectado com o cliente %s" % str(addrcliente)
    c = "\r\n\r\n"
    message = ''
    while 1:
        message += sockcliente.recv(1024)
        print message
        if c in message:
            break
        # check = sockcliente.recv(1024)
        # if not check:
        #    break
    metodo, caminhoSplitado, corpo = Parsing(message)
    print metodo
    print caminhoSplitado
    print corpo
    resultado = metodo_handler(metodo, caminhoSplitado, corpo)
    sockcliente.send(resultado)
    print resultado
    sockcliente.close()


def metodo_handler(metodo, caminho, corpo):
    """Definindo qual metodo e qual handler usar, retorna mensagem."""
    if metodo == get:
        objeto = acha_objeto(caminho)
        resposta = Get_Handler(objeto)
        # fazer a mensagem correta com o codigo e os dados
        return resposta
    elif metodo == post:
        resposta = Post_Handler(caminho, corpo)
        return resposta
    elif metodo == put:
        objeto = acha_objeto(caminho)
        resposta = Put_Handler(objeto, corpo)
        return resposta
    elif metodo == delete:
        objeto = acha_objeto(caminho)
        resposta = Delete_Handler(objeto)
        return resposta
    elif metodo == header:
        objeto = acha_objeto(caminho)
        resposta = Header_Handler(objeto)
        return resposta


def acha_objeto(caminho):
    """Procura o objeto no qual o caminho termina."""
    nodo = root
    if len(caminho) == 1 and caminho[0] == '':
        return root
    elif caminho[0] != '':
        for i in range(0, len(root.filhos), 1):
            if caminho[0] == root.filhos[i].nome:
                nodo = root.filhos[i]
        for i in range(1, len(caminho), 1):
            for j in range(0, len(nodo.filhos), 1):
                if caminho[i] == nodo.filhos[j].nome:
                    nodo = nodo.filhos[j]
    if caminho[len(caminho)-1] != nodo.nome:
        nodo = None
        return None
    elif caminho[len(caminho)-1] == nodo.nome:
        return nodo


def Parsing(message):
    """Faz parsing e separa uma lista para o metodo e caminhos splitados."""
    linhas = message.split("\n")
    data = message.split("\r\n\r\n")
    data = data[1]
    linhas2 = linhas[0].split(" HTTP")
    linhas3 = linhas2[0].split(" /")
    caminho = linhas3[1].split("/")
    metodo = linhas3[0]
    return metodo, caminho, data


def traduz(mensagem):
    """Coloca mensagem em plaintext."""
    mensagem = mensagem.replace("\n", " ")
    return mensagem


def msg200_OK(metodo, objeto):
    """Definindo a mensagem 200 OK."""
    msg = ('HTTP/1.1 ' + str(metodo) + ' 200 OK\n')
    msg2 = ('Version: ' + str(objeto.version) + '\n'
            + 'Creation: ' + str(objeto.created) + '\n'
            + 'Modification: ' + str(objeto.modified) + '\n')
    if metodo != delete:
        msg += msg2
    if objeto.data is None:
        objeto.data = "None"
    corpo = ('Content_Length: ' + str(len(objeto.data)))
    dados = ('\n\n' + str(objeto.data))
    if metodo == header:
        msg += corpo
    if metodo == get:
        msg += corpo
        msg += dados
    return msg


def msg403_Forbidden(metodo, objeto):
    """Definindo mensagem de acesso nao autorizado."""
    msg = "HTTP/1.1 403 Forbidden"
    if metodo == post:
        msg += ('\nVersion: ' + str(objeto.version) + '\n'
                + 'Creation: ' + str(objeto.created) + '\n'
                + 'Modification: ' + str(objeto.modified) + '\n')
    return msg


def msg201_Created():
    """Definindo mensagem 201, Created."""
    msg = """HTTP/1.1 201 Created\nContent-Type: text/html\nConnection: Closed\r\n\r\n
        <!DOCTYPE HTML PUBLIC>
        <html><head>
        <title>201 Created</title>
        </head><body>
        </body></html>"""
    return msg


def msg_204NoContent():
    """Definindo mensagem 204."""
    msg = """HTTP/1.1 204 No content\nContent-Type: text/html\nConnection: Closed\r\n\r\n
        <!DOCTYPE HTML PUBLIC>
        <html><head>
        <title>204 No content</title>
        </head><body>
        </body></html>"""
    return msg


def msg_400BadRequest():
    """Definindo mensagem 400."""
    msg = "HTTP/1.1 400 Bad request"
    return msg


def msg_404NotFound():
    """Definindo mensagem."""
    msg = "HTTP/1.1 404 Not Found"
    return msg


def Get_Handler(objeto):
    """Manejamento do GET."""
    if objeto is None:
        mensagem = msg_404NotFound()
    else:
        mensagem = msg200_OK(get, objeto)
    # Fazer a mensagem correta junto com a msg
    return mensagem


def Post_Handler(caminho, dados):
    """Manejamento do POST(cria)."""
    nodo = root
    # checa se o caminho 'e a propria raiz
    if len(caminho) == 1 and caminho[0] == '':
        message = msg_400BadRequest()
        return message
    # acha ate o ultimo nodo que existe no caminho e devolve ele em nodo
    elif caminho[0] != '':
        for i in range(0, len(caminho), 1):
            for j in range(0, len(nodo.filhos), 1):
                if caminho[i] == nodo.filhos[j].nome:
                    nodo = nodo.filhos[j]
                    break
            # devolve a posicao do caminho que ele difere de um existente
            pos = i
            if caminho[i] != nodo.nome:
                pos = i
                break
    if caminho[pos] == nodo.nome:
        msg = msg403_Forbidden(post, nodo)
        return msg
    novonodo = Fileserver(caminho[pos])
    nodo.insere(novonodo)
    ptnodo = novonodo
    # aloca os novos nodos dependendo de quantos vierem no request
    for k in range(pos+1, len(caminho), 1):
        novonodo = Fileserver(caminho[k])
        # achar um meio de renomear os novos nodos para insercao
        ptnodo.insere(novonodo)
        ptnodo = novonodo
    ptnodo.data = dados
    message = msg200_OK(post, novonodo)
    return message


def Delete_Handler(objeto):
    """Manejamento do DELETE."""
    if objeto is None:
        mensagem = msg403_Forbidden(delete, objeto)
    else:
        objeto.remove_arq()
        mensagem = msg200_OK(delete, objeto)
    return mensagem


def Put_Handler(objeto, dados):
    """Manejamento do PUT(modifica dados)."""
    if objeto is None:
        mensagem = msg403_Forbidden(put, objeto)
    else:
        objeto.data = dados
        objeto.version += 1
        mensagem = msg200_OK(put, objeto)
    return mensagem


def Header_Handler(objeto):
    """Manejamento do Header."""
    if objeto is None:
        mensagem = msg_404NotFound()
    else:
        mensagem = msg200_OK(header, objeto)
    return mensagem


class controle_global():
    """Lista com todos os arquivos ja criados."""

    def __init__(self, nome):
        """Inicializa a lista global."""
        self.criados = []


class Fileserver():
    """Definindo estrutura do servidor de arquivos."""

    def __init__(self, nome):
        """Inicializando um arquivo na arvore(diretorio tambem)."""
        self.nome = nome
        self.filhos = []
        self.nomefilhos = []
        self.data = None
        self.pai = None
        self.nomepai = ''
        self.created = int(time.time())
        self.modified = int(time.time())
        self.version = 0

    def insere(self, filho):
        """Inserir na lista de arquivos subjacentes."""
        self.filhos.append(filho)
        self.nomefilhos.append(filho.nome)
        filho.pai = self

    def insere_dentro(self, pai):
        """Insere arquivo dentro de um pai."""
        pai.filhos.append(self)
        pai.nomefilhos.append(self.nome)

    def insere_dados(self, data):
        """Insere dados dentro de um arquivo."""
        self.data = data
        self.modified = int(time.time())

    def remove_filho(self, filho):
        """Remove um arquivo do diretorio."""
        self.filhos.extend(filho.filhos)
        self.filhos.remove(filho)
        self.nomefilhos.remove(filho.nome)
        self.modified = int(time.time())
        del filho

    def remove_arq(self):
        """Remove o proprio arquivo que chama."""
        self.pai.filhos.extend(self.filhos)
        self.pai.filhos.remove(self)
        self.pai.nomefilhos.remove(self.nome)
        self.pai.modified = int(time.time())
        del self

    def get_dados(self):
        """Devolve os dados guardados no arquivo."""
        return self.data

root = Fileserver("/")
main()
