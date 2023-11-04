import pandas as pd

class ElencoDaoMySQL():
    def __init__(self, database):
        """
        Construtor da classe
        Args:
            database: Conexão com o banco de dados
        """
        self.database = database
        self.cursor = database.cursor()

    def getFilmeByNacionalidade(self, nacionalidade):
        query = "SELECT DISTINCT IdFilme, NomeFilme, DataLancamento, Genero, NomeEstudio, NomeDiretor, qtdEstoque, precoAluguel FROM ELENCO WHERE PaisNatal = %s"
        value = (nacionalidade,)

        self.cursor.execute(query, value)

        resultado = self.cursor.fetchall()

        colunas = [desc[0] for desc in self.cursor.description]

        if resultado == []:
            return pd.DataFrame(columns=colunas)

        resultado = pd.DataFrame(resultado, columns=colunas)

        return resultado
    
    def getFilmeByAtor(self, ator):
        query = "SELECT DISTINCT IdFilme, NomeFilme, DataLancamento, Genero, NomeEstudio, NomeDiretor, qtdEstoque, precoAluguel FROM ELENCO WHERE NomeAtor = %s"
        value = (ator,)

        self.cursor.execute(query, value)

        resultado = self.cursor.fetchall()

        colunas = [desc[0] for desc in self.cursor.description]

        if resultado == []:
            return pd.DataFrame(columns=colunas)

        resultado = pd.DataFrame(resultado, columns=colunas)

        return resultado

