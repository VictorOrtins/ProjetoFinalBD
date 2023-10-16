import os
import time
import sys


#Classe para fazer a manipulação de cores de texto no terminal
#O ideal era ter feito um Enum, porém eu só vi como funcionava direito depois. Por enquanto tá assim
class Texto():
    def branco():
        return str('\033[0m')
    def negrito():
        return str('\033[1m')
    def fraco():
        return str('\033m[2m')
    def italico():
        return str('\033[3m')
    def underline():
        return str('\033[4m')
    def vermelho():
        return str('\033[31m')
    def verde():
        return str('\033[32m')
    def amarelo():
        return str('\033[33m')
    def azul():
        return str('\033[34m')
    def magenta():
        return str('\033[35m')
    def ciano():
        return str('\033[36m')
    def cinza():
        return str('\033[37m')
    def reset():
        return str('\033[m')

#Classe para fazer a manipulação de cores do background do terminal. 
#Por enquanto não foi utilizada porém achei bom deixá-la 
class Background():
    def negativo():
        return str('\033[7m')
    def branco():
        return str('\033[40m')
    def vermelho():
        return str('\033[41m')
    def verde():
        return str('\033[42m')
    def amarelo():
        return str('\033[43m')
    def azul():
        return str('\033[44m')
    def magenta():
        return str('\033[45m')
    def ciano():
        return str('\033[46m')
    def cinza():
        return str('\033[47m')
    def reset():
        return str('\033[m')

#Função que simula a sensação de carregamento entre telas
def loading(message, cor):
    """
    Faz o processo de carregamento entre as telas. A sensação de tempo
    entre os menus é simulada pelo time.sleep utilizado na função. Já reseta
    a cor do terminal para a original, ou seja, branco
    Args:
        message: Mensagem de carregamento
        cor: Cor que a mensagem de carregamento tomará
    """
    print(cor)
    for i in message:
        print(i, end = "")
        sys.stdout.flush()
        time.sleep(0.1)
    print("...\n", Texto.branco())
    
    time.sleep(0.8)
    sys.stdout.flush()
    os.system('cls')

#Função que Pergunta se o usuário quer alterar um atributo do filme
def whileAlterarYN(stringMudar, stringNovo, stringErro, expressaoErro):
    """
    Pergunta se o usuário quer ou não alterar um dos atributos do filme
    Args:
        stringMudar: String de saída que perguntará o que o usuário poderá mudar
        stringNovo: String de saída que perguntará qual o novo do respectivo atributo
        stringErro: String de saída que dirá se a entrada digitada pelo usuário é inválida
    Returns:
        O retorno depende da expressão de erro.
    """
    while(True):
        mudar = input(stringMudar).upper()
        if mudar == "N":
            return None
        elif mudar == "Y":
            # caractFilme = input(stringNovo)
            caractFilme = checaEntrada(stringNovo, stringErro, expressaoErro)
            break
        print(textoCor("Opção Inválida!\n", Texto.vermelho()))

    return caractFilme

#Função que pergunta se o usuário que fazer mais daquela operação
def whileOutro(stringOutro):
    """
    Pergunta se o usuário quer fazer outra da respetiva operação
    Args:
        stringOutro: String de saída perguntando se quer repetir a operação
    Returns:
        boolean: Indica o valor que a condição do while mais externo deve ser após o input do usuário
    """
    menu = True
    while(True):
        outroFilme = input(stringOutro).upper()
        if outroFilme == "N":
            menu = False
            break
        elif outroFilme == "Y":
            break

    return menu

#Função que printa os títulos dos menus
def titulo(txtTitulo, cor=Texto.branco()):
    """
    Printa os títulos dos menus na tela
    Args:
        txtTitulo: texto do título
        cor: cor do texto. Por padrão é branco
    """
    print(f"{cor}==== {txtTitulo} ===={Texto.reset()}\n\n")

#Função que dá cor a um texto
def textoCor(txt, cor):
    """
    Pinta um respectivo texto. Ela não printa o texto na tela,e sim retorna
    Args:
        txt: Texto a ser customizado
        cor: Cor do texto
    Returns:
        string: Texto colorido
    """
    return f"{cor}{txt}{Texto.reset()}"

#Função que checa uma das entradas do usuário
def checaEntrada(entrada, msgErro, expressaoErro):
    """
    Função que checa se uma determinada entrada é válida. Se não for, o loop continua até ela ser válida
    Args:
        entrada: Texto de input para o usuário
        msgErro: Mensagem que será mostrada quando o usuário digitar uma entrada inválida
        expressaoErro: Expressão que irá checar a validade da entrada
    Returns:
        Depende da expressão de erro: Representa o atributo do filme que foi digitado
    """
    while(True):
        nomeCaract = input(entrada)
        if expressaoErro(nomeCaract):
            print(textoCor(msgErro, Texto.vermelho()), end="\n\n")
            continue
        return nomeCaract

def checaSeData(entrada):
    """
    Função que checa se uma determinada entrada é uma data válida, no formato Ano-Mês-Dia
    Args:
        entrada: Entrada a ser checada pela função
    Returns:
        Boolean: Verdadeiro quer dizer que a entrada foi válida, falso se é inválida
    """
    try:
        time.strptime(entrada, '%Y-%m-%d') #Checa se a entrada é uma data
    except ValueError:
        return False

    return True

def checaSeCPF(entrada):
    if not(entrada.isdigit()):
        return False
    
    if len(entrada) != 11:
        return False
    
    if entrada == entrada[0]*11:
        return False
    
    return True
    