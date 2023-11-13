class FilmeCarrinho:
    def __init__(self, id, nome, dataLancamento, genero, nomeEstudio, nomeDiretor, qtdSelecionada, precoAluguelUnidade):
        self.id = id
        self.nome = nome
        self.dataLancamento = dataLancamento
        self.genero = genero
        self.nomeEstudio = nomeEstudio
        self.nomeDiretor = nomeDiretor
        self.qtdSelecionada = qtdSelecionada
        self.precoAluguelUnidade = precoAluguelUnidade

    def stringFilmeCarrinho(self):
        return "{\n" + f"\tID: {self.id}\n\tNome: {self.nome}\n\tData de Lançamento: {self.dataLancamento}\n\tGênero: {self.genero}\n\tNome do Estúdio: {self.nomeEstudio}\n\tNome do Diretor: {self.nomeDiretor}\n\tQuantidade Selecionada: {self.qtdSelecionada}" + f"\n\tPreço do Aluguel por Unidade: {self.precoAluguelUnidade}\n" + "}"
    
    def printaAluguelFuncionario(idAluga, nomeCliente, valorTotal):
        return "{\n" + f"\tID Aluguel: {idAluga}\n\tNome do Cliente: {nomeCliente}\n\tValor Total: {valorTotal}\n" + "}"
