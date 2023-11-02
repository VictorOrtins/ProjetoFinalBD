class Cliente:
    def __init__(self, id, cpf, primeiroNome, ultimoNome, cidade, login, senha, isFlamengo, assisteOnePiece):
        self.id = id
        self.primeiroNome = primeiroNome
        self.ultimoNome = ultimoNome
        self.cpf = cpf
        self.cidade = cidade
        self.login = login
        self.senha = senha
        self.isFlamengo = isFlamengo
        self.assisteOnePiece = assisteOnePiece

    def stringCliente(self):
        return "{\n" + f"Nome: {self.nome}\n\tCPF: {self.cpf}\n\tCidade: {self.cidade}\n\tTorce pro Flamengo: {self.isFlamengo}\n\tAssiste One Piece: {self.assisteOnePiece}\n" + "}"

