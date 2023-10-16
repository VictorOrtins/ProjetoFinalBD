class Cliente:
    def __init__(self, id, nome, cpf, endereco, senha, isFlamengo, assisteOnePiece):
        self.id = id
        self.nome = nome
        self.cpf = cpf
        self.endereco = endereco
        self.senha = senha
        self.isFlamengo = isFlamengo
        self.assisteOnePiece = assisteOnePiece

    def stringCliente(self):
        return "{\n" + f"\tID: {self.id}\n\tNome: {self.nome}\n\tCPF: {self.cpf}\n\tEndereço: {self.endereco}\n\tTorce pro Flamengo: {self.isFlamengo}\n\tAssiste One Piece: {self.assisteOnePiece}\n" + "}"

