import mysql
import pandas as pd

class DaoGeralMySQL():
    def __init__(self, database):
        self.database = database
        self.cursor = database.cursor()

    def inserirAluguel(self, idCliente, idFuncionario, valorFinal, formaPagamento, itens):
        temp_table = "Carrinho"

        self.criaTabelaTemporaria(temp_table)
        for item in itens:
            query = f'INSERT INTO {temp_table}(IdFilme, NumItens) VALUES (%s, %s)'

            value = (item.id, item.qtdSelecionada)

            self.cursor.execute(query, value)

            try:
                self.database.commit()
            except mysql.error as e:
                raise e

        self.cursor.callproc("ProcessarCompra", ( int(idCliente), int(idFuncionario), float(valorFinal), formaPagamento ) )

        self.destroiTabelaTemporaria(temp_table)

    def pegarFilmesSemDevolucao(self, idCliente):
        query = 'SELECT IdAluga, Nome, NumDeItens, IdFilme FROM DVDsNaoDevolvidos WHERE IdCliente = %s ORDER BY IdAluga ASC'
        value = (idCliente,)

        self.cursor.execute(query, value)

        resultado = self.cursor.fetchall()

        return resultado
    
    def pegarTudoFilmesSemDevolucao(self, idCliente):
        query = 'SELECT * FROM DVDsNaoDevolvidos WHERE IdCliente = %s ORDER BY IdAluga ASC'
        value = (idCliente,)

        self.cursor.execute(query, value)

        resultado = self.cursor.fetchall()

        return resultado
    
    def devolverFilme(self, idAluga, idFilme):
        query = 'UPDATE DVD SET Devolvido = True WHERE IdAluga = %s AND IdFilme = %s'
        value = (idAluga, idFilme)

        self.cursor.execute(query, value)

        self.database.commit()

    def verHistoricoCliente(self, id):
        query = 'SELECT IdAluga, Nome, NumDeItens, IdFilme, Devolvido FROM ALUGA A INNER JOIN DVD D ON A.ID = D.IdAluga INNER JOIN Cliente C ON A.IdCliente = C.ID INNER JOIN Filme F ON F.ID = D.IdFilme WHERE IdCliente = %s'
        value = (id,)

        self.cursor.execute(query, value)

        resultado = self.cursor.fetchall()

        return resultado
    
    def pegaAluguelFuncionario(self, idFuncionario):
        query = 'SELECT A.ID, PrimeiroNome, UltimoNome, ValorFinal FROM Aluga A  INNER JOIN CLIENTE C ON  A.IdCliente = C.ID WHERE IdFuncionario = %s'
        value = (idFuncionario,)

        self.cursor.execute(query, value)

        resultado = self.cursor.fetchall()

        return resultado
    
    def insereParticipa(self, idAtor, idFilme):
        query = 'INSERT INTO Participa(IdFilme, IdAtor) VALUES (%s, %s)'
        value = (idFilme, idAtor)

        self.cursor.execute(query, value)

        self.database.commit()
        

    def criaTabelaTemporaria(self, nome):
        query = f'CREATE TEMPORARY TABLE {nome} (IdAluga INT, IdFilme INT ,NumItens INT)'

        self.cursor.execute(query)
        self.database.commit()


    def destroiTabelaTemporaria(self, nome):
        query = f'DROP TEMPORARY TABLE {nome}'

        self.cursor.execute(query)
        self.database.commit()


