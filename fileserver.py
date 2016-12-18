import time
import uuid
import merkletree
import httpserver

__metaclass__ = type

merkle = merkletree.merkle()
global file_hashes
file_hashes = []

class arquivo():
    """Estrutura dos arquivos do servidor."""

    def __init__(self,nome):
        global file_hashes
        #self.nome = httpserver.Parsing(nome)
        #self.nome = self.nome[-1]
        #self.nome = str(self.nome)
        self.nome = nome
        self.filhos = []
        self.data = None
        self.created = int(time.time())
        self.modified = int(time.time())
        self.version = 0
        self.hash = hash(nome)
        self.pai = None
        file_hashes.append(self.hash)

    def insere(self, filho):
        """Insere na lista de arquivos subjacentes."""
        self.filhos.append(filho)
        filho.pai = self

    def insere_dados(self,data):
        """Insere dados dentro de um arquivo."""
        global file_hashes
        self.data = data
        self.modified = int(time.time())
        self.version = self.version + 1
        #file_hashes = merkle.merkle_handler(file_hashes, self.hash)
        #self.hash = str(uuid.uuid4().hex)
        #file_hashes.append(self.hash)

    def remove_arq(self):
        """Removendo um arquivo e realocando seus filhos."""
        global file_hashes
        if self.pai != None:
            self.pai.filhos.extend(self.filhos)
            self.pai.filhos.remove(self)
            self.pai.modified = int(time.time())
        #file_hashes = merkle.merkle_handler(file_hashes, self.hash)
        del self

    def merkle_hash(self):
        global file_hashes
        roothash = merkle.acha_root(file_hashes)

        return roothash

#root = arquivo("/")
