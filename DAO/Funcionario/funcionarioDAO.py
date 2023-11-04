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
        self.nomeTabela = "Funcionario"

    def findByLogin(self, login):
        query = f'SELECT * FROM {self.nomeTabela} WHERE Login = %s'
        value = (login, )
        self.cursor.execute(query, value)

        resultado = self.cursor.fetchall()

        colunas = [desc[0] for desc in self.cursor.description]

        if resultado == []:
             return pd.DataFrame(columns=colunas)
        
        resultado = pd.DataFrame(resultado, colunas)

        return resultado
    
    def findSenhaByLogin(self, login):
        query = f'SELECT Login,Senha FROM {self.nomeTabela} WHERE Login = %s'
        value = (login, )
        self.cursor.execute(query, value)

        resultado = self.cursor.fetchall()

        colunas = [desc[0] for desc in self.cursor.description]

        if resultado == []:
             return pd.DataFrame(columns=colunas)
        
        resultado = pd.DataFrame(resultado, colunas)

        return resultado
    
    def inserir(self, funcionario: Funcionario):
        query = f"INSERT INTO {self.nomeTabela} (PrimeiroNome, UltimoNome, Login, Senha) VALUES (%s, %s, %s, %s)"
        values = (funcionario.primeiroNome, funcionario.ultimoNome, funcionario.login, funcionario.senha)

        try:
            self.cursor.execute(query, values)
            self.database.commit()
            idFuncionario = self.cursor.lastrowid
        except mysql.connector.Error as err:
            raise err

        return idFuncionario
    
    def inserirVendedor(self, funcionario: Funcionario):
        query = f"INSERT INTO {self.nomeTabela} (PrimeiroNome, UltimoNome, Login, Senha, TipoFuncionario) VALUES (%s, %s, %s, %s, %s)"
        values = (funcionario.primeiroNome, funcionario.ultimoNome, funcionario.login, funcionario.senha, funcionario.tipoFuncionario)

        try:
            self.cursor.execute(query, values)
            self.database.commit()
            idFuncionario = self.cursor.lastrowid
        except mysql.connector.Error as err:
            raise err

        return idFuncionario
    
    def pegarID(self, login):
        query = f"SELECT ID From {self.nomeTabela} WHERE Login = %s"
        values = (login,)

        self.cursor.execute(query, values)

        resultado = self.cursor.fetchall()

        colunas = [desc[0] for desc in self.cursor.description]

        if resultado == []:
            return pd.DataFrame(columns=colunas)
        
        resultado = pd.DataFrame(resultado, colunas)

        return resultado
    
    def removerID(self, idFuncionario):
        query = f"REMOVE FROM {self.nomeTabela} WHERE ID = %s"
        values = (idFuncionario,)

        try:
            self.cursor.execute(query, values)
            self.database.commit()
        except mysql.connector.Error as err:
            print(err)
            self.database.rollback()
            return False
        
        return True
    
    def demitirVendedor(self, idVendedor):
        query = f"DELETE FROM {self.nomeTabela} WHERE ID = %s AND TipoFuncionario = %s"
        values = (idVendedor, "Vendedor")

        try:
            self.cursor.execute(query, values)
            if self.cursor.rowcount == 0:
                return False
            self.database.commit()
        except mysql.connector.Error as err:
            print(err)
            self.database.rollback()
            return False
        
        return True
    
    def findAll(self):
        query = f"SELECT * FROM {self.nomeTabela}"
         
        self.cursor.execute(query)

        resultado = self.cursor.fetchall()

        colunas = [desc[0] for desc in self.cursor.description]

        if resultado == []:
            return pd.DataFrame(columns=colunas)

        resultado = pd.DataFrame(resultado, columns=colunas)

        return resultado
         