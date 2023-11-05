class Filme:
    def __init__(self, id, nome, dataLancamento, genero, nomeEstudio, nomeDiretor, qtdEstoque, precoAluguel):
        self.id = id
        self.nome = nome
        self.dataLancamento = dataLancamento
        self.genero = genero
        self.nomeEstudio = nomeEstudio
        self.nomeDiretor = nomeDiretor
        self.qtdEstoque = qtdEstoque
        self.precoAluguel = precoAluguel

    def stringFilme(self):
        return "{\n" + f"\tID: {self.id}\n\tNome: {self.nome}\n\tData de Lançamento: {self.dataLancamento}\n\tGênero: {self.genero}\n\tNome do Estúdio: {self.nomeEstudio}\n\tNome do Diretor: {self.nomeDiretor}\n\tQuantidade em Estoque: {self.qtdEstoque}" + f"\n\tPreço do Aluguel: {self.precoAluguel}\n" + "}"
        
    def printaComoFilme(nome, qtdSelecionada):
        return "{\n" + f"\tNome do Filme: {nome}\n\tqtdSelecionada: {qtdSelecionada}\n" + "}"
