from DAO.filmeDAO import *
from Conexao.Conexao import *

class DaoFactory():
    def createFilmeDao():
        mydb = Conexao.criaConexao()
        return filmeDAOMySQL(mydb)