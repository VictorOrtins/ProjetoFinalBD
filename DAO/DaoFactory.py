from DAO.filmeDAO import *
from DAO.ClienteDAO import *
from Conexao.Conexao import *

class DaoFactory():
    def __init__(self):
        self.mydb = Conexao.criaConexao()

    def createFilmeDao(self):
        return filmeDAOMySQL(self.mydb)
    
    def createClienteDao(self):
        return ClienteDAOMySQL(self.mydb)