import mysql

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
        


    def criaTabelaTemporaria(self, nome):
        query = f'CREATE TEMPORARY TABLE {nome} (IdAluga INT, IdFilme INT ,NumItens INT)'

        self.cursor.execute(query)
        self.database.commit()


    def destroiTabelaTemporaria(self, nome):
        query = f'DROP TEMPORARY TABLE {nome}'

        self.cursor.execute(query)
        self.database.commit()


