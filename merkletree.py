""" Implementacao de uma merkle tree para utilizacao no servidor\
    http distribuido"""


import hashlib

class merkle(object):
    """Achar o hash de todos os arquivos e a raiz."""
    def __init__(self):
        pass

    def findkey(self, arqname):
        hasher = hashlib.sha256()
        hasher.update(arqname)
        key = hasher.hexdigest()
        return key


    def acha_root(self, file_hashes):
        """Separa os hashes em 2 grupos, e concatena os grupos."""
        blocks = []

        try:
            if file_hashes:
                print "[+]"
        except ValueError:
            print "\nArquivo de hashes nao presente."

        # embaralha hashes
        for m in sorted(file_hashes):
            blocks.append(m)

        list_len = len(blocks)

        # ajusta o nmr de hashes em cada bloco para par
        while list_len % 2 != 0:
            blocks.extend(blocks[-1:])
            list_len = len(blocks)


        secondary = []
        for k in [blocks[x:x+2] for x in xrange(0, len(blocks), 2)]:
            hasher = hashlib.sha256()
            hasher.update(k[0]+k[1])
            secondary.append(hasher.hexdigest())

        if len(secondary) == 1:
            # Devolvendo apenas os primeiros 64 caracteres do hash
            return secondary[0][0:64]
        else:
            #Se o numero de itens na lista > 1 recursa
            return self.acha_root(secondary)

    def merkle_handler(self, file_hashes, hash):
        """Apagar um hash da lista."""
        hash_len = len(file_hashes)

        for k in xrange(0, hash_len):
            if file_hashes[k] == hash:
                del file_hashes[k]

        return file_hashes
