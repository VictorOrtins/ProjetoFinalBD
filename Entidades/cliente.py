class Cliente:
    def __init__(self, id, cpf, primeiroNome, ultimoNome, cidade, isFlamengo, assisteOnePiece):
        self.id = id
        self.primeiroNome = primeiroNome
        self.ultimoNome = ultimoNome
        self.cpf = cpf
        self.cidade = cidade
        self.isFlamengo = isFlamengo
        self.assisteOnePiece = assisteOnePiece

    def stringCliente(self):
        return "{\n" + f"Nome: {self.nome}\n\tCPF: {self.cpf}\n\tCidade: {self.cidade}\n\tTorce pro Flamengo: {self.isFlamengo}\n\tAssiste One Piece: {self.assisteOnePiece}\n" + "}"
    
    def stringInformacoes(self):
        string = "{\n" + f"\tNome Completo: {self.primeiroNome} {self.ultimoNome}\n\tCPF: {self.cpf}\n\tCidade Natal: {self.cidade}\n"
        if self.isFlamengo:
            string += "\tTorcedor do Flamengo\n"
        if self.assisteOnePiece:
            string += "\tAssiste One Piece\n"
        string += "}"

        return string

