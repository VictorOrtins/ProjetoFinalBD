import abc
import mysql
import pandas as pd

from Entidades.filme import *

#Classe que define o padrão de acesso ao banco de dados
class FilmeDAO(metaclass=abc.ABCMeta):
    """
    Interface que define as funções que um Data Acess Object de um Filme devem ter
    """
    @classmethod
    def __subclasshook__(cls, subclass):
            return (hasattr(subclass, 'inserir') and 
            callable(subclass.inserir) and 
            hasattr(subclass, 'updateById') and 
            callable(subclass.update) and 
            hasattr(subclass, 'deleteById') and 
            callable(subclass.deleteById) and
            hasattr(subclass, 'findById') and 
            callable(subclass.findById) and
            hasattr(subclass, 'findByName') and 
            callable(subclass.findByName) and
            hasattr(subclass, 'findAll') and 
            callable(subclass.findAll) and 
            hasattr(subclass, 'countInstances') and
            callable(subclass.countInstances) and
            hasattr(subclass, 'sumPrecoAluguel') and
            callable(subclass.sumPrecoAluguel) and
            hasattr(subclass, 'sumQtdEstoque') and
            callable(subclass.sumQtdEstoque))

#Implementação de um DAO Filme para o MySql
class filmeDAOMySQL():
    """
    Implementação do DAO filme para o MySQL
    """
    def __init__(self, database):
        """
        Construtor da classe
        Args:
            database: Conexão com o banco de dados
        """
        self.database = database
        self.cursor = database.cursor()

    
    def inserir(self, filme: Filme):
        query = "INSERT INTO Filme (Nome, DataLancamento, Genero, NomeEstudio, NomeDiretor, qtdEstoque, precoAluguel) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (filme.nome, filme.dataLancamento, filme.genero, filme.nomeEstudio, filme.nomeDiretor, filme.qtdEstoque, filme.precoAluguel)

        try:
            self.cursor.execute(query, values)
            self.database.commit()
            idFilme = self.cursor.lastrowid
        except mysql.connector.Error as err:
            self.database.rollback()
            return False

        return True, idFilme
    
    def updateById(self, filme):
        query = 'UPDATE Filme SET Nome = %s, DataLancamento = %s, Genero = %s, NomeEstudio = %s, NomeDiretor = %s, qtdEstoque = %s, precoAluguel = %s WHERE ID = %s'
        values = (filme.nome, filme.dataLancamento, filme.genero, filme.nomeEstudio, filme.nomeDiretor, filme.qtdEstoque, filme.precoAluguel ,filme.id)

        try:
            self.cursor.execute(query, values)
            self.database.commit()
        except mysql.connector.Error as err:
            self.database.rollback()
            return False

        return True
    
    def deleteById(self, idFilme):
        query = 'DELETE FROM Filme WHERE ID = %s'
        value = (idFilme,)

        try:
            self.cursor.execute(query, value)
            self.database.commit()
        except mysql.connector.Error as err:
            print(err)
            self.database.rollback()
            return False

        return True

    def findById(self, idFilme):
        query = 'SELECT * FROM Filme WHERE ID = %s'
        value = (idFilme,)
        self.cursor.execute(query, value)

        resultado = self.cursor.fetchall()

        if resultado == []:
            return None

        return resultado[0]

    def findByName(self, nomeFilme):
        query = 'SELECT * FROM Filme WHERE Nome LIKE %s'
        value = ('%' + nomeFilme + '%',)
        self.cursor.execute(query, value)

        resultado = self.cursor.fetchall()

        colunas = [desc[0] for desc in self.cursor.description]

        if resultado == []:
            return pd.DataFrame(columns=colunas)

        resultado = pd.DataFrame(resultado, columns=colunas)

        return resultado

    
    def findByRangePrice(self, range1, range2):
        query = 'SELECT * FROM Filme WHERE precoAluguel BETWEEN %s AND %s ORDER BY precoAluguel ASC'

        value = (range1, range2)

        self.cursor.execute(query, value)

        resultado = self.cursor.fetchall()

        colunas = [desc[0] for desc in self.cursor.description]

        if resultado == []:
            return pd.DataFrame(columns=colunas)
        
        resultado = pd.DataFrame(resultado, columns=colunas)

        return resultado
    
    def findByDirector(self, diretor):
        query = 'SELECT * FROM Filme WHERE NomeDiretor = %s'

        value = (diretor,)

        self.cursor.execute(query, value)

        resultado = self.cursor.fetchall()

        colunas = [desc[0] for desc in self.cursor.description]

        if resultado == []:
            return pd.DataFrame(columns=colunas)
        
        resultado = pd.DataFrame(resultado, columns=colunas)

        return resultado
    
    def findByRangeQtdEstoque(self, range1, range2):
        query = 'SELECT * FROM Filme WHERE qtdEstoque BETWEEN %s AND %s ORDER BY qtdEstoque DESC'

        value = (range1, range2)

        self.cursor.execute(query, value)

        resultado = self.cursor.fetchall()

        colunas = [desc[0] for desc in self.cursor.description]

        if resultado == []:
            return pd.DataFrame(columns=colunas)
        
        resultado = pd.DataFrame(resultado, columns=colunas)

        return resultado
    
    def findByGenre(self, genre):
        query = 'SELECT * FROM Filme WHERE Genero = %s'

        value = (genre,)

        self.cursor.execute(query, value)

        resultado = self.cursor.fetchall()

        colunas = [desc[0] for desc in self.cursor.description]

        if resultado == []:
            return pd.DataFrame(columns=colunas)
        
        resultado = pd.DataFrame(resultado, columns=colunas)

        return resultado


    def findAll(self):
        query = 'SELECT * FROM Filme'
        self.cursor.execute(query)

        resultado = self.cursor.fetchall()

        colunas = [desc[0] for desc in self.cursor.description]

        if resultado == []:
            return pd.DataFrame(columns=colunas)

        resultado = pd.DataFrame(resultado, columns=colunas)

        return resultado

    def countInstances(self):
        query = 'SELECT COUNT(*) FROM FILME'
        self.cursor.execute(query)

        resultado = self.cursor.fetchall()

        return resultado[0][0]

    def sumPrecoAluguel(self):
        query = 'SELECT SUM(precoAluguel) FROM FILME'
        self.cursor.execute(query)

        resultado = self.cursor.fetchall()

        return resultado[0][0]

    def sumQtdEstoque(self):
        query = 'SELECT SUM(qtdEstoque) FROM FILME'
        self.cursor.execute(query)

        resultado = self.cursor.fetchall()

        return resultado[0][0]
    
    def existeFilmeDeID(self, ID):
        query = 'SELECT * FROM Filme WHERE ID = %s'
        value = (ID,)
        self.cursor.execute(query, value)

        resultado = self.cursor.fetchall()

        if resultado == []:
            return False

        return True





