class Funcionario:
    def __init__(self, ID, primeiroNome, ultimoNome, login, senha, tipoFuncionario):
        self.ID = ID
        self.primeiroNome = primeiroNome
        self.ultimoNome = ultimoNome
        self.login = login
        self.senha = senha
        self.tipoFuncionario = tipoFuncionario

    def stringFuncionario(self):
        return "{\n" + f"\tID: {self.ID}\n\tPrimeiro Nome: {self.primeiroNome}\n\tUltimo Nome: {self.ultimoNome}\n\tLogin: {self.login}\n\tSenha: {self.senha}\n\tTipo de Funcionario: {self.tipoFuncionario}\n" + "}"

    def stringInformacoes(self):
        return "{\n" + f"\tPrimeiro Nome: {self.primeiroNome}\n\tUltimo Nome: {self.ultimoNome}\n\tTipo de Funcionario: {self.tipoFuncionario}\n" + "}" 
