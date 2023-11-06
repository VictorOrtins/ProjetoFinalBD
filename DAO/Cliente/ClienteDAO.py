import abc
import mysql
import pandas as pd

from Entidades.cliente import *

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
            callable(subclass.inserir) and
            hasattr(subclass, 'pegarID') and 
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
        self.tabela = "Cliente"

    def findByLogin(self, login):
        query = f'SELECT * FROM {self.tabela} WHERE Login = %s'
        value = (login, )
        self.cursor.execute(query, value)

        resultado = self.cursor.fetchall()

        colunas = [desc[0] for desc in self.cursor.description]

        if resultado == []:
             return pd.DataFrame(columns=colunas)
        
        resultado = pd.DataFrame(resultado, colunas)

        return resultado
    
    def findSenhaByLogin(self, login):
        query = f'SELECT Login,Senha FROM {self.tabela} WHERE Login = %s'
        value = (login, )
        self.cursor.execute(query, value)

        resultado = self.cursor.fetchall()

        colunas = [desc[0] for desc in self.cursor.description]

        if resultado == []:
             return pd.DataFrame(columns=colunas)
        
        resultado = pd.DataFrame(resultado, colunas)

        return resultado
    
    def inserir(self, cliente: Cliente):
        query = f"INSERT INTO {self.tabela} (CPF, PrimeiroNome, UltimoNome, Cidade, IsFlamengo, AssisteOnePiece) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (cliente.cpf, cliente.primeiroNome, cliente.ultimoNome, cliente.cidade, cliente.isFlamengo, cliente.assisteOnePiece)

        try:
            self.cursor.execute(query, values)
            self.database.commit()
            idCliente = self.cursor.lastrowid
        except mysql.connector.Error as err:
            raise err

        return idCliente
    
    def pegarID(self, login):
        query = f"SELECT ID From {self.tabela} WHERE Login = %s"
        values = (login,)

        self.cursor.execute(query, values)

        resultado = self.cursor.fetchall()

        colunas = [desc[0] for desc in self.cursor.description]

        if resultado == []:
            return pd.DataFrame(columns=colunas)
        
        resultado = pd.DataFrame(resultado, colunas)

        return resultado
    
    def findIdByCPF(self, cpf):
        query = f'SELECT ID FROM {self.tabela} WHERE CPF = %s'
        value = (cpf, )
        self.cursor.execute(query, value)

        resultado = self.cursor.fetchall()

        colunas = [desc[0] for desc in self.cursor.description]

        if resultado == []:
             return pd.DataFrame(columns=colunas)
        
        resultado = pd.DataFrame(resultado, colunas)

        return resultado
    
    def findIdNomeByCPF(self, cpf):
        query = f'SELECT ID, PrimeiroNome, UltimoNome FROM {self.tabela} WHERE CPF = %s'
        value = (cpf, )

        self.cursor.execute(query, value)

        resultado = self.cursor.fetchall()
        colunas = [desc[0] for desc in self.cursor.description]

        if resultado == []:
            return pd.DataFrame(columns=colunas)
        
        resultado = pd.DataFrame(resultado, colunas)

        return resultado

    def findByCPF(self, cpf):
        query = f'SELECT * FROM {self.tabela} WHERE CPF = %s'
        value = (cpf, )
        self.cursor.execute(query, value)

        resultado = self.cursor.fetchall()

        colunas = [desc[0] for desc in self.cursor.description]

        if resultado == []:
             return pd.DataFrame(columns=colunas)
        
        resultado = pd.DataFrame(resultado, colunas)

        return resultado


         