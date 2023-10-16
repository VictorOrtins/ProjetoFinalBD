class Funcionario:
    def __init__(self, cpf, nome, idFuncionario, senha):
        self.cpf = cpf
        self.nome = nome
        self.idFuncionario = idFuncionario
        self.senha = senha

    def stringFuncionario(self):
        return "{\n" + f"\tID: {self.idFuncionario}\n\tCPF: {self.cpf}\n\tNome: {self.nome}\n\tSenha: {self.senha}\n" + "}" 
