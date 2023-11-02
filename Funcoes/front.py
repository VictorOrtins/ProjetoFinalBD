from enum import Enum

from Funcoes.funcoesAuxiliares import *

from DAO.ManipulaDAOs import *
from DAO.DaoFactory import *


from Entidades.cliente import *
from Entidades.funcionario import *
from Entidades.filme import *
from Entidades.dvd import *

from Funcoes.frontCadastro import menuCadastro


class TipoUsuario(Enum):
    CLIENTE = 1
    FUNCIONARIO = 2
    SEM_LOGIN = 3

manipulaDaos = ManipulaDAOs(DaoFactory())

tipoUsuario = TipoUsuario.SEM_LOGIN
usuario = None

carrinho = [DVD(1, 6, "Avengers Endgame"), DVD(2, 5, "Barbie")]


def iniciar():
    os.system('cls')
    login()

def login():
    listaFuncoes = [loginCliente, loginFuncionario, menuLoja, cadastroUsuario, cadastroFuncionario, sairLoja]
    while(True):
        titulo("ESCOLHA DE LOGIN", Texto.negrito())

        print(f"{textoCor("1 - ", Texto.azul())}Login Cliente\n")
        print(f"{textoCor("2 - ", Texto.azul())}Login Funcionário\n")
        print(f"{textoCor("3 - ", Texto.azul())}Entrar sem Login\n")
        print(f"{textoCor("4 - ", Texto.azul())}Cadastrar Usuário\n")
        print(f"{textoCor("5 - ", Texto.azul())}Cadastrar Funcionário\n")
        print(f"{textoCor("6 - ", Texto.azul())}Sair da loja\n")

        try:
            opcao = int(input("Escolha uma opção: "))
        except ValueError: #Trata um input não numeral
            print(textoCor("Opcão Inválida!\n",Texto.vermelho()))
            loading("Recarregando", Texto.ciano())
            continue
            
        if opcao <= 0 or opcao > 6: #Trata um input fora das opções válidas
            print(textoCor("Opcão Inválida!\n",Texto.vermelho()))
            loading("Recarregando", Texto.ciano())
            continue

        break

    if opcao != 6:
        loading("Carregando", Texto.amarelo())
    listaFuncoes[opcao - 1]()


def loginCliente():
    global tipoUsuario
    global usuario

    titulo("LOGIN CLIENTE", Texto.negrito())

    while(True):
        naoEncontrado = False

        login = checaEntrada("Login: ", "", lambda x: False)
        senha = checaEntrada("Senha: ", "", lambda x: False)

        cliente = manipulaDaos.daoCliente.findByLogin(login)

        if cliente == None:
            print(textoCor("Usuário não encontrado!", Texto.vermelho()))
            naoEncontrado = True

        if cliente[6] != senha:
            print(textoCor("Senha Incorreta!", Texto.vermelho()))
            naoEncontrado = True

        
        if naoEncontrado:
            continuar = whileOutro("Deseja continuar sem login? (Y/N)")
            if continuar:
                break
            loading("Recarregando", Texto.amarelo())
            continue

        cliente = Cliente(cliente[0], cliente[1], cliente[2], cliente[3], cliente[4], cliente[5], cliente[6], cliente[7], cliente[8])

        

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
    if (menuCadastro()):
        menuLoja()

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

def cadastroUsuario():
    print("Cadastro de Usuário ainda não foi implementado!")
    loading("Recarregando", Texto.vermelho())
    login()

def cadastroFuncionario():
    print("Cadastro de Funcionário ainda não foi implementado!")
    loading("Recarregando", Texto.vermelho())
    login()

