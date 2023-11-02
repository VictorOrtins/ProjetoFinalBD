
from DAO.DaoFactory import *

class ManipulaDAOs():
    def __init__(self, daoFactory: DaoFactory):
        self.daoFilme = daoFactory.createFilmeDao()
        self.daoCliente = daoFactory.createClienteDao()
        self.daoFuncionario = daoFactory.createFuncionarioDao()

    