from DAO.Filme.filmeDAO import *
from DAO.Cliente.ClienteDAO import *
from DAO.Funcionario.funcionarioDAO import *
from Conexao.Conexao import *

class DaoFactory():
    def __init__(self):
        self.mydb = Conexao.criaConexao()

    def createFilmeDao(self):
        return filmeDAOMySQL(self.mydb)
    
    def createClienteDao(self):
        return ClienteDAOMySQL(self.mydb)
    
    def createFuncionarioDao(self):
        return FuncionarioDAOMySQL(self.mydb)