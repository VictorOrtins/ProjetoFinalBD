from enum import Enum

from Funcoes.funcoesAuxiliares import *

from DAO.ManipulaDAOs import *
from DAO.DaoFactory import *


from Entidades.cliente import *
from Entidades.funcionario import *
from Entidades.filme import *
from Entidades.dvd import *
from Entidades.filmeCarrinho import *

from Funcoes.frontCadastroEstoque import menuCadastro

import time
from decimal import Decimal


class TipoUsuario(Enum):
    VENDEDOR = 2
    SEM_LOGIN = 3
    GERENTE = 4

manipulaDaos = ManipulaDAOs(DaoFactory())

tipoUsuario = TipoUsuario.SEM_LOGIN
usuario = None

carrinho = []


def iniciar():
    """
    Função que chama o menu de início do programa
    """
    os.system('cls')
    menuIniciar()

def menuIniciar():
    """
    Função que serve como o menu de tentativa de login, cadastro ou entrada no sistema sem login
    """
    listaFuncoes = [loginFuncionario, menuSistema, sairLoja] #Lista de funções que são chamadas após a escolha do usuário
    while(True):
        titulo("ESCOLHA DE LOGIN", Texto.negrito())

        print(f"{textoCor("1 - ", Texto.azul())}Fazer Login\n")
        print(f"{textoCor("2 - ", Texto.azul())}Entrar sem Login\n")
        print(f"{textoCor("3 - ", Texto.azul())}Sair da loja\n")

        try:
            opcao = int(input("Escolha uma opção: "))
        except ValueError: #Trata um input não numeral
            print(textoCor("Opcão Inválida!\n",Texto.vermelho()))
            loading("Recarregando", Texto.ciano())
            continue
            
        if opcao <= 0 or opcao > len(listaFuncoes): #Trata um input fora das opções válidas
            print(textoCor("Opcão Inválida!\n",Texto.vermelho()))
            loading("Recarregando", Texto.ciano())
            continue

        break

    if opcao != 4: #Se a opção não for a de sair (Sair possui um loading próprio)
        loading("Carregando", Texto.amarelo())
    
    listaFuncoes[opcao - 1]() #Chama a função correspondente a opção que o usuário digitou


def loginFuncionario():
    """
    Função que faz o login do funcionário
    """

    global tipoUsuario #Se o login for bem sucedido, o tipo do usuário será atualizado
    global usuario #Se o login for bem sucedido, o usuário será atualizado
    global manipulaDaos #Variável que manipula os daos

    while(True):
        naoEncontrado = False #É assumido primeiramente que o usuário será encontrado

        titulo("LOGIN FUNCIONÁRIO", Texto.negrito())
        login = checaEntrada("Login: ", "", lambda x: False) #Checa se o login é válido
        senha = checaEntrada("Senha: ", "", lambda x: False) #Checa se a senha é válida
        
        funcionario = manipulaDaos.daoFuncionario.findSenhaByLogin(login) #Tenta achar o funcionário a partir do login

        if funcionario.empty: #Se o usuário não for encontrado
            print(textoCor("Usuário não encontrado!", Texto.vermelho()))
            naoEncontrado = True
        elif funcionario.iloc[0,1] != senha: #Se a senha for inválida
            print(textoCor("Senha inválida!\n", Texto.vermelho()))
            naoEncontrado = True

        if naoEncontrado: #Se o usuário não foi encontrado ou a senha é inválida
            continuar = whileOutro("Deseja continuar sem login? (Y/N)") #Pergunta se quer continuar sem login
            if continuar: #Se quiser, tenta ir pra loja
                break

            loading("Recarregando", Texto.amarelo())
            continue

        funcionario = manipulaDaos.daoFuncionario.findByLogin(login)
        #Cria o objeto do funcionário   
        funcionario = Funcionario(funcionario.iloc[0,0], funcionario.iloc[0,1], funcionario.iloc[0,2], funcionario.iloc[0,3], funcionario.iloc[0,4], funcionario.iloc[0,5])

        break
    
    if not(naoEncontrado): #Se o login foi bem sucedido
        print(textoCor("\nLogin de Funcionário bem-sucedido!", Texto.verde()))

        if funcionario.tipoFuncionario == "Vendedor":
            tipoUsuario = TipoUsuario.VENDEDOR #Muda o tipo do usuário
        elif funcionario.tipoFuncionario == "Gerente":
            tipoUsuario = TipoUsuario.GERENTE
        
        usuario = funcionario #Atualiza o usuário para o funcionário

    loading("Carregando", Texto.amarelo())
    menuSistema() #Sempre redireciona para o menu da loja

def menuSistema():
    """
    Função que representa o menu principal da loja. 
    Esse menu muda de visualização a partir do tipo do usuário que está logando no sistema
    """

    if tipoUsuario == TipoUsuario.VENDEDOR: #Se for um funcionário
        listaFuncoes = [menuInformacoesUsuario, menuAluguelDeFilmes, menuCadastroEstoque, confirmarDevolucao, sairLoja] #Define as funções
        #Texto que será exibido para o usuário digitar a opção que ele quer
        #Ele vai conter o nome do funcionário, pode redirecionar para o menu de informações de usuário,
        #O menu de cadastro de estoque e para a função que sai do sistema

        txtInput = "".join([f"{textoCor("Vendedor: ", Texto.magenta())}{usuario.primeiroNome} {usuario.ultimoNome}\n\n",f"{textoCor("1 - ", Texto.azul())}Informações do Usuário\n\n",
        f"{textoCor("2 - ", Texto.azul())}Registrar Venda\n\n",f"{textoCor("3 - ", Texto.azul())}Cadastro de Estoque\n\n", f"{textoCor("4 - ", Texto.azul())}Devolução de Filmes\n\n", f"{textoCor("5 - ", Texto.azul())}Sair da Loja\n"])

    elif tipoUsuario == TipoUsuario.SEM_LOGIN: #Se não tiver feito login. A visualização dele é mais parecida com a do cliente
        listaFuncoes = [pesquisarNome, pesquisarPreco, pesquisarGenero, pesquisarFilmeAtor, pesquisarFilmeNacionalidade, pesquisarFilmeDiretor, loginFuncionario, sairLoja] #Lista de funções
        #Basicamente a mesma coisa do cliente, porém tem a opção de fazer o login e não se pode ver as informações
        #do usuário
        txtInput = "".join([
        f"{textoCor("1 - ", Texto.azul())}Pesquisar por Nome\n\n",f"{textoCor("2 - ", Texto.azul())}Pesquisar por Preço\n\n", f"{textoCor("3 - ", Texto.azul())}Pesquisar por Gênero\n\n",
        f"{textoCor("4 - ", Texto.azul())}Pesquisar Filme com Ator X\n\n", f"{textoCor("5 - ", Texto.azul())}Pesquisar Filme com Ator de Nacionalidade X\n\n", f"{textoCor("6 - ", Texto.azul())}Pesquisar Filme do Diretor X\n\n",
        f"{textoCor("7 - ", Texto.azul())}Fazer Login\n\n", f"{textoCor("8 - ", Texto.azul())}Sair\n\n"])

    elif tipoUsuario == TipoUsuario.GERENTE:
        listaFuncoes = [menuInformacoesUsuario, menuAluguelDeFilmes, menuCadastroEstoque, menuCadastroFuncionario, confirmarDevolucao, sairLoja] #Define as funções

        #Mesma coisa do vendedor porém com a opção de cadastrar vendedores
        txtInput = "".join([f"{textoCor("Gerente: ", Texto.verde())}{usuario.primeiroNome} {usuario.ultimoNome}\n\n",f"{textoCor("1 - ", Texto.azul())}Informações do Usuário\n\n",
        f"{textoCor("2 - ", Texto.azul())}Registrar Venda\n\n",f"{textoCor("3 - ", Texto.azul())}Cadastro de Estoque\n\n", f"{textoCor("4 - ", Texto.azul())}Cadastro de Vendedores\n\n", f"{textoCor("5 - ", Texto.azul())}Devolução de Filmes\n\n", f"{textoCor("6 - ", Texto.azul())}Sair da Loja\n"])

    while(True):
        #Loop do menu da loja
        titulo("MENU DA LOJA", Texto.negrito())

        print(txtInput)

        try:
            opcao = int(input("Escolha uma opção: "))
        except ValueError: #Trata um input não numeral
            print(textoCor("Opcão Inválida!\n",Texto.vermelho()))
            loading("Recarregando", Texto.ciano())
            continue
        
        
        if opcao <= 0 or opcao > len(listaFuncoes): #Trata um input fora das opções válidas
            print(textoCor("Opcão Inválida!\n",Texto.vermelho()))
            loading("Recarregando", Texto.ciano())
            continue
        break

    if opcao != len(listaFuncoes):
        loading("Carregando", Texto.amarelo())

    if tipoUsuario == TipoUsuario.SEM_LOGIN:
        if opcao <= 6:
            listaFuncoes[opcao - 1](False)
        else:
            listaFuncoes[opcao - 1]()
    else:
        listaFuncoes[opcao - 1]()

def menuCadastroFuncionario():
    listaFuncoes = [cadastroFuncionario, demitirVendedor, mostrarFuncionarios, menuSistema]
    while(True):
        titulo("MENU DO CADASTRO FUNCIONÁRIO", Texto.negrito())

        print(f"{textoCor("1 - ", Texto.azul())}Cadastro de Funcionário\n")
        print(f"{textoCor("2 - ", Texto.azul())}Demitir Funcionário\n")
        print(f"{textoCor("3 - ", Texto.azul())}Mostrar Todos os Funcionários\n")
        print(f"{textoCor("4 - ", Texto.azul())}Voltar para Loja\n")

        try:
            opcao = int(input("Escolha uma opção: "))
        except ValueError: #Trata um input não numeral
            print(textoCor("Opcão Inválida!\n",Texto.vermelho()))
            loading("Recarregando", Texto.ciano())
            continue
        
        
        if opcao <= 0 or opcao > len(listaFuncoes): #Trata um input fora das opções válidas
            print(textoCor("Opcão Inválida!\n",Texto.vermelho()))
            loading("Recarregando", Texto.ciano())
            continue

        break

    loading("Carregando", Texto.amarelo())
    listaFuncoes[opcao - 1]() #Chamar a função da lista de funções

def menuInformacoesUsuario():
    """
    Menu que redireciona para as informações do usuário
    """

    global tipoUsuario #É preciso chegar o tipo de usuário
    global usuario #E mostrar informações do usuário

    listaFuncoes = [exibirInformacoesUsuario, historicoAlugueis, menuSistema, sairConta] #Funções que podem ser chamadas

    #Pergunta se o funcioário quer ver as informações do funcionário, os aluguéis pendentes de confirmação,
    #Se quer voltar ao menu da loja ou sair da conta

    if tipoUsuario == TipoUsuario.GERENTE:
        textoNome = textoCor("Gerente: ", Texto.verde())
        textoNome2 = "Gerente"
    elif tipoUsuario == TipoUsuario.VENDEDOR:
        textoNome = textoCor("Vendedor: ", Texto.magenta())
        textoNome2 = "Vendedor"
    
    txtInput = "".join([f"{textoNome}{usuario.primeiroNome} {usuario.ultimoNome}\n\n",f"{textoCor("1 - ", Texto.azul())}Exibir Informações do {textoNome2}\n\n",
    f"{textoCor("2 - ", Texto.azul())}Histórico de Aluguéis\n\n",
    f"{textoCor("3 - ", Texto.azul())}Voltar para o Menu\n\n", f"{textoCor("4 - ", Texto.azul())}Sair da Conta\n\n"])

    while(True):

        titulo("MENU DO USUÁRIO", Texto.negrito())

        print(txtInput)

        try:
            opcao = int(input("Escolha uma opção: "))
        except ValueError: #Trata um input não numeral
            print(textoCor("Opcão Inválida!\n",Texto.vermelho()))
            loading("Recarregando", Texto.ciano())
            continue
        
        
        if opcao <= 0 or opcao > len(listaFuncoes): #Trata um input fora das opções válidas
            print(textoCor("Opcão Inválida!\n",Texto.vermelho()))
            loading("Recarregando", Texto.ciano())
            continue

        break

    if opcao != len(listaFuncoes): #Se o usuário não escolher sair
        loading("Carregando", Texto.amarelo())
    
    listaFuncoes[opcao - 1]() #Chamar a função da lista de funções

def menuAluguelDeFilmes():
    """
    Menu de aluguel de filmes
    Ainda não está com o SQL!
    """
    global tipoUsuario #É preciso checar o tipo do usuário
    global usuario #É preciso pegar informações do usuário

    if tipoUsuario == TipoUsuario.GERENTE:
        txtTipo = "Funcionário: "
    else:
        txtTipo = "Vendedor: "
    
    listaFuncoes = [pesquisarNome, pesquisarPreco, pesquisarGenero, pesquisarFilmeAtor, pesquisarFilmeNacionalidade, pesquisarFilmeDiretor, verCarrinho, menuSistema] #Funções
    txtInput = "".join([f"{textoCor(f"{txtTipo}", Texto.verde())}{usuario.primeiroNome} {usuario.ultimoNome}\n\n",f"{textoCor("1 - ", Texto.azul())}Pesquisar por Nome\n\n",
    f"{textoCor("2 - ", Texto.azul())}Pesquisar por Preço\n\n", f"{textoCor("3 - ", Texto.azul())}Pesquisar por Gênero\n\n",
    f"{textoCor("4 - ", Texto.azul())}Pesquisar por Filmes do Ator X\n\n", f"{textoCor("5 - ", Texto.azul())}Pesquisar por Filmes do Ator de Nacionalidade X\n\n",
    f"{textoCor("6 - ", Texto.azul())}Pesquisar por Filmes do Diretor X\n\n",f"{textoCor("7 - ", Texto.azul())}Ver Carrinho\n\n" ,f"{textoCor("8 - ", Texto.azul())}Voltar para o menu da loja\n\n"])
    #O funcionário não pode ir para o menu de aluguel de filmes, para que não tenha chance dele poder alugar um filme

    while(True):

        titulo("ALUGUEL DE FILMES", Texto.negrito())

        print(txtInput)

        try:
            opcao = int(input("Escolha uma opção: "))
        except ValueError: #Trata um input não numeral
            print(textoCor("Opcão Inválida!\n",Texto.vermelho()))
            loading("Recarregando", Texto.ciano())
            continue
        
        
        if opcao <= 0 or opcao > len(listaFuncoes): #Trata um input fora das opções válidas
            print(textoCor("Opcão Inválida!\n",Texto.vermelho()))
            loading("Recarregando", Texto.ciano())
            continue

        break

    loading("Carregando", Texto.amarelo())
    
    if opcao <= 6:
        listaFuncoes[opcao - 1](True)
    else:
        listaFuncoes[opcao - 1]()


def pesquisarGeral(podeAddCarrinho, txtPesquisa, txtInput, txtErroVazio, dao):
    global carrinho #Essa função mexe com o carrinho, que está de alguma forma implementado

    titulo(txtPesquisa, Texto.negrito())

    nomeFilme = input(txtInput) #Pega o input

    resultado = dao(nomeFilme)

    if resultado.empty:
        print(textoCor(txtErroVazio, Texto.vermelho()))
        loading("Carregando", Texto.amarelo())
        if podeAddCarrinho:
            menuAluguelDeFilmes()
        else:
            menuSistema()
    else:
        for _, row in resultado.iterrows(): #Mostra os filmes
            filme = Filme(row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4], row.iloc[5], row.iloc[6], row.iloc[7])
            print(filme.stringFilme(), "\n")

        if podeAddCarrinho:
            adicionar = whileOutro("Deseja adicionar um desses filmes no carrinho? (Y/N)")
    
            if adicionar:
                idFilme = checaEntrada("\n\nDigite o ID do filme que deseja adicionar no carrinho: ", "ID Inválido", lambda x: not(x.isdigit()))

                idValido = False
                for _, row in resultado.iterrows():
                    if int(row.iloc[0]) == int(idFilme):
                        idValido = True
                
                if idValido:
                    qtdFilme = int(checaEntrada(f"\n\nDigite a quantidade do filme de ID {idFilme} que deseja adicionar: ", "Quantidade inválida!", lambda x: not(x.isdigit())))

                    podeContinuar = True

                    for _,row in resultado.iterrows():
                        if int(row.iloc[0]) == int(idFilme):
                            for item in carrinho:
                                if item.id == int(row.iloc[0]):
                                    if int(qtdFilme + item.qtdSelecionada) > int(row.iloc[6]):
                                        print(f"{textoCor("Quantidade selecionada inválida! O adicional de DVDs não será colocado no carrinho!", Texto.vermelho())}")
                                        time.sleep(0.5)
                                        podeContinuar = False
                                        break
                                    
                                    item.qtdSelecionada += qtdFilme
                                    podeContinuar = False
                                    print(f"{textoCor(f"Foram adicionados {qtdFilme} unidades de {row.iloc[1]} no carrinho!", Texto.verde())}")
                                    time.sleep(0.5)
                                    break
                            
                            if podeContinuar:
                                if int(qtdFilme) > int(row.iloc[6]):
                                        print(f"{textoCor("Quantidade selecionada inválida! O filme não será colocado no carrinho!", Texto.vermelho())}")
                                        time.sleep(0.5)
                                        break

                                carrinho.append(FilmeCarrinho(row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4], row.iloc[5], qtdFilme, row.iloc[7]))
                                print(f"{textoCor(f"Foram adicionados {qtdFilme} unidades de {row.iloc[1]} no carrinho!", Texto.verde())}")
                                time.sleep(0.5)
                                break
                    
                    loading("Carregando", Texto.amarelo())
                    menuAluguelDeFilmes()
                else:
                    print(f"{textoCor("ID de Filme inválido para a adição no carrinho!", Texto.vermelho())}")
                    time.sleep(0.5)
                    loading("Carregando", Texto.amarelo())
                    menuAluguelDeFilmes()
            else:
                loading("Carregando", Texto.amarelo())
                menuAluguelDeFilmes()
        else:
            input("Pressione qualquer tecla para continuar ")
            loading("Carregando", Texto.amarelo())
            menuSistema()

def pesquisarNome(podeAddCarrinho):
    """
    Pesquisa um filme pelo nome e tenta adicionar no carrinho
    """
    pesquisarGeral(podeAddCarrinho, "Pesquisa por Nome", "Nome do Filme que você deseja pesquisar: ", "Não há filmes com esse nome!", manipulaDaos.daoFilme.findByName)

            

def pesquisarPreco(podeAddCarrinho):
    """
    Pesquisa um filme pelo range de preço. A ideia era deixar o usuário digitar um range de preço
    Que seria convertido numa expressão booleana. Mas não sei se vai dar
    Não está com SQL!
    """
    global carrinho #Essa função mexe com o carrinho, que está de alguma forma implementado

    titulo("Pesquisa por Preço", Texto.negrito())

    input(f"{textoCor("Indique a faixa de Range de preço que você quer procurar o filme\n", Texto.amarelo())}Ela será no formato 'Preço entre X e Y\nPrimeiro perguntarei o X e depois o Y\nDigite qualquer tecla para continuar': ")

    range1 = checaEntrada("\nDigite o X na expressão 'Preço entre X e Y': ", "Número inválido", lambda x: not(x.isdigit()))
    range2 = checaEntrada(f"Digite o Y na expressão 'Preço entre {range1} e Y': ", "Número inválido", lambda x: not(x.isdigit()))
                            
    resultado = manipulaDaos.daoFilme.findByRangePrice(range1, range2) #Tenta achar o filme pelo nome

    if resultado.empty:
        print(textoCor("Não há filmes nessa faixa de preço!", Texto.vermelho()))
        loading("Carregando", Texto.amarelo())
        if podeAddCarrinho:
            menuAluguelDeFilmes()
        else:
            menuSistema()
    else:
        for _, row in resultado.iterrows(): #Mostra os filmes
            filme = Filme(row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4], row.iloc[5], row.iloc[6], row.iloc[7])
            print(filme.stringFilme())

        if podeAddCarrinho:
            adicionar = whileOutro("Deseja adicionar um desses filmes no carrinho? (Y/N)")
    
            if adicionar:
                idFilme = checaEntrada("Digite o ID do filme que deseja adicionar no carrinho: ", "ID Inválido", lambda x: not(x.isdigit()))

                idValido = False
                for _, row in resultado.iterrows():
                    if int(row.iloc[0]) == int(idFilme):
                        idValido = True
                
                if idValido:
                    qtdFilme = int(checaEntrada(f"Digite a quantidade do filme de ID {idFilme} que deseja adicionar: ", "Quantidade inválida!", lambda x: not(x.isdigit())))

                    podeContinuar = True

                    for _,row in resultado.iterrows():
                        if int(row.iloc[0]) == int(idFilme):
                            for item in carrinho:
                                if item.id == int(row.iloc[0]):
                                    if int(qtdFilme + item.qtdSelecionada) > int(row.iloc[6]):
                                        print(f"{textoCor("Quantidade selecionada inválida! O adicional de DVDs não será colocado no carrinho!", Texto.vermelho())}")
                                        time.sleep(0.5)
                                        podeContinuar = False
                                        break
                                    
                                    item.qtdSelecionada += qtdFilme
                                    podeContinuar = False
                                    print(f"{textoCor(f"Foram adicionados {qtdFilme} unidades de {row.iloc[1]} no carrinho!", Texto.verde())}")
                                    time.sleep(0.5)
                                    break
                            
                            if podeContinuar:
                                if int(qtdFilme) > int(row.iloc[6]):
                                        print(f"{textoCor("Quantidade selecionada inválida! O filme não será colocado no carrinho!", Texto.vermelho())}")
                                        time.sleep(0.5)
                                        break

                                carrinho.append(FilmeCarrinho(row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4], row.iloc[5], qtdFilme, row.iloc[7]))
                                print(f"{textoCor(f"Foram adicionados {qtdFilme} unidades de {row.iloc[1]} no carrinho!", Texto.verde())}")
                                time.sleep(0.5)
                                break
                    loading("Carregando", Texto.amarelo())
                    menuAluguelDeFilmes()
                else:
                    print(f"{textoCor("ID de Filme inválido para a adição no carrinho!", Texto.vermelho())}")
                    time.sleep(0.5)
                    loading("Carregando", Texto.amarelo())
                    menuAluguelDeFilmes()
            else:
                loading("Carregando", Texto.amarelo())
                menuAluguelDeFilmes()
        else:
            input("Pressione qualquer tecla para continuar ")
            loading("Carregando", Texto.amarelo())
            menuSistema()

def pesquisarGenero(podeAddCarrinho):
    """
    Pesquisa um filme pelo seu gênero
    Não está com o SQL!
    """
    pesquisarGeral(podeAddCarrinho, "Pesquisa por Gênero", "Gênero do Filme que você deseja pesquisar: ", "Não há filmes desse gênero!", manipulaDaos.daoFilme.findByGenre)

def pesquisarFilmeAtor(podeAddCarrinho):
    pesquisarGeral(podeAddCarrinho, "Pesquisa por Filmes com o Ator X", "Pesquise filmes em que aparecem o ator: ", "Não há filmes com esse ator no nosso sistema!",  manipulaDaos.daoElenco.getFilmeByAtor)


def pesquisarFilmeNacionalidade(podeAddCarrinho):
    pesquisarGeral(podeAddCarrinho, "Pesquise filmes em que aparecem Atores do País X: ", "Pesquise filmes em que aparecem Atores do País: ", "Não há filmes com atores dessa nacionalidade no nosso sistema!", manipulaDaos.daoElenco.getFilmeByNacionalidade)


def pesquisarFilmeDiretor(podeAddCarrinho):
    pesquisarGeral(podeAddCarrinho, "Pesquisa Filme por Diretor", "Pesquise filmes do Diretor: ", "Não há filmes desse diretor no nosso sistema!", manipulaDaos.daoFilme.findByDirector)


def menuCadastroEstoque():
    """
    Função que redireciona para o menu de cadastro de estoque de filmes
    Para poder utilizar a função funcionalmente, precisei mudar um pouco o cadastro
    Se ele retornou do cadastro, vai direto para 
    """
    global manipulaDaos
    if (menuCadastro(manipulaDaos)):
        menuSistema()

def voltarMenuLoja():
    """
    Função que redireciona para o menu da loja
    """
    loading("Carregando", Texto.amarelo())
    menuSistema()

def verCarrinho():
    """
    Função que vê o carrinho
    Não possui o SQL!
    """
    global carrinho

    titulo("CARRINHO", Texto.negrito())

    if carrinho == []:
        print("O carrinho está vazio!\n")
        loading("Carregando", Texto.amarelo())
        menuAluguelDeFilmes()
    else:
        for item in carrinho:
            print(item.stringFilmeCarrinho())
        
        print()

        finalizar = whileOutro("Deseja finalizar a compra?(Y/N) ")
        if finalizar:
            loading("Carregando", Texto.amarelo())
            finalizarCompra()
        else:
            retirar = whileOutro("Deseja retirar algum filme do Carrinho? (Y/N)")
            if retirar:
                id = int(checaEntrada("Digite o ID do Filme no Carrinho que deseja retirar: ", "ID inválido!", lambda x: not(x.isdigit())))
                idCorreto = False
                for item in carrinho:
                    if item.id == id:
                        idCorreto = True
                
                if idCorreto:
                    while(True):
                        qtd = int(checaEntrada(f"Digite a quantidade do filme de ID {id} que deseja remover: ", "Quantidade inválida", lambda x: not(x.isdigit())))
                        if qtd < 0:
                            print(f"{textoCor("Quantidade Inválida!", Texto.vermelho())}")
                            continue
                        break

                    for i in range(len(carrinho)):
                        if carrinho[i].id == id:
                            index = i
                            break

                    if qtd > carrinho[index].qtdSelecionada:
                        print(textoCor("Quantidade inválida! Voltando ao Menu!", Texto.vermelho()))
                        loading("Carregando", Texto.amarelo())
                        menuAluguelDeFilmes()
                    else:
                        carrinho[index].qtdSelecionada -= qtd
                        print(textoCor("Remoção feita com sucesso!", Texto.verde()))
                        if carrinho[index].qtdSelecionada == 0:
                            carrinho.pop(index)
                        loading("Carregando", Texto.amarelo())
                        menuAluguelDeFilmes()

                else:
                    print(textoCor("ID de Filme Inválido! Voltando ao Menu!", Texto.vermelho()))
                    loading("Carregando", Texto.amarelo())
                    menuAluguelDeFilmes()
            else:
                loading("Carregando", Texto.amarelo())
                menuAluguelDeFilmes()

def finalizarCompra():
    """
    Função que finaliza a compra
    """
    global carrinho


    titulo("FINALIZAR COMPRA", Texto.negrito())

    for item in carrinho:
        print(item.stringFilmeCarrinho())

    cpf = checaEntrada("Digite o CPF do Cliente que está fazendo a compra que está no carrinho: ", "CPF inválido", lambda x: not(checaSeCPF(x)))

    resultado = manipulaDaos.daoCliente.findByCPF(cpf)

    if resultado.empty:
        cadastrar = whileOutro("Deseja cadastrar o cliente no sistema para prosseguir com a compra? (Y/N)")
        if cadastrar:
            loading("Carregando",Texto.amarelo())
            cadastroCliente(cpf)
            pagamentoAluguel(cpf, True)
        else:
            print(f"{textoCor("Voltando para o Sistema!", Texto.vermelho())}")
            loading("Carregando", Texto.amarelo())
            menuAluguelDeFilmes()
    else:
        pagamentoAluguel(cpf, False)

def pagamentoAluguel(cpf, printaCarrinho):
    global carrinho
    global usuario

    cliente = manipulaDaos.daoCliente.findByCPF(cpf)

    totalCompra = 0
    for item in carrinho:
        if printaCarrinho:
            print(item.stringFilmeCarrinho())
        
        totalCompra += item.precoAluguelUnidade*item.qtdSelecionada

    cliente = Cliente(cliente.iloc[0,0], cliente.iloc[0,1], cliente.iloc[0,2], cliente.iloc[0,3], cliente.iloc[0,4],
                      cliente.iloc[0,5], cliente.iloc[0,6])
    
    if cliente.isFlamengo or cliente.assisteOnePiece or cliente.cidade == "Sousa":
        print(f"{textoCor("Você é um cliente habilitado a uma de nossas promoções!", Texto.verde())}")
        totalCompra *= Decimal('0.9')

    print(f"\nO total do aluguel é de {totalCompra}\n")
    print("Qual a forma de pagamento desejada?\n")

    pagamentos = ["Berries", "Boleto", "Cartão", "Pix"]

    while(True):

        print(f"{textoCor("1 - ", Texto.azul())}Berries\n")
        print(f"{textoCor("2 - ", Texto.azul())}Boleto\n")
        print(f"{textoCor("3 - ", Texto.azul())}Cartão\n")
        print(f"{textoCor("4 - ", Texto.azul())}Pix\n")

        opcao = input("Opção escolhida: ")

        if not(opcao.isdigit()):
            print(f"{textoCor("Opção inválida!\n", Texto.vermelho())}")
            continue
        
        opcao = int(opcao)

        if opcao <= 0 or opcao > 4:
            print(f"{textoCor("Opção inválida!\n", Texto.vermelho())}")
            continue

        break

    
    manipulaDaos.daoGeral.inserirAluguel(cliente.id, usuario.ID, totalCompra, pagamentos[opcao - 1], carrinho)

    print(f"{textoCor("Pagamento feito com sucesso!\n", Texto.verde())}")
    print(f"{textoCor("Filmes Alugados!", Texto.verde())}")

    carrinho = []

    input("Aperte qualquer tecla para continuar! ")
    loading("Carregando", Texto.amarelo())
    menuSistema()


def historicoAlugueis():
    """
    Seção da histórico de aluguéis
    """
    titulo("Histórico de Alugueis", Texto.negrito())
    
    print("Seção de histórico de aluguéis ainda não foi feita!")
    loading("Carregando", Texto.amarelo())
    menuInformacoesUsuario()

def confirmarDevolucao():
    """
    Seção da confirmação de aluguéis
    Como Marcelo pede para que os vendedores confirmam a compra, acho que seja relevante. A gente pode
    tirar se for necessário
    """
    titulo("Menu Devolução", Texto.negrito())

    cpf = checaEntrada("Digite o CPF do Cliente que deseja confirmar a devolução: ", "CPF Inválido!", lambda x: not(checaSeCPF(x)))
    
    resultado = manipulaDaos.daoCliente.findIdNomeByCPF(cpf)
    if resultado.empty:
        print(f"{textoCor("Não há cadastro com esse CPF!", Texto.vermelho())}")
        loading("Carregando", Texto.amarelo())
        menuSistema()
    else:
        idCliente = resultado.iloc[0,0]
        nomeCliente =  resultado.iloc[0,1]
        sobrenomeCliente = resultado.iloc[0,2]

        print(f"{textoCor("Cliente: ", Texto.ciano())} {nomeCliente} {sobrenomeCliente}\n")

        resultado = manipulaDaos.daoGeral.pegarFilmesSemDevolucao(int(idCliente))

        if resultado == []:
            print(f"{textoCor("Não há filmes a serem devolvidos por esse cliente!", Texto.vermelho())}")
            loading("Carregando", Texto.amarelo())
            menuSistema()
        else:
            idAlugas = []
            for item in resultado:
                if item[0] not in idAlugas:
                    idAlugas.append(item[0])
                print(Filme.printaComoFilme(item[0], item[3]
                                            ,item[1], item[2],), "\n")

            idAluguel = int(checaEntrada("Em qual Aluguel (ID) está o filme da devolução: ", "ID inválido!", lambda x: not(x.isdigit())))
            if not(idAluguel in idAlugas):
                print(f"{textoCor("ID de Aluguel Inválido! Voltando ao Menu Anterior!", Texto.vermelho())}")
                time.sleep(0.5)
                loading("Carregando", Texto.amarelo())
                menuInformacoesUsuario()
            else:
                idFilme = int(checaEntrada(f"ID do Filme do Aluguel {idAluguel} que será devolvido: ", "ID inválido", lambda x: not(x.isdigit())))

                idCerto = False
                for item in resultado:
                    if idAluguel == item[0] and idFilme == item[3]:
                        idCerto = True
                
                if not(idCerto):
                    print(f"{textoCor("ID de Filme Inválido! Voltando ao Menu Anterior!", Texto.vermelho())}")
                    time.sleep(0.5)
                    loading("Carregando", Texto.amarelo())
                    menuInformacoesUsuario()
                else:
                    manipulaDaos.daoGeral.devolverFilme(idAluguel, idFilme)
                    print(textoCor("Filme Devolvido com Sucesso!", Texto.verde()))
                    loading("Carregando", Texto.amarelo())
                    menuInformacoesUsuario()
                    
def exibirInformacoesUsuario():
    """
    Seção que exibe as informações do usuário
    """

    titulo("Informações do Usuário", Texto.negrito())
    print(usuario.stringFuncionario())
    
    input("\nAperte qualquer tecla para continuar ")
    loading("Recarregando", Texto.ciano())
    menuInformacoesUsuario()


def sairConta():
    """
    Função que sai da conta
    """ 
    global tipoUsuario #Muda o tipo de usuário para sem login
    global usuario #Muda o usuário para none

    sair = whileOutro("Deseja sair da loja? (Y/N)")


    if sair:
        sairLoja()
    else:
        loading("Saindo da conta", Texto.verde())
    
    tipoUsuario = TipoUsuario.SEM_LOGIN
    usuario = None

    menuSistema()

def sairLoja():
    """
    Função que sai da loja
    """
    loading("Saindo", Texto.amarelo())
    sys.exit()

def cadastroCliente(cpf):
    """
    Função que cadastra o cliente
    """
    global tipoUsuario
    global usuario
    global manipulaDaos

    titulo("Nova Conta Cliente")

    #Pega as informações do cliente
    primeiroNome = checaEntrada("Primeiro Nome do Cliente: ", "Nome de Cliente inválido!", lambda x: False) #Não há nada que impeça o input de qualquer nome
    print()
    ultimoNome = checaEntrada("Último nome do Cliente: ", "Nome de Cliente inválido", lambda x: False) #Não há nada que inpeça o input de qualquer nome
    print()
    cidade = checaEntrada(f"Cidade natal de {primeiroNome}: ", "Cidade inválida!", lambda x: False) #Não há nada que impeça a cidade digitada
    print()
    isFlamengo = inputYNtoBool(f"O Cliente {primeiroNome} torce para o Flamengo? (Y/N)")
    print()
    assisteOnePiece = inputYNtoBool(f"O cliente {primeiroNome} assiste One Piece? (Y/N)")
    print()


    #Cadastra o cliente. Como o ID é só autoincrementado, coloco como -1
    cliente = Cliente(-1, cpf, primeiroNome, ultimoNome, cidade, isFlamengo, assisteOnePiece)

    try:
        idCliente = manipulaDaos.daoCliente.inserir(cliente) #Tenta inserir o cliente
    except mysql.connector.Error as err: #Se houve algum erro
        print(err)
        time.sleep(10)
        if err.errno == 1062: #Se o erro foi de inserção, ou seja, alguma constraint foi de unique ou primary key foi violada
            print(f"{textoCor("Inserção inválida! CPF já existente!", Texto.vermelho())}")
        else: #Se foi outro erro
            print(f"{textoCor("Erro ao tentar inserir Cliente!", Texto.vermelho())}")

        loading("Carregando", Texto.amarelo())
        return None
    else:
        print(f"{textoCor(f"Cliente de CPF {cpf} inserido com sucesso", Texto.verde())}") 

        loading("Carregando", Texto.amarelo())
        return cpf

        
def cadastroFuncionario():
    global tipoUsuario
    global usuario
    global manipulaDaos

    titulo("Cadastro de Funcionários")

    primeiroNome = checaEntrada("Primeiro Nome do Funcionário: ", "Nome de Funcionário inválido!", lambda x: False)
    print()
    segundoNome = checaEntrada("Último nome do Funcionário: ", "Nome de Funcionário inválido", lambda x: False)
    print()
    login = checaEntrada("Nome de login do funcionário: ", "Nome de login inválido", lambda x: False)
    print()
    senha = checaEntrada(f"Senha do usuário de login {login}: ", "Senha inválida", lambda x: False)

    print(f"[1] - {textoCor("Vendedor\n", Texto.verde())}")
    print(f"[2] - {textoCor("Gerente\n", Texto.verde())}")

    opcao = checaEntrada("Digite uma das Opções de Tipo de Funcionário: ", "Tipo Inválido!", lambda x: not(x == "1" or x == "2"))

    if opcao == "1":
        funcionario = Funcionario(-1,primeiroNome, segundoNome, login, senha, "Vendedor")
    elif opcao == "2":
        funcionario = Funcionario(-1,primeiroNome, segundoNome, login, senha, "Gerente")

    try:
        idFuncionario = manipulaDaos.daoFuncionario.inserirVendedor(funcionario)
    except mysql.connector.Error as err:
        if err.errno == 1062:
            print(f"{textoCor("Inserção inválida! Login já existente!", Texto.vermelho())}")
        else:
            print(err)
            print(f"{textoCor("Erro ao tentar inserir funcionário!", Texto.vermelho())}")
        loading("Carregando", Texto.amarelo())
        menuCadastroFuncionario()

    else:
        print(f"{textoCor(f"Funcionário de id {idFuncionario} inserido com sucesso", Texto.verde())}")
        loading("Carregando", Texto.amarelo())
        menuCadastroFuncionario()

def demitirVendedor():
    global manipulaDaos

    while(True):
        titulo("DEMITIR VENDEDOR", Texto.negrito())

        idVendedor = input("Digite o ID do Vendedor que desejas demitir: ")

        sucesso = manipulaDaos.daoFuncionario.demitirVendedor(idVendedor)
        if sucesso:
            print(f"{textoCor("Vendedor demitido com sucesso!", Texto.verde())}")
        else:
            print(f"{textoCor(f"Vendedor de ID {idVendedor} não encontrado!", Texto.vermelho())}")

        sucesso = whileOutro("Deseja demitir outro vendedor? (Y/N)")
        if sucesso:
            loading("Recarregando", Texto.ciano())
            continue
        else:
            break

    loading("Carregando", Texto.amarelo())
    menuCadastroFuncionario()

def mostrarFuncionarios():
    global manipulaDaos

    titulo("Mostrar Funcionários", Texto.negrito())

    funcionarios = manipulaDaos.daoFuncionario.findAll()

    for _, row in funcionarios.iterrows():
        funcionario = Funcionario(row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4], row.iloc[5])
        print(funcionario.stringFuncionario(), end="\n\n")

    input("Digite qualquer tecla para voltar ao menu ")
    loading("Saindo", Texto.amarelo())
    menuCadastroFuncionario()
