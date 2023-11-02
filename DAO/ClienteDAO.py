import abc
import pandas as pd

from Entidades import Cliente

#Classe que define o padrão de acesso ao banco de dados
class ClienteDAO(metaclass=abc.ABCMeta):
    """
    Interface que define as funções que um Data Acess Object de um Filme devem ter
    """
    @classmethod
    def __subclasshook__(cls, subclass):
            return (hasattr(subclass, 'inserir') and 
            callable(subclass.inserir) and
            hasattr(subclass, 'findByLogin') and 
            callable(subclass.inserir) and
            hasattr(subclass, 'findSenhaByLogin') and 
            callable(subclass.inserir)
            )

    
class ClienteDAOMySQL():
    def __init__(self, database):
        """
        Construtor da classe
        Args:
            database: Conexão com o banco de dados
        """
        self.database = database
        self.cursor = database.cursor()

    def findByLogin(self, login):
        query = 'SELECT * FROM WHERE Login = %s'
        value = (login, )
        self.cursor.execute(query, value)

        resultado = self.cursor.fetchall()

        colunas = [desc[0] for desc in self.cursor.description]

        if resultado == []:
             return pd.DataFrame(columns=colunas)
        
        resultado = pd.DataFrame(resultado, colunas)

        return resultado
    
    def findSenhaByLogin(self, login):
        query = 'SELECT Login,Senha FROM WHERE Login = %s'
        value = (login, )
        self.cursor.execute(query, value)

        resultado = self.cursor.fetchall()

        colunas = [desc[0] for desc in self.cursor.description]

        if resultado == []:
             return pd.DataFrame(columns=colunas)
        
        resultado = pd.DataFrame(resultado, colunas)

        return resultado
         