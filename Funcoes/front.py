from enum import Enum

from Funcoes.funcoesAuxiliares import *

from DAO.DaoFactory import *


from Entidades.cliente import *
from Entidades.funcionario import *
from Entidades.filme import *
from Entidades.dvd import *

class TipoUsuario(Enum):
    CLIENTE = 1
    FUNCIONARIO = 2
    SEM_LOGIN = 3

tipoUsuario = TipoUsuario.SEM_LOGIN
usuario = None

carrinho = [DVD(1, 6, "Avengers Endgame"), DVD(2, 5, "Barbie")]


def iniciar():
    os.system('cls')
    login()

def login():
    listaFuncoes = [loginCliente, loginFuncionario, menuLoja, sairLoja]
    while(True):
        titulo("ESCOLHA DE LOGIN", Texto.negrito())

        print(f"{textoCor("1 - ", Texto.azul())}Login Cliente\n")
        print(f"{textoCor("2 - ", Texto.azul())}Login Funcionário\n")
        print(f"{textoCor("3 - ", Texto.azul())}Entrar sem Login\n")
        print(f"{textoCor("4 - ", Texto.azul())}Sair da loja\n")

        try:
            opcao = int(input("Escolha uma opção: "))
        except ValueError: #Trata um input não numeral
            print(textoCor("Opcão Inválida!\n",Texto.vermelho()))
            loading("Recarregando", Texto.ciano())
            continue
            
        if opcao <= 0 or opcao > 4: #Trata um input fora das opções válidas
            print(textoCor("Opcão Inválida!\n",Texto.vermelho()))
            loading("Recarregando", Texto.ciano())
            continue

        break

    if opcao != 4:
        loading("Carregando", Texto.amarelo())
    listaFuncoes[opcao - 1]()


def loginCliente():
    global tipoUsuario
    global usuario

    titulo("LOGIN CLIENTE", Texto.negrito())
    cliente = Cliente(1, "Teste", "09933758470", "Av Manoel Morais, 632", "Victor12", True, False)

    while(True):
        naoEncontrado = False

        cpf = checaEntrada("Usuário (CPF): ", "Digite um CPF válido!", lambda x: not(checaSeCPF(x)))
        senha = checaEntrada("Senha: ", "", lambda x: False)

        if cliente.cpf != cpf:
            print(textoCor("Usuário não encontrado!", Texto.vermelho()))
            naoEncontrado = True

        if cliente.senha != senha:
            print(textoCor("Senha inválida!", Texto.vermelho()))
            naoEncontrado = True

        if naoEncontrado:
            continuar = whileOutro("Deseja continuar sem login? (Y/N)")
            if continuar:
                break
            loading("Recarregando", Texto.amarelo())
            continue


        break
    
    if not(naoEncontrado):
        print(textoCor("\nLogin de Cliente bem-sucedido!", Texto.verde()))
        tipoUsuario = TipoUsuario.CLIENTE
        usuario = cliente

    loading("Carregando", Texto.amarelo())
    menuLoja()


def loginFuncionario():
    global tipoUsuario
    global usuario

    funcionario = Funcionario("09933758470", "Victor Ortins", 1, "Victor12")

    while(True):
        naoEncontrado = False

        titulo("LOGIN FUNCIONÁRIO", Texto.negrito())
        cpf = checaEntrada("Usuário (CPF): ", "Digite um CPF válido!", lambda x: not(checaSeCPF(x)))
        senha = checaEntrada("Senha: ", "", lambda x: False)

        if funcionario.cpf != cpf:
            print(textoCor("CPF não encontrado!", Texto.vermelho()))
            naoEncontrado = True

        if funcionario.senha != senha:
            print(textoCor("Senha inválida!", Texto.vermelho()))
            naoEncontrado = True

        if naoEncontrado:
            continuar = whileOutro("Deseja continuar sem login? (Y/N)")
            if continuar:
                break

            loading("Recarregando", Texto.amarelo())
            continue

        break
    
    if not(naoEncontrado):
        print(textoCor("\nLogin de Funcionário bem-sucedido!", Texto.verde()))
        tipoUsuario = TipoUsuario.FUNCIONARIO
        usuario = funcionario

    loading("Carregando", Texto.amarelo())
    menuLoja()

def menuLoja():

    if tipoUsuario == TipoUsuario.FUNCIONARIO:
        listaFuncoes = [menuInformacoesUsuario, menuCadastroEstoque, sairLoja]
        txtInput = "".join([f"{textoCor("Funcionário: ", Texto.magenta())}{usuario.nome}\n\n",f"{textoCor("1 - ", Texto.azul())}Informações do Usuário\n\n",
        f"{textoCor("2 - ", Texto.azul())}Cadastro de Estoque\n\n", f"{textoCor("3 - ", Texto.azul())}Sair da Loja\n"])

        teste = 3

    elif tipoUsuario == TipoUsuario.CLIENTE:
        listaFuncoes = [menuInformacoesUsuario, menuAluguelDeFilmes, verCarrinho, sairLoja]
        txtInput = "".join([f"{textoCor("Cliente: ", Texto.verde())}{usuario.nome}\n\n",f"{textoCor("1 - ", Texto.azul())}Informações do Usuário\n\n" 
        ,f"{textoCor("2 - ", Texto.azul())}Aluguel de Filmes\n\n",f"{textoCor("3 - ", Texto.azul())}Ver Carrinho\n\n",
        f"{textoCor("4 - ", Texto.azul())}Sair da Loja\n"])

        teste = 4

    elif tipoUsuario == TipoUsuario.SEM_LOGIN:
        listaFuncoes = [menuAluguelDeFilmes, verCarrinho, login, sairLoja]
        txtInput = "".join([
        f"{textoCor("1 - ", Texto.azul())}Aluguel de Filmes\n\n",f"{textoCor("2 - ", Texto.azul())}Ver Carrinho\n\n", f"{textoCor("3 - ", Texto.azul())}Fazer Login\n\n",
        f"{textoCor("4 - ", Texto.azul())}Sair da Loja\n"])

        teste = 4


    while(True):
        titulo("MENU DA LOJA", Texto.negrito())

        print(txtInput)

        try:
            opcao = int(input("Escolha uma opção: "))
        except ValueError: #Trata um input não numeral
            print(textoCor("Opcão Inválida!\n",Texto.vermelho()))
            loading("Recarregando", Texto.ciano())
            continue
        
        
        if opcao <= 0 or opcao > teste: #Trata um input fora das opções válidas
            print(textoCor("Opcão Inválida!\n",Texto.vermelho()))
            loading("Recarregando", Texto.ciano())
            continue

        break

    if opcao != 4:
        loading("Carregando", Texto.ciano())
    listaFuncoes[opcao - 1]()

def menuInformacoesUsuario():
    global tipoUsuario

    if tipoUsuario == TipoUsuario.CLIENTE:
        listaFuncoes = [exibirInformacoesUsuario, exibirHistoricoFilmes, menuLoja, sairConta]
        txtInput = "".join([f"{textoCor("Cliente: ", Texto.verde())}{usuario.nome}\n\n",f"{textoCor("1 - ", Texto.azul())}Exibir Informações do Cliente\n\n",
        f"{textoCor("2 - ", Texto.azul())}Histórico de Filmes Alugados\n\n", f"{textoCor("3 - ", Texto.azul())}Voltar para o Menu da Loja\n\n",
        f"{textoCor("4 - ", Texto.azul())}Sair da conta\n\n"])

    elif tipoUsuario == TipoUsuario.FUNCIONARIO:
        listaFuncoes = [exibirInformacoesUsuario, alugueisConfirmacao, menuLoja, sairConta]
        txtInput = "".join([f"{textoCor("Funcionário: ", Texto.magenta())}{usuario.nome}\n\n",f"{textoCor("1 - ", Texto.azul())}Exibir Informações do Funcionário\n\n",
        f"{textoCor("2 - ", Texto.azul())}Aluguéis pendentes de confirmação\n\n", f"{textoCor("3 - ", Texto.azul())}Voltar para o Menu da Loja\n\n",
        f"{textoCor("4 - ", Texto.azul())}Sair da conta\n\n"])
    elif tipoUsuario == TipoUsuario.SEM_LOGIN:
        print(textoCor("ERRO!!!", Texto.vermelho()))
        sys.exit()

    while(True):
        teste = 4

        titulo("MENU DO USUÁRIO", Texto.negrito())

        print(txtInput)

        try:
            opcao = int(input("Escolha uma opção: "))
        except ValueError: #Trata um input não numeral
            print(textoCor("Opcão Inválida!\n",Texto.vermelho()))
            loading("Recarregando", Texto.ciano())
            continue
        
        
        if opcao <= 0 or opcao > teste: #Trata um input fora das opções válidas
            print(textoCor("Opcão Inválida!\n",Texto.vermelho()))
            loading("Recarregando", Texto.ciano())
            continue

        break

    if opcao != 4 :
        loading("Carregando", Texto.ciano())
    
    listaFuncoes[opcao - 1]()

def menuAluguelDeFilmes():
    global tipoUsuario

    if tipoUsuario == TipoUsuario.CLIENTE:
        listaFuncoes = [pesquisarNome, pesquisarPreco, pesquisarGenero, menuLoja]
        txtInput = "".join([f"{textoCor("Cliente: ", Texto.verde())}{usuario.nome}\n\n",f"{textoCor("1 - ", Texto.azul())}Pesquisar por Nome\n\n",
        f"{textoCor("2 - ", Texto.azul())}Pesquisar por Preço\n\n", f"{textoCor("3 - ", Texto.azul())}Pesquisar por Gênero\n\n",
        f"{textoCor("4 - ", Texto.azul())}Voltar para o menu da loja\n\n"])
    elif tipoUsuario == TipoUsuario.SEM_LOGIN:
        listaFuncoes = [pesquisarNome, pesquisarPreco, pesquisarGenero, menuLoja]
        txtInput = "".join([f"{textoCor("1 - ", Texto.azul())}Pesquisar por Nome\n\n",
        f"{textoCor("2 - ", Texto.azul())}Pesquisar por Preço\n\n", f"{textoCor("3 - ", Texto.azul())}Pesquisar por Gênero\n\n",
        f"{textoCor("4 - ", Texto.azul())}Voltar para o menu da loja\n\n"])


    while(True):
        teste = 4

        titulo("ALUGUEL DE FILMES", Texto.negrito())

        print(txtInput)

        try:
            opcao = int(input("Escolha uma opção: "))
        except ValueError: #Trata um input não numeral
            print(textoCor("Opcão Inválida!\n",Texto.vermelho()))
            loading("Recarregando", Texto.ciano())
            continue
        
        
        if opcao <= 0 or opcao > teste: #Trata um input fora das opções válidas
            print(textoCor("Opcão Inválida!\n",Texto.vermelho()))
            loading("Recarregando", Texto.ciano())
            continue

        break

    loading("Carregando", Texto.ciano())
    
    listaFuncoes[opcao - 1]()

def pesquisarNome():
    global carrinho

    nomeFilme = input("Nome do Filme que você deseja pesquisar: ")

    filmes = [Filme(2, "Avengers Endgame", "2019-09-05", "Herói", "Marvel", "Joe Russo", 9, 8.7),
              Filme(1, "Revenge of The Sith", "2005-05-05", "Ficção", "Lucasfilm", "George Lucas", 10, 12),
              ]

    for filme in filmes:
        print(filme.stringFilme())

    adicionar = whileOutro("Deseja adicionar um desses filmes no carrinho? (Y/N)")
    if adicionar:
        while(True):
            id = input("Digite o ID do filme que deseja adicionar no carrinho: ")
            if not(id.isdigit()):
                print(f"{textoCor("ID inválido!", Texto.vermelho())}")
                continue

            break
        
        for filme in filmes:
            if filme.id == int(id):
                carrinho.append(DVD(filme.id, 1, filme.nome))
                break
        
        loading("Carregando", Texto.ciano())
        menuAluguelDeFilmes()
    else:
        loading("Carregando", Texto.ciano())
        menuAluguelDeFilmes()

def pesquisarPreco():
    global carrinho

    rangePreco = input("Expressão de preço que deseja pesquisar: (Ex: preco > 10 and preco < 20) ")

    filmes = [Filme(2, "Avengers Endgame", "2019-09-05", "Herói", "Marvel", "Joe Russo", 9, 8.7),
              Filme(1, "Revenge of The Sith", "2005-05-05", "Ficção", "Lucasfilm", "George Lucas", 10, 12),
              ]

    for filme in filmes:
        print(filme.stringFilme())

    adicionar = whileOutro("Deseja adicionar um desses filmes no carrinho? (Y/N)")
    if adicionar:
        while(True):
            id = input("Digite o ID do filme que deseja adicionar no carrinho: ")
            if not(id.isdigit()):
                print(f"{textoCor("ID inválido!", Texto.vermelho())}")
                continue

            break
        
        for filme in filmes:
            if filme.id == int(id):
                carrinho.append(DVD(filme.id, 1, filme.nome))
                break
        
        loading("Carregando", Texto.ciano())
        menuAluguelDeFilmes()
    else:
        loading("Carregando", Texto.ciano())
        menuAluguelDeFilmes()

def pesquisarGenero():
    global carrinho

    genero = input("Gênero do filme que desejas pesquisar: ")

    filmes = [Filme(2, "Avengers Endgame", "2019-09-05", "Herói", "Marvel", "Joe Russo", 9, 8.7),
              Filme(1, "Revenge of The Sith", "2005-05-05", "Ficção", "Lucasfilm", "George Lucas", 10, 12),
              ]

    for filme in filmes:
        print(filme.stringFilme())

    adicionar = whileOutro("Deseja adicionar um desses filmes no carrinho? (Y/N)")
    if adicionar:
        while(True):
            id = input("Digite o ID do filme que deseja adicionar no carrinho: ")
            if not(id.isdigit()):
                print(f"{textoCor("ID inválido!", Texto.vermelho())}")
                continue

            break
        
        for filme in filmes:
            if filme.id == int(id):
                carrinho.append(DVD(filme.id, 1, filme.nome))
                break
        
        loading("Carregando", Texto.ciano())
        menuAluguelDeFilmes()
    else:
        loading("Carregando", Texto.ciano())
        menuAluguelDeFilmes()


def menuCadastroEstoque():
    menuCadastro()

def voltarMenuLoja():
    loading("Carregando", Texto.ciano())
    menuLoja()

def verCarrinho():
    global carrinho

    titulo("CARRINHO", Texto.negrito())

    if carrinho == []:
        print("O carrinho está vazio!\n")
        loading("Carregando", Texto.ciano())
        menuLoja()
    else:
        print(len(carrinho))
        for item in carrinho:
            print(item.stringDVD())
        
        print()

        finalizar = whileOutro("Deseja finalizar a compra?(Y/N) ")
        if finalizar:
            loading("Carregando", Texto.ciano())
            finalizarCompra()
        else:
            input("Pressione qualquer tecla para voltar ao Menu da Loja ")
            loading("Carregando", Texto.ciano())
            menuLoja()

def finalizarCompra():
    global carrinho

    totalCompra = 18.9

    titulo("FINALIZAR COMPRA", Texto.negrito())

    for item in carrinho:
        print(item.stringDVD())

    print(f"\nO total do aluguel é de {totalCompra}\n")
    print("Qual a forma de pagamento desejada?\n")
    while(True):

        print(f"{textoCor("1 - ", Texto.azul())}Pix\n")
        print(f"{textoCor("2 - ", Texto.azul())}Cartão de Crédito\n")
        print(f"{textoCor("3 - ", Texto.azul())}Cartão de Débito\n")
        print(f"{textoCor("4 - ", Texto.azul())}Boleto\n")

        opcao = input("Opção escolhida: ")

        if not(opcao.isdigit()):
            print(f"{textoCor("Opção inválida!\n", Texto.vermelho())}")
            continue
        
        opcao = int(opcao)

        if opcao <= 0 or opcao > 4:
            print(f"{textoCor("Opção inválida!\n", Texto.vermelho())}")
            continue

        break

    print(f"{textoCor("Pagamento feito com sucesso!\n", Texto.verde())}")
    print(f"{textoCor("Esperando confirmação do vendedor!", Texto.amarelo())}")

    carrinho = []

    input("Aperte qualquer tecla para continuar! ")
    loading("Carregando", Texto.ciano())
    menuLoja()



def alugueisConfirmacao():
    print("Seção de confirmação ainda não foi feita!")
    loading("Carregando", Texto.ciano())
    menuInformacoesUsuario()

def exibirInformacoesUsuario():
    titulo("Informações do Usuário", Texto.negrito())
    if tipoUsuario == TipoUsuario.CLIENTE:
        print(usuario.stringCliente())
    elif tipoUsuario == TipoUsuario.FUNCIONARIO:
        print(usuario.stringFuncionario())
    
    input("\nAperte qualquer tecla para continuar ")
    loading("Recarregando", Texto.ciano())
    menuInformacoesUsuario()


def exibirHistoricoFilmes():
    titulo("Histórico de Filmes Alugados", Texto.negrito())

    filmes = [Filme(1, "Revenge of The Sith", "2005-05-05", "Ficção", "Lucasfilm", "George Lucas", 10, 12),
              Filme(2, "Avengers Endgame", "2019-09-05", "Herói", "Marvel", "Joe Russo", 9, 8.7)]
    
    for filme in filmes:
        print(filme.stringFilme())

    print()

    input("Aperte qualquer tecla para continuar ")
    loading("Recarregando", Texto.ciano())
    menuInformacoesUsuario()


def sairConta():
    global tipoUsuario
    global usuario

    sair = whileOutro("Deseja sair da loja? (Y/N)")


    if sair:
        sairLoja()
    else:
        loading("Saindo da conta", Texto.verde())
    
    tipoUsuario = TipoUsuario.SEM_LOGIN
    usuario = None

    menuLoja()

def sairLoja():
    loading("Saindo", Texto.amarelo())
    sys.exit()




# ------------------------------------------------------------------------------------------------ #

#Por algum motivo, não consegui deixar isso num arquivo diferente. É o equivalente ao primeiro projeto
#Vai ficar por aqui até a gente conseguir resolver

ID = 'ID'
NOME = 'Nome'
DATA_LANCAMENTO = 'DataLancamento'
GENERO = 'Genero'
NOME_ESTUDIO = 'NomeEstudio'
NOME_DIRETOR = 'NomeDiretor'
QTD_ESTOQUE = 'qtdEstoque'
PRECO_ALUGUEL = 'precoAluguel'

daoFilme = DaoFactory.createFilmeDao()

def menuCadastro():
    """
    Menu Principal da aplicação
    Args:
        daoFilme: Objeto que implementa a interface FilmeDao
    """

    listaFuncoes = [menuInserir, menuAlterar, menuPesquisar, menuRemover, menuListar, menuExibir, menuRelatorio, menuSair]

    #Lista das funções que serão utilizadas. Todas elas tem assinatura parecidas para 
    #evitar o uso excessivo de ifs ou de switch cases

    #Looping principal do menu
    while(True):
        titulo("CADASTRO DE FILMES", Texto.negrito())
        cor = Texto.azul()
        print(textoCor("1 - ", cor) + "Inserir Filme\n")
        print(textoCor("2 - ", cor) + "Alterar Filme\n")
        print(textoCor("3 - ", cor) + "Pesquisar por Nome\n")
        print(textoCor("4 - ", cor) + "Remover Filme\n")
        print(textoCor("5 - ", cor) + "Listar todos os Filmes\n")
        print(textoCor("6 - ", cor) + "Exibir um filme\n")
        print(textoCor("7 - ", cor) + "Exibir Relatório\n")
        print(textoCor("8 - ", cor) + "Voltar para o Menu da Loja\n")

        try:
            opcao = int(input("Escolha uma opção: "))
        except ValueError: #Trata um input não numeral
            print(textoCor("Opcão Inválida!\n",Texto.vermelho()))
            loading("Recarregando", Texto.ciano())
            continue
        
        if opcao <= 0 or opcao > 8: #Trata um input fora das opções válidas
            print(textoCor("Opcão Inválida!\n",Texto.vermelho()))
            loading("Recarregando", Texto.ciano())
            continue

        listaFuncoes[opcao - 1]
        if opcao != 8:
            loading(f"Carregando", Texto.amarelo())
        sair = listaFuncoes[opcao - 1]() #A função sair retorna True quando chamado para fazer o controle do menu
        #O resto das funções retorna None

        if sair == True: #Fim do Programa
            break

    menuLoja()

    
            
#Função que controla as inserções de filmes           
def menuInserir():
    """
    Menu de inserção dos filmes
    Args:
        daoFilme: Objeto que implementa a interface FilmeDao
    """
    global daoFilme

    menuInserir = True
    while(menuInserir):
        titulo("INSERÇÃO DE FILMES", Texto.negrito())

        nomeFilme = checaEntrada("Nome do Filme a ser inserido: ", "Nome do Filme inválido!", lambda x: x == "")
        #Pega o Nome do Filme. Checa também se esse nome é válido (É inválido se for vazio, apenas)

       #Looping para pegar a Data de Lançamento 
        while(True):
            dataLancamento = input(f"\nData de lançamento (YY-mm-dd) do filme {nomeFilme}: ")
            ehData = checaSeData(dataLancamento)
            if not(ehData):
                print(textoCor(f"Formato de data inválido", Texto.vermelho()))
                continue
            break
        
        expressao = lambda x: x == "" or x.isdigit() # Checagem de entrada válida para gênero, Nome do Estúdio
        # e Nome do Diretor

        genero = checaEntrada(f"\nGênero do filme {nomeFilme}: ", "Gênero de Filme inválido!", expressao)

        nomeEstudio = checaEntrada(f"\nNome do Estúdio que produziu o filme {nomeFilme}: ", "Nome de Estúdio inválido!", expressao)

        nomeDiretor = checaEntrada(f"\nNome do Diretor do filme {nomeFilme}: ", "Nome de Diretor inválido!", expressao)

        while(True):
            try:
                qtdEstoque = int(input(f"\nQuantidade em estoque do filme {nomeFilme}: ")) #Pega a quantidade em estoque
            except ValueError: #Checa se é um número
                print(textoCor(f"Quantidade inválida\n", Texto.vermelho()))
                continue

            if qtdEstoque < 0: #Checa se a quantidade é inválida
                print(textoCor(f"Quantidade inválida\n", Texto.vermelho()))
                continue

            break

        while(True):
            try:
                precoAluguel = float(input(f"\nPreço do Aluguel do filme {nomeFilme}: "))
                precoAluguel = round(precoAluguel, 2)
            except ValueError:
                print(textoCor(f"Preço inválido\n", Texto.vermelho()))
                continue

            if precoAluguel <= 0: #Checa se o preço é inválido
                print(textoCor(f"Preço inválido\n", Texto.vermelho()))
                continue

            break

        #Cria um filme da classe filme a ser inserido. Como o ID é um atributo auto incremental,
        #O filme é, no front, iniciado com -1. No método inserir, o ID é apenas desconsiderado
        filme = Filme(-1, nomeFilme, dataLancamento, genero, nomeEstudio, nomeDiretor, qtdEstoque, precoAluguel)
        sucesso, idFilme = daoFilme.inserir(filme) #Inserção

        if sucesso: #Se foi possível inserir o filme
            print(textoCor("\nFilme inserido com sucesso!", Texto.verde()))
            print(f"\nO ID do filme {nomeFilme} é: {idFilme}")
        else: #Se a inserção foi impossível
            print(textoCor("O filme não pôde ser inserido no banco de dados!", Texto.vermelho()))

        menuInserir = whileOutro("Deseja inserir outro filme? (Y/N) ")

        if menuInserir:
            loading("Recarregando", Texto.ciano())

    loading("Saindo", Texto.amarelo())

#Função que controla as alterações de filmes
def menuAlterar():
    """
    Menu de alteração dos filmes
    Args:
        daoFilme: Objeto que implementa a interface FilmeDao
    """
    global daoFilme

    menuAlterar = True
    while(menuAlterar):
        titulo("ALTERAÇÃO DE FILMES", Texto.negrito())
        idFilme = input("ID do filme a ser alterado: ")

        filme = daoFilme.findById(idFilme) #Checa se o filme de ID existe. Se existe, pega os dados atuais
        if filme == None: #Se esse filme não existir, recarregar
            print(f"O filme de id {idFilme} não existe em nossos registros!")
            loading("Recarregando", Texto.ciano())
            continue

        contador = 0 #Contador para saber se o filme a ser alterado é realmente diferente do atual
        #Isso serve para uma operação inútil pelo banco de dados

        expressao = lambda x: x == "" or x.isdigit() #Cria a expressão de erro mais comum
        #Não é usada para a Data de Lançamento, o nome do filme, a quantidade de estoque e o preço do aluguel

        expressaoInt = lambda x: (not(x.isdigit()) or int(x) < 0)

        #Cria o filme da classe Filme
        filme = Filme(filme[0], filme[1], filme[2], filme[3], filme[4], filme[5], filme[6], filme[7])
        

        nomeFilme = whileAlterarYN(f"\nDeseja mudar o nome de {filme.nome}? (Y/N)", f"Novo nome do filme {filme.nome}: ", "Nome inválido!", lambda x: x == "")
        if nomeFilme == None: #Se o nome não foi alterado
            nomeFilme = filme.nome #O nome do filme do UPDATE será o mesmo de antes
            contador += 1 #Registrar que não houve mudança efetiva

        #Pega a nova data de lançamento
        dataLancamento = whileAlterarYN(f"\nDeseja mudar a data de lançamento de {nomeFilme}? (Y/N) ", f"Nova data de lançamento do filme {nomeFilme}: ", "Data de lançamento inválida!", lambda x: not checaSeData(x))

        if dataLancamento == None:
            dataLancamento = filme.dataLancamento
            contador += 1
        
        #Pega o novo gênero
        genero = whileAlterarYN(f"\nDeseja mudar o gênero de {nomeFilme}? (Y/N) ", f"Novo gênero do filme {nomeFilme}: ", "Gênero inválido!", expressao)

        if genero == None:
            genero = filme.genero
            contador += 1

        #Pega o novo nome do Estúdio
        nomeEstudio = whileAlterarYN(f"\nDeseja mudar o estúdio de {nomeFilme}? (Y/N) ", f"Nova estúdio do filme {nomeFilme}: ", "Nome de Estúdio inválido!", expressao)

        if nomeEstudio == None:
            nomeEstudio = filme.nomeEstudio
            contador += 1

        #Pega o novo nome do Diretor
        nomeDiretor = whileAlterarYN(f"\nDeseja mudar o diretor de {nomeFilme}? (Y/N) ", f"Novo diretor do filme {nomeFilme}: ", "Nome do Diretor inválido!", expressao)

        if nomeDiretor == None:
            nomeDiretor = filme.nomeDiretor
            contador += 1

        #Pega a nova quantidade em estoque
        qtdEstoque = whileAlterarYN(f"\nDeseja mudar a quantidade em estoque de {nomeFilme}? (Y/N) ", f"Nova quantidade de estoque do filme {nomeFilme}: ", "Quantidade de estoque inválida!", expressaoInt)

        if qtdEstoque == None:
            qtdEstoque = filme.qtdEstoque
            contador += 1

        #Pega o novo preço de aluguel
        precoAluguel = whileAlterarYN(f"\nDeseja mudar o preço do aluguel de {nomeFilme}? (Y/N) ", f"Novo preço do aluguel do filme {nomeFilme}: ", "Preço de Aluguel inválido!", expressaoInt)

        if precoAluguel == None:
            precoAluguel = filme.precoAluguel
            contador += 1

        #Se houve alguma alteração real no filme
        if contador < 7:
            filme = Filme(idFilme, nomeFilme, dataLancamento, genero, nomeEstudio, nomeDiretor, qtdEstoque, precoAluguel)

            sucesso = daoFilme.updateById(filme) #Atualiza o filme
            if sucesso: #Se atualização bem sucedida
                print(textoCor(f"\nFilme de id {idFilme} alterado com sucesso!", Texto.verde()))
            else:
                print(textoCor(f"Os dados do filme de id {idFilme} não poderam ser alterados!", Texto.vermelho()))

        menuAlterar = whileOutro("\nDeseja alterar outro filme? (Y/N) ")

        if menuAlterar:
            loading("Recarregando", Texto.ciano())
    
    loading("Saindo", Texto.amarelo())

#Função que controla as pesquisas de filmes
def menuPesquisar():
    """
    Menu de Pesquisa de filmes
    Args:
        daoFilme: Objeto que implementa a interface FilmeDao
    """
    global daoFilme
    
    menuPesquisar = True
    while(menuPesquisar):
        titulo("PESQUISA DE FILMES", Texto.negrito())

        nomeFilme = input("Nome do filme que desejas pesquisar: ")
        filmes = daoFilme.findByName(nomeFilme) #Tenta achar o filme pelo nome

        if filmes.empty: #Se não há filmes com esse padrão de nome
            print(textoCor("Não há nenhum filme cadastrado com esse nome!", Texto.vermelho()))
            loading("Recarregando", Texto.ciano())
            continue

        print("\n")
    
        for index, row in filmes.iterrows():
            filme = Filme(row[ID], row[NOME], row[DATA_LANCAMENTO], row[GENERO], row[NOME_ESTUDIO], row[NOME_DIRETOR], row[QTD_ESTOQUE], row[PRECO_ALUGUEL])
            print(filme.stringFilme(), end="\n\n")

        menuPesquisar = whileOutro("\nDeseja pesquisar outro filme? (Y/N) ")
        if menuPesquisar:
            loading("Recarregando", Texto.ciano())
            
    loading("Saindo", Texto.amarelo())

#Função que controla as remoções de filmes
def menuRemover():
    """
    Menu de remoção dos Filmes
    Args:
        daoFilme: Objeto que implementa a interface FilmeDao
    """
    global daoFilme

    menuRemover = True
    while(menuRemover):
        titulo("REMOÇÃO DE FILMES", Texto.negrito())
        # idFilme = input()
        idFilme = checaEntrada("ID do filme que desejas remover: ", "ID de filme Inválido!", lambda x: not(x.isdigit()))
        filme = daoFilme.findById(idFilme)
        if filme == None:
            print(textoCor("Não há nenhum filme cadastrado com esse ID!", Texto.vermelho()))
            loading("Recarregando", Texto.ciano())
            continue

        sucesso = daoFilme.deleteById(idFilme) #Tenta deletar o filme 
        
        if sucesso: #Se foi possível deletar esse filme
            print(textoCor(f"O filme {filme[1]} foi removido com sucesso", Texto.verde()))
        else: #Se não foi possível deletar esse filme
            print(textoCor(f"O filme {filme[1]} não pôde ser removido!", Texto.vermelho()))

        menuRemover = whileOutro("Deseja remover outro filme? (Y/N) ")
    
        if menuRemover:
            loading("Recarregando", Texto.ciano())

    loading("Saindo", Texto.amarelo())

#Função que controla a listagem de filmes
def menuListar():
    """
    Menu de listagem dos Filmes
    Args:
        daoFilme: Objeto que implementa a interface FilmeDao
    """
    global daoFilme

    titulo("LISTAGEM DE FILMES", Texto.negrito())
    print("Filmes cadastrados:")

    filmes = daoFilme.findAll() #Pega todos os filmes do banco de dados

    if filmes.empty : #
        print(textoCor("Não há nenhum filme cadastrado!\n\n", Texto.vermelho()))
    else:
        for index, row in filmes.iterrows():
            filme = Filme(row[ID], row[NOME], row[DATA_LANCAMENTO], row[GENERO], row[NOME_ESTUDIO], row[NOME_DIRETOR], row[QTD_ESTOQUE], row[PRECO_ALUGUEL])
            print(filme.stringFilme(), end="\n\n")


    input("Digite qualquer tecla para voltar ao menu")
    loading("Saindo", Texto.amarelo())

#Função que controla a exibição de filmes
def menuExibir():
    """
    Menu de exibição dos Filmes
    Args:
        daoFilme: Objeto que implementa a interface FilmeDao
    """
    global daoFilme

    menuExibir = True

    while(menuExibir):
        titulo("EXIBIÇÃO DE FILME", Texto.negrito())
        idFilme = input("ID do filme que desejas exibir: ") #ID do filme a ser exibido
        filme = daoFilme.findById(idFilme) #Tenta achar o filme

        if filme == None: #Se não conseguiu achar
            print(textoCor("Não há nenhum filme cadastrado com esse ID!", Texto.vermelho()))
        else:
            filme = Filme(filme[0], filme[1], filme[2], filme[3], filme[4], filme[5], filme[6], filme[7])
            print(filme.stringFilme())

        print("\n")
        menuExibir = whileOutro("Deseja exibir outro filme? (Y/N) ")

        if menuExibir:
            loading("Recarregando", Texto.ciano())

    loading("Saindo", Texto.amarelo())

#Função que controla a exibição do relatório de informações
def menuRelatorio():
    """
    Menu que exibe o relatório do Banco de Daos
    Args:
        daoFilme: Objeto que implementa a interface FilmeDao
    """
    global daoFilme

    titulo("RELATÓRIO DE INFORMAÇÕES", Texto.negrito())

    filmesCadastrados = daoFilme.countInstances() #Pega a quantidade de linhas da tabela
    precoTotalAluguel = daoFilme.sumPrecoAluguel() #Pega a soma dos preços de aluguel
    qtdEstoqueTotal = daoFilme.sumQtdEstoque() #Pega a soma da quantidade de filmes em estoque

    print(f"Filmes Cadastrados no Sistema: {filmesCadastrados}")
    print(f"Preço total de aluguel dos filmes cadastrados: {precoTotalAluguel}")
    print(f"Quantidade total de filmes em Estoque: {qtdEstoqueTotal}\n")

    input("Digite qualquer tecla para voltar ao menu")
    loading("Saindo", Texto.amarelo())

#Função que controla a saída do menu
def menuSair():
    
    """
    Menu de saída dos Filmes
    Args:
        daoFilme: Objeto que implementa a interface FilmeDao
    Returns:
        Boolean: Indica que o programa deve ser finalizado. Retorna True quando o programa
        deve ser encerrado
    """
    
    loading("Saindo", Texto.amarelo())
    return True






