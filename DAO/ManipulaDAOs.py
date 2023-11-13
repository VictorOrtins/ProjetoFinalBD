
from DAO.DaoFactory import *

class ManipulaDAOs():
    def __init__(self, daoFactory: DaoFactory):
        self.daoFilme = daoFactory.createFilmeDao()
        self.daoCliente = daoFactory.createClienteDao()
        self.daoFuncionario = daoFactory.createFuncionarioDao()
        self.daoElenco = daoFactory.createElencoDao()
        self.daoDVD = daoFactory.createDvdDAO()
        self.daoGeral = daoFactory.createDaoGeral()
        self.daoAtor = daoFactory.createDaoAtor()

    