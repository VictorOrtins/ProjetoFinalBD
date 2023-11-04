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


class TipoUsuario(Enum):
    CLIENTE = 1
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
    listaFuncoes = [menuLogin, menuLoja, cadastroCliente, sairLoja] #Lista de funções que são chamadas após a escolha do usuário
    while(True):
        titulo("ESCOLHA DE LOGIN", Texto.negrito())

        print(f"{textoCor("1 - ", Texto.azul())}Login\n")
        print(f"{textoCor("2 - ", Texto.azul())}Entrar sem Login\n")
        print(f"{textoCor("3 - ", Texto.azul())}Novo Cadastro\n")
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

    if opcao != 4: #Se a opção não for a de sair (Sair possui um loading próprio)
        loading("Carregando", Texto.amarelo())
    
    listaFuncoes[opcao - 1]() #Chama a função correspondente a opção que o usuário digitou

def menuLogin():
    """
    Função que chama as funções referentes ao login
    """
    listaFuncoes = [loginCliente, loginFuncionario, menuIniciar] #Funções que serão chamadas a partir da escolha do usuário
    while(True):
        titulo("ESCOLHA DE LOGIN", Texto.negrito())

        print(f"{textoCor("1 - ", Texto.azul())}Login de Cliente\n")
        print(f"{textoCor("2 - ", Texto.azul())}Login de Funcionário\n")
        print(f"{textoCor("3 - ", Texto.azul())}Voltar\n")

        try:
            opcao = int(input("Escolha uma opção: "))
        except ValueError: #Trata um input não numeral
            print(textoCor("Opcão Inválida!\n",Texto.vermelho()))
            loading("Recarregando", Texto.ciano())
            continue
            
        if opcao <= 0 or opcao > 3: #Trata um input fora das opções válidas
            print(textoCor("Opcão Inválida!\n",Texto.vermelho()))
            loading("Recarregando", Texto.ciano())
            continue

        break

    loading("Carregando", Texto.amarelo())
    listaFuncoes[opcao - 1]()


def loginCliente():
    """
    Função que faz o login do cliente
    """

    global tipoUsuario #Se o login for bem sucedido, o tipo do usuário dentro do sistema precisa ser atualizado
    global usuario #Se o login for bem sucedido, o usuário utilizando o sistema precisa ser atualizado
    global manipulaDaos #Variável que manipula os daos


    while(True):
        titulo("LOGIN CLIENTE", Texto.negrito())

        naoEncontrado = False #É assumido primeiramente que o usuário será encontrado

        login = checaEntrada("Login: ", "", lambda x: False) #Checa se o login é válido
        senha = checaEntrada("Senha: ", "", lambda x: False) #Checa se a senha é válida

        cliente = manipulaDaos.daoCliente.findByLogin(login) #Tenta achar os dados do cliente a partir do login
        
        if cliente.empty: #Se o usuário não for encontrada (Ou seja, o dataframe enviado for vazio)
            print(textoCor("Usuário não encontrado!", Texto.vermelho()))
            naoEncontrado = True
        elif cliente.iloc[0,6] != senha: #Se a senha digitada for diferente da senha real do usuário (Se a coluna 6 da única linha retornada for diferente da senha digitada)
            print(textoCor("Senha Incorreta!", Texto.vermelho()))
            naoEncontrado = True

        if naoEncontrado: #Se o usuário não for encontrado ou a senha for incorreta
            continuar = whileOutro("Deseja continuar sem login? (Y/N)")
            if continuar: #Se for desejado continuar sem login
                break
            loading("Recarregando", Texto.amarelo())
            continue #Senão, tenta fazer login novamente

        #Cria o objeto que representa o cliente
        cliente = Cliente(cliente.iloc[0,0], cliente.iloc[0,1], cliente.iloc[0,2], cliente.iloc[0,3], cliente.iloc[0,4], cliente.iloc[0,5], cliente.iloc[0,6], cliente.iloc[0,7], cliente.iloc[0,8])

        break

    if not(naoEncontrado): #Se o cliente for encontrado
        print(textoCor("\nLogin de Cliente bem-sucedido!", Texto.verde()))
        tipoUsuario = TipoUsuario.CLIENTE
        usuario = cliente

    loading("Carregando", Texto.amarelo())
    menuLoja() #Redireciona para o menu da loja

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
        
        funcionario = manipulaDaos.daoFuncionario.findByLogin(login) #Tenta achar o funcionário a partir do login

        if funcionario.empty: #Se o usuário não for encontrado
            print(textoCor("Usuário não encontrado!", Texto.vermelho()))
            naoEncontrado = True
        elif funcionario.iloc[0,4] != senha: #Se a senha for inválida
            print(textoCor("Senha inválida!", Texto.vermelho()))
            naoEncontrado = True

        if naoEncontrado: #Se o usuário não foi encontrado ou a senha é inválida
            continuar = whileOutro("Deseja continuar sem login? (Y/N)") #Pergunta se quer continuar sem login
            if continuar: #Se quiser, tenta ir pra loja
                break

            loading("Recarregando", Texto.amarelo())
            continue

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
    menuLoja() #Sempre redireciona para o menu da loja

def menuLoja():
    """
    Função que representa o menu principal da loja. 
    Esse menu muda de visualização a partir do tipo do usuário que está logando no sistema
    """

    if tipoUsuario == TipoUsuario.VENDEDOR: #Se for um funcionário
        listaFuncoes = [menuInformacoesUsuario, menuCadastroEstoque, sairLoja] #Define as funções
        #Texto que será exibido para o usuário digitar a opção que ele quer
        #Ele vai conter o nome do funcionário, pode redirecionar para o menu de informações de usuário,
        #O menu de cadastro de estoque e para a função que sai do sistema

        txtInput = "".join([f"{textoCor("Funcionário: ", Texto.magenta())}{usuario.primeiroNome} {usuario.ultimoNome}\n\n",f"{textoCor("1 - ", Texto.azul())}Informações do Usuário\n\n",
        f"{textoCor("2 - ", Texto.azul())}Cadastro de Estoque\n\n", f"{textoCor("3 - ", Texto.azul())}Sair da Loja\n"])

        teste = 3 #Teste que será feito no input 

    elif tipoUsuario == TipoUsuario.CLIENTE: #Se for um cliente
        listaFuncoes = [menuInformacoesUsuario, menuAluguelDeFilmes, verCarrinho, sairLoja]
        #Texto que será exibido para o usuário digitar uma opção
        #Ele vai conter o nome do cliente, pode redirecionar para o menu de informações do usuário,
        #O menu de aluguel de filmes, o menu de ver o carrinho e a função que sai do sistema
        txtInput = "".join([f"{textoCor("Cliente: ", Texto.verde())}{usuario.primeiroNome} {usuario.ultimoNome}\n\n",f"{textoCor("1 - ", Texto.azul())}Informações do Usuário\n\n" 
        ,f"{textoCor("2 - ", Texto.azul())}Aluguel de Filmes\n\n",f"{textoCor("3 - ", Texto.azul())}Ver Carrinho\n\n",
        f"{textoCor("4 - ", Texto.azul())}Sair da Loja\n"])

        teste = 4 #4 opções

    elif tipoUsuario == TipoUsuario.SEM_LOGIN: #Se não tiver feito login. A visualização dele é mais parecida com a do cliente
        listaFuncoes = [menuAluguelDeFilmes, verCarrinho, menuIniciar, sairLoja] #Lista de funções
        #Basicamente a mesma coisa do cliente, porém tem a opção de fazer o login e não se pode ver as informações
        #do usuário
        txtInput = "".join([
        f"{textoCor("1 - ", Texto.azul())}Aluguel de Filmes\n\n",f"{textoCor("2 - ", Texto.azul())}Ver Carrinho\n\n", f"{textoCor("3 - ", Texto.azul())}Fazer Login\n\n",
        f"{textoCor("4 - ", Texto.azul())}Sair da Loja\n"])

        teste = 4 #4 opções
    elif tipoUsuario == TipoUsuario.GERENTE:
        listaFuncoes = [menuInformacoesUsuario, menuCadastroEstoque, menuCadastroFuncionario, sairLoja] #Define as funções

        #Mesma coisa do vendedor porém com a opção de cadastrar vendedores
        txtInput = "".join([f"{textoCor("Gerente: ", Texto.azul())}{usuario.primeiroNome} {usuario.ultimoNome}\n\n",f"{textoCor("1 - ", Texto.azul())}Informações do Usuário\n\n",
        f"{textoCor("2 - ", Texto.azul())}Cadastro de Estoque\n\n", f"{textoCor("3 - ", Texto.azul())}Cadastro de Vendedores\n\n", f"{textoCor("4 - ", Texto.azul())}Sair da Loja\n"])

        teste = 4

        
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
        
        
        if opcao <= 0 or opcao > teste: #Trata um input fora das opções válidas
            print(textoCor("Opcão Inválida!\n",Texto.vermelho()))
            loading("Recarregando", Texto.ciano())
            continue
        break

    if opcao != teste:
        loading("Carregando", Texto.amarelo())
    listaFuncoes[opcao - 1]()

def menuCadastroFuncionario():
    listaFuncoes = [cadastroVendedor, demitirVendedor, mostrarFuncionarios, menuLoja]
    teste = 4
    while(True):
        titulo("MENU DO CADASTRO FUNCIONÁRIO", Texto.negrito())

        print(f"{textoCor("1 - ", Texto.azul())}Cadastro de Vendedor\n")
        print(f"{textoCor("2 - ", Texto.azul())}Demitir Vendedor\n")
        print(f"{textoCor("3 - ", Texto.azul())}Mostrar Todos os Funcionários\n")
        print(f"{textoCor("4 - ", Texto.azul())}Voltar para Loja\n")

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

    loading("Carregando", Texto.amarelo())
    listaFuncoes[opcao - 1]() #Chamar a função da lista de funções

def menuInformacoesUsuario():
    """
    Menu que redireciona para as informações do usuário
    """
    global tipoUsuario #É preciso chegar o tipo de usuário
    global usuario #E mostrar informações do usuário

    if tipoUsuario == TipoUsuario.CLIENTE: #Se for um cliente
        listaFuncoes = [exibirInformacoesUsuario, exibirHistoricoFilmes, menuLoja, sairConta] #Funções que podem ser chamadas

        #Input que será pedido ao usuário
        #Pergunta se o cliente quer ver as informações do cliente, o histórico de filmes alugados
        #Se quer voltar ao menu da loja ou sair da conta
        txtInput = "".join([f"{textoCor("Cliente: ", Texto.verde())}{usuario.primeiroNome} {usuario.ultimoNome}\n\n",f"{textoCor("1 - ", Texto.azul())}Exibir Informações do Cliente\n\n",
        f"{textoCor("2 - ", Texto.azul())}Histórico de Filmes Alugados\n\n", f"{textoCor("3 - ", Texto.azul())}Voltar para o Menu da Loja\n\n",
        f"{textoCor("4 - ", Texto.azul())}Sair da conta\n\n"])

    elif tipoUsuario == TipoUsuario.VENDEDOR or tipoUsuario == TipoUsuario.GERENTE: #Se for um funcionário
        listaFuncoes = [exibirInformacoesUsuario, alugueisConfirmacao, menuLoja, sairConta] #Funções que podem ser chamadas

        #Pergunta se o funcioário quer ver as informações do funcionário, os aluguéis pendentes de confirmação,
        #Se quer voltar ao menu da loja ou sair da conta

        if tipoUsuario == TipoUsuario.GERENTE:
            textoNome = textoCor("Gerente: ", Texto.azul())
        elif tipoUsuario == TipoUsuario.VENDEDOR:
            textoNome = textoCor("Vendedor: ", Texto.magenta())
        
        txtInput = "".join([f"{textoNome}{usuario.primeiroNome} {usuario.ultimoNome}\n\n",f"{textoCor("1 - ", Texto.azul())}Exibir Informações do Funcionário\n\n",
        f"{textoCor("2 - ", Texto.azul())}Aluguéis pendentes de confirmação\n\n", f"{textoCor("3 - ", Texto.azul())}Voltar para o Menu da Loja\n\n",
        f"{textoCor("4 - ", Texto.azul())}Sair da conta\n\n"])
    elif tipoUsuario == TipoUsuario.SEM_LOGIN: #Se não for nada. Isso aqui é só um teste, pra se der algo errado
        print(textoCor("ERRO!!!", Texto.vermelho()))
        sys.exit()

    while(True):
        teste = 4 #Nos 2 casos, o menu tem 4 opções

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

    if opcao != 4: #Se o usuário não escolher sair
        loading("Carregando", Texto.amarelo())
    
    listaFuncoes[opcao - 1]() #Chamar a função da lista de funções

def menuAluguelDeFilmes():
    """
    Menu de aluguel de filmes
    Ainda não está com o SQL!
    """
    global tipoUsuario #É preciso checar o tipo do usuário
    global usuario #É preciso pegar informações do usuário

    #Por enquanto está igual, mas acho que eu pensei em algo que fosse diferenciar os 2. Acho que seria o fato do usuário sem login
    #Não poder fazer a compra sem digitar as informações

    listaFuncoes = [pesquisarNome, pesquisarPreco, pesquisarGenero, pesquisarFilmeAtor, pesquisarFilmeNacionalidade, pesquisarFilmeDiretor, menuLoja] #Funções
    txtInput = "".join([f"{textoCor("Cliente: ", Texto.verde())}{usuario.primeiroNome} {usuario.ultimoNome}\n\n",f"{textoCor("1 - ", Texto.azul())}Pesquisar por Nome\n\n",
    f"{textoCor("2 - ", Texto.azul())}Pesquisar por Preço\n\n", f"{textoCor("3 - ", Texto.azul())}Pesquisar por Gênero\n\n",
    f"{textoCor("4 - ", Texto.azul())}Pesquisar por Filmes do Ator\n\n", f"{textoCor("5 - ", Texto.azul())}Pesquisar por Filmes do Ator que nasceu em\n\n",
    f"{textoCor("6 - ", Texto.azul())}Pesquisar por Filmes do Diretor\n\n", f"{textoCor("7 - ", Texto.azul())}Voltar para o menu da loja\n\n"])
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
    
    listaFuncoes[opcao - 1]()

def pesquisarNome():
    """
    Pesquisa um filme pelo nome e tenta adicionar no carrinho
    """
    global carrinho #Essa função mexe com o carrinho, que está de alguma forma implementado

    titulo("Pesquisa por Nome", Texto.negrito())

    nomeFilme = input("Nome do Filme que você deseja pesquisar: ") #Pega o input

    resultado = manipulaDaos.daoFilme.findByName(nomeFilme)

    if resultado.empty:
        print(textoCor("Não há filmes com esse nome!", Texto.vermelho()))
        loading("Carregando", Texto.amarelo())
        menuAluguelDeFilmes()
    else:
        for _, row in resultado.iterrows(): #Mostra os filmes
            filme = Filme(row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4], row.iloc[5], row.iloc[6], row.iloc[7])
            print(filme.stringFilme())

        adicionar = whileOutro("Deseja adicionar um desses filmes no carrinho? (Y/N)")
  
        if adicionar:
            idFilme = checaEntrada("\nDigite o ID do filme que deseja adicionar no carrinho: ", "ID Inválido", lambda x: not(x.isdigit()))
            
            qtdFilme = checaEntrada(f"\nDigite a quantidade do filme de ID {idFilme} que deseja adicionar: ", "Quantidade inválida!", lambda x: not(x.isdigit()))

            for _,row in resultado.iterrows():
                if int(row.iloc[0]) == int(idFilme):
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
            loading("Carregando", Texto.amarelo())
            menuAluguelDeFilmes()

def pesquisarPreco():
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
        menuAluguelDeFilmes()
    else:
        for _, row in resultado.iterrows(): #Mostra os filmes
            filme = Filme(row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4], row.iloc[5], row.iloc[6], row.iloc[7])
            print(filme.stringFilme())

        adicionar = whileOutro("Deseja adicionar um desses filmes no carrinho? (Y/N)")
  
        if adicionar:
            idFilme = checaEntrada("Digite o ID do filme que deseja adicionar no carrinho: ", "ID Inválido", lambda x: not(x.isdigit()))
            
            qtdFilme = checaEntrada(f"Digite a quantidade do filme de ID {idFilme} que deseja adicionar: ", "Quantidade inválida!", lambda x: not(x.isdigit()))

            for _,row in resultado.iterrows():
                if int(row.iloc[0]) == int(idFilme):
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
            loading("Carregando", Texto.amarelo())
            menuAluguelDeFilmes()

def pesquisarGenero():
    """
    Pesquisa um filme pelo seu gênero
    Não está com o SQL!
    """
    global carrinho #Essa função mexe com o carrinho, que está de alguma forma implementado

    titulo("Pesquisa por Gênero", Texto.negrito())

    nomeFilme = input("Gênero do Filme que você deseja pesquisar: ") #Pega o input

    resultado = manipulaDaos.daoFilme.findByGenre(nomeFilme)

    if resultado.empty:
        print(textoCor("Não há filmes desse gênero!", Texto.vermelho()))
        loading("Carregando", Texto.amarelo())
        menuAluguelDeFilmes()
    else:
        for _, row in resultado.iterrows(): #Mostra os filmes
            filme = Filme(row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4], row.iloc[5], row.iloc[6], row.iloc[7])
            print(filme.stringFilme())

        adicionar = whileOutro("Deseja adicionar um desses filmes no carrinho? (Y/N)")
  
        if adicionar:
            idFilme = checaEntrada("\nDigite o ID do filme que deseja adicionar no carrinho: ", "ID Inválido", lambda x: not(x.isdigit()))
            
            qtdFilme = checaEntrada(f"\nDigite a quantidade do filme de ID {idFilme} que deseja adicionar: ", "Quantidade inválida!", lambda x: not(x.isdigit()))

            for _,row in resultado.iterrows():
                if int(row.iloc[0]) == int(idFilme):
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
            loading("Carregando", Texto.amarelo())
            menuAluguelDeFilmes()

def pesquisarFilmeAtor():
    global carrinho #Essa função mexe com o carrinho, que está de alguma forma implementado

    titulo("Pesquisa por Gênero", Texto.negrito())

    nomeAtor = input("Pesquise filmes em que aparecem o ator: ") #Pega o input

    resultado = manipulaDaos.daoElenco.getFilmeByAtor(nomeAtor)

    if resultado.empty:
        print(textoCor("Não há filmes com esse ator no nosso sistema!", Texto.vermelho()))
        loading("Carregando", Texto.amarelo())
        menuAluguelDeFilmes()
    else:
        for _, row in resultado.iterrows(): #Mostra os filmes
            filme = Filme(row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4], row.iloc[5], row.iloc[6], row.iloc[7])
            print(filme.stringFilme())

        adicionar = whileOutro("Deseja adicionar um desses filmes no carrinho? (Y/N)")
  
        if adicionar:
            idFilme = checaEntrada("\nDigite o ID do filme que deseja adicionar no carrinho: ", "ID Inválido", lambda x: not(x.isdigit()))
            
            qtdFilme = checaEntrada(f"\nDigite a quantidade do filme de ID {idFilme} que deseja adicionar: ", "Quantidade inválida!", lambda x: not(x.isdigit()))

            for _,row in resultado.iterrows():
                if int(row.iloc[0]) == int(idFilme):
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
            loading("Carregando", Texto.amarelo())
            menuAluguelDeFilmes()
def pesquisarFilmeNacionalidade():
    global carrinho #Essa função mexe com o carrinho, que está de alguma forma implementado

    titulo("Pesquisa por Atores de uma Nacionalidade", Texto.negrito())

    nacionalidade = input("Pesquise filmes em que aparecem Atores da Nacionalidade: ") #Pega o input

    resultado = manipulaDaos.daoElenco.getFilmeByNacionalidade(nacionalidade)

    if resultado.empty:
        print(textoCor("Não há filmes com atores dessa nacionalidade no nosso sistema!", Texto.vermelho()))
        loading("Carregando", Texto.amarelo())
        menuAluguelDeFilmes()
    else:
        for _, row in resultado.iterrows(): #Mostra os filmes
            filme = Filme(row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4], row.iloc[5], row.iloc[6], row.iloc[7])
            print(filme.stringFilme())

        adicionar = whileOutro("Deseja adicionar um desses filmes no carrinho? (Y/N)")
  
        if adicionar:
            idFilme = checaEntrada("\nDigite o ID do filme que deseja adicionar no carrinho: ", "ID Inválido", lambda x: not(x.isdigit()))
            
            qtdFilme = checaEntrada(f"\nDigite a quantidade do filme de ID {idFilme} que deseja adicionar: ", "Quantidade inválida!", lambda x: not(x.isdigit()))

            for _,row in resultado.iterrows():
                if int(row.iloc[0]) == int(idFilme):
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
            loading("Carregando", Texto.amarelo())
            menuAluguelDeFilmes()
def pesquisarFilmeDiretor():
    global carrinho #Essa função mexe com o carrinho, que está de alguma forma implementado

    titulo("Pesquisa Filme por Diretor", Texto.negrito())

    diretor = input("Pesquise filmes do Diretor ") #Pega o input

    resultado = manipulaDaos.daoFilme.findByDirector(diretor)

    if resultado.empty:
        print(textoCor("Não há filmes desse diretor no nosso sistema!", Texto.vermelho()))
        loading("Carregando", Texto.amarelo())
        menuAluguelDeFilmes()
    else:
        for _, row in resultado.iterrows(): #Mostra os filmes
            filme = Filme(row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4], row.iloc[5], row.iloc[6], row.iloc[7])
            print(filme.stringFilme())

        adicionar = whileOutro("Deseja adicionar um desses filmes no carrinho? (Y/N)")
  
        if adicionar:
            idFilme = checaEntrada("\nDigite o ID do filme que deseja adicionar no carrinho: ", "ID Inválido", lambda x: not(x.isdigit()))
            
            qtdFilme = checaEntrada(f"\nDigite a quantidade do filme de ID {idFilme} que deseja adicionar: ", "Quantidade inválida!", lambda x: not(x.isdigit()))

            for _,row in resultado.iterrows():
                if int(row.iloc[0]) == int(idFilme):
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
            loading("Carregando", Texto.amarelo())
            menuAluguelDeFilmes()

def menuCadastroEstoque():
    """
    Função que redireciona para o menu de cadastro de estoque de filmes
    Para poder utilizar a função funcionalmente, precisei mudar um pouco o cadastro
    Se ele retornou do cadastro, vai direto para 
    """
    global manipulaDaos
    if (menuCadastro(manipulaDaos)):
        menuLoja()

def voltarMenuLoja():
    """
    Função que redireciona para o menu da loja
    """
    loading("Carregando", Texto.amarelo())
    menuLoja()

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
        menuLoja()
    else:
        print(len(carrinho))
        for item in carrinho:
            print(item.stringFilmeCarrinho())
        
        print()

        finalizar = whileOutro("Deseja finalizar a compra?(Y/N) ")
        if finalizar:
            loading("Carregando", Texto.amarelo())
            finalizarCompra()
        else:
            input("Pressione qualquer tecla para voltar ao Menu da Loja ")
            loading("Carregando", Texto.amarelo())
            menuLoja()

def finalizarCompra():
    """
    Função que finaliza a compra
    """
    global carrinho

    totalCompra = 18.9

    titulo("FINALIZAR COMPRA", Texto.negrito())

    for item in carrinho:
        print(item.stringFilmeCarrinho())

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
    loading("Carregando", Texto.amarelo())
    menuLoja()



def alugueisConfirmacao():
    """
    Seção da confirmação de aluguéis
    Como Marcelo pede para que os vendedores confirmam a compra, acho que seja relevante. A gente pode
    tirar se for necessário
    """
    print("Seção de confirmação ainda não foi feita!")
    loading("Carregando", Texto.amarelo())
    menuInformacoesUsuario()

def exibirInformacoesUsuario():
    """
    Seção que exibe as informações do usuário
    """

    titulo("Informações do Usuário", Texto.negrito())
    print(usuario.stringInformacoes())
    
    input("\nAperte qualquer tecla para continuar ")
    loading("Recarregando", Texto.ciano())
    menuInformacoesUsuario()


def exibirHistoricoFilmes():
    """
    Seção que exibe o histórico de filmes
    Não possui SQL ainda"
    """
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

    menuLoja()

def sairLoja():
    """
    Função que sai da loja
    """
    loading("Saindo", Texto.amarelo())
    sys.exit()

def cadastroCliente():
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
    cpf = checaEntrada(f"CPF do cliente {primeiroNome}: ", "CPF do cliente inválido!", lambda x: not(checaSeCPF(x))) #Checa se o CPF é válidop
    print()
    login = checaEntrada(f"Nome de login do cliente {primeiroNome}: ", "Nome de login inválido", lambda x: False) #Não há nada que impeça o input do login
    print()
    senha = checaEntrada(f"Senha do usuário de login {login}: ", "Senha inválida", lambda x: False) #Não há nada que impeça a senha digitada
    print()
    cidade = checaEntrada(f"Cidade natal de {primeiroNome}: ", "Cidade inválida!", lambda x: False) #Não há nada que impeça a cidade digitada
    print()
    isFlamengo = inputYNtoBool(f"O Cliente {primeiroNome} torce para o Flamengo? (Y/N)")
    print()
    assisteOnePiece = inputYNtoBool(f"O cliente {primeiroNome} assiste One Piece? (Y/N)")
    print()


    #Cadastra o cliente. Como o ID é só autoincrementado, coloco como -1
    cliente = Cliente(-1, cpf, primeiroNome, ultimoNome, cidade, login, senha, isFlamengo, assisteOnePiece)

    try:
        idCliente = manipulaDaos.daoCliente.inserir(cliente) #Tenta inserir o cliente
    except mysql.connector.Error as err: #Se houve algum erro
        if err.errno == 1062: #Se o erro foi de inserção, ou seja, alguma constraint foi de unique ou primary key foi violada
            print(f"{textoCor("Inserção inválida! Login e/ou Nome de Cliente já existente!", Texto.vermelho())}")
        else: #Se foi outro erro
            print(f"{textoCor("Erro ao tentar inserir Cliente!", Texto.vermelho())}")

        loading("Carregando", Texto.amarelo())
        menuIniciar() #Redireciona para o primeiro menu
    else:
        print(f"{textoCor("Cliente inserido com sucesso", Texto.verde())}") 
        entrar = whileOutro("Deseja entrar com esse usuário? (Y/N)") #Vê se o usuário só quis cadastrar o cliente
        #Ou se ele quer entrar com ele tbm

        if entrar: #Se for desejado entrar com esse usuário
            
            cliente.id = idCliente

            #Atualiza o usuário e o tipo do usuário
            tipoUsuario = TipoUsuario.CLIENTE
            usuario = cliente

            loading("Carregando", Texto.amarelo())
            menuLoja()
        else: #Se a pessoa só quis cadastrar o usuário
            loading("Carregando", Texto.amarelo())
            menuIniciar()
        

def cadastroVendedor():
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

    funcionario = Funcionario(-1,primeiroNome, segundoNome, login, senha, "Vendedor")

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
