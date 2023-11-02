class Funcionario:
    def __init__(self, ID, primeiroNome, ultimoNome, login, senha):
        self.ID = ID
        self.primeiroNome = primeiroNome
        self.ultimoNome = ultimoNome
        self.login = login
        self.senha = senha

    def stringFuncionario(self):
        return "{\n" + f"\tID: {self.idFuncionario}\n\tPrimeiro Nome: {self.primeiroNome}\n\tUltimo Nome: {self.segundoNome}\n\tLogin: {self.login}\n\tSenha: {self.senha}\n" + "}"

    def stringInformacoes(self):
        return "{\n" + f"\tPrimeiro Nome: {self.primeiroNome}\n\tUltimo Nome: {self.ultimoNome}\n" + "}" 
