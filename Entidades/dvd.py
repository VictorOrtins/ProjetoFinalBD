class DVD:
    def __init__(self, idFilme, quantidade, nomeFilme):
        self.idFilme = idFilme
        self.quantidade = quantidade
        self.nomeFilme = nomeFilme

    def stringDVD(self):
        return "{" + f"\n\tNome do Filme: {self.nomeFilme}\n\tQuantidade: {self.quantidade}\n" + "}"