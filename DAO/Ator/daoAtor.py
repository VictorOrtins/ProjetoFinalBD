from Entidades.ator import *
import mysql

class AtorDAOMySQL():
    def __init__(self, database):
        """
        Construtor da classe
        Args:
            database: Conexão com o banco de dados
        """
        self.database = database
        self.cursor = database.cursor()
        self.tabela = "Ator"

    def insere(self, ator):
        query = f"INSERT INTO {self.tabela} (Nome, PaisNatal) VALUES (%s, %s)"
        values = (ator.nome, ator.paisNatal)

        try:
            self.cursor.execute(query, values)
            self.database.commit()
            idCliente = self.cursor.lastrowid
        except mysql.connector.Error as err:
            print(err)
            return False, 0

        return True, idCliente
    
    def getIdByNome(self, nome):
        query = f"SELECT ID FROM Ator WHERE Nome = %s"
        value = (nome,)

        self.cursor.execute(query, value)
        resultado = self.cursor.fetchall()

        return resultado