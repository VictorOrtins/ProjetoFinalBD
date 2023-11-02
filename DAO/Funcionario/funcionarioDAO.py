import abc
import mysql
import pandas as pd

from Entidades.funcionario import *

#Classe que define o padrão de acesso ao banco de dados
class FuncionarioDAO(metaclass=abc.ABCMeta):
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

    
class FuncionarioDAOMySQL():
    def __init__(self, database):
        """
        Construtor da classe
        Args:
            database: Conexão com o banco de dados
        """
        self.database = database
        self.cursor = database.cursor()

    def findByLogin(self, login):
        query = 'SELECT * FROM Funcionario WHERE Login = %s'
        value = (login, )
        self.cursor.execute(query, value)

        resultado = self.cursor.fetchall()

        colunas = [desc[0] for desc in self.cursor.description]

        if resultado == []:
             return pd.DataFrame(columns=colunas)
        
        resultado = pd.DataFrame(resultado, colunas)

        return resultado
    
    def findSenhaByLogin(self, login):
        query = 'SELECT Login,Senha FROM Funcionario WHERE Login = %s'
        value = (login, )
        self.cursor.execute(query, value)

        resultado = self.cursor.fetchall()

        colunas = [desc[0] for desc in self.cursor.description]

        if resultado == []:
             return pd.DataFrame(columns=colunas)
        
        resultado = pd.DataFrame(resultado, colunas)

        return resultado
    
    def inserir(self, funcionario: Funcionario):
        query = "INSERT INTO Funcionario (PrimeiroNome, UltimoNome, Login, Senha) VALUES (%s, %s, %s, %s)"
        values = (funcionario.primeiroNome, funcionario.ultimoNome, funcionario.login, funcionario.senha)

        try:
            self.cursor.execute(query, values)
            self.database.commit()
        except mysql.connector.Error as err:
            raise err

        return True
    
    def pegarID(self, login):
        query = "SELECT ID From Funcionario WHERE Login = %s"
        values = (login,)

        self.cursor.execute(query, values)

        resultado = self.cursor.fetchall()

        colunas = [desc[0] for desc in self.cursor.description]

        if resultado == []:
            return pd.DataFrame(columns=colunas)
        
        resultado = pd.DataFrame(resultado, colunas)

        return resultado
         