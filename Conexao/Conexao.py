import mysql.connector

class Conexao():
    def criaConexao():
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="RNSwRWGzz&TRifomvx4pya^#o*Dc5ZLirh!9ZRmN8*dAaFNmmf@gFk*JAZezHeqQhXAZWEyx",
        database="locadora")

        return mydb
