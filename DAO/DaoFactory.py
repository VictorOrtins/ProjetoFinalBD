from DAO.Filme.filmeDAO import *
from DAO.Cliente.ClienteDAO import *
from DAO.Funcionario.funcionarioDAO import *
from DAO.Elenco.elencoDAO import *
from DAO.DVD.dvdDAO import *

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
    
    def createElencoDao(self):
        return ElencoDaoMySQL(self.mydb)
    
    def createDvdDAO(self):
        return DvdDaoMySQL(self.mydb)