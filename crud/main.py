# -*- encoding: utf-8 -*-

from usuario import (
    inserirUsuario, 
    atualizarUsuario, 
    excluirUsuario, 
    consultarExibirUsuarioJoin, 
    consultarExibirUsuarioSubconsulta 
)

from categoria import ( 
    cadastrarCategoria,
    excluirCategoria,
    atualizarCategoria,
    consultarCategoria 
)

from produto import ( 
    cadastrarProduto,
    excluirProduto,
    atualizarProduto,
    consultarProduto 
)

from promocao import ( 
    criarPromocao,
    excluirPromocao,
    atualizarPromocao,
    consultarPromocao,
    aplicarPromocao 
)

from pedido import (
    fazerPedido 
)

from pagamento import (
    computarPagamento,
    finalizarPagamento 
)

from notafiscal import (
    emitirNota 
)

from entrega import (
    enviarEntrega,
    receberEntrega
)


# Função para exibir o menu
def exibirMenu():
    print("\nMenu:")
    print("1. Usuários")
    print("2. Categorias")
    print("3. Produtos")
    print("4. Promoções")
    print("5. Pedidos")
    print("6. Pagamentos")
    print("7. Nota Fiscal")
    print("8. Entregas")
    print("9. Sair")

# Função para exibir o menu de usuários
def exibirMenuUsuario():
    print("\nMenu Usuários:")
    print("1. Inserir novo usuário")
    print("2. Excluir um usuário")
    print("3. Atualizar dados de um usuário")
    print("4. Consultar utilizando JOIN")
    print("5. Consultar utilizando subconsulta aninhada")
    print("6. Sair")

# Função para exibir o menu de categorias
def exibirMenuCategoria():
    print("\nMenu Categorias:")
    print("1. Cadastrar Categoria")
    print("2. Excluir Categoria")
    print("3. Atualizar Categoria")
    print("4. Consultar Categoria")
    print("5. Sair")
    
# Função para exibir o menu de produtos
def exibirMenuProduto():
    print("\nMenu Produtos:")
    print("1. Cadastrar Produto")
    print("2. Excluir Produto")
    print("3. Atualizar Produto")
    print("4. Consultar Produto")
    print("5. Sair")
    
# Função para exibir o menu de promoções
def exibirMenuPromocao():
    print("\nMenu Promoções:")
    print("1. Inserir nova promoção")
    print("2. Excluir promoção")
    print("3. Atualizar promoção")
    print("4. Consultar promoção")
    print("5. Aplicar promoção")
    print("6. Sair")
    
# Função para exibir o menu de pedido
def exibirMenuPedido():
    print("\nMenu Pedido:")
    print("1. Fazer Pedido")
    print("2. Sair")
    
# Função para exibir o menu de pagamento
def exibirMenuPagamento():
    print("\nMenu Pagamento:")
    print("1. Computar Pagamento")
    print("2. Finalizar Pagamento")
    print("3. Sair")

# Função para exibir o menu de nota fiscal
def exibirMenuNotaFiscal():
    print("\nMenu Nota Fiscal:")
    print("1. Emitir Nota Fiscal")
    print("2. Sair")
    
# Função para exibir o menu de entrega
def exibirMenuEntrega():
    print("\nMenu Entrega:")
    print("1. Enviar Entrega")
    print("2. Receber Entrega")
    print("3. Sair")

while True:
    exibirMenu()
    opcao = input("\nDigite o número da opção desejada: ")

    # Escolher opção para menu de usuários
    if opcao == "1":
        exibirMenuUsuario()
        opcaoUsuario = input("\nDigite o número da opção desejada: ")
        if opcaoUsuario == "1":
            inserirUsuario()
        elif opcaoUsuario == "2":
            excluirUsuario()
        elif opcaoUsuario == "3":
            atualizarUsuario()
        elif opcaoUsuario == "4":
            consultarExibirUsuarioJoin()
        elif opcaoUsuario == "5":
            consultarExibirUsuarioSubconsulta()
        elif opcaoUsuario == "6":
            print("Retornando ao menu principal...")
            continue
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")
            
    # Escolher opção para menu de categorias
    elif opcao == "2":
        exibirMenuCategoria()
        opcaoCategoria = input("\nDigite o número da opção desejada: ")
        if opcaoCategoria == "1":
            cadastrarCategoria()
        elif opcaoCategoria == "2":
            excluirCategoria()
        elif opcaoCategoria == "3":
            atualizarCategoria()
        elif opcaoCategoria == "4":
            consultarCategoria()
        elif opcaoCategoria == "5":
            print("Retornando ao menu principal...")
            continue
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")
            
    # Escolher opção para menu de produtos
    elif opcao == "3":
        exibirMenuProduto()
        opcaoProduto = input("\nDigite o número da opção desejada: ")
        if opcaoProduto == "1":
            cadastrarProduto()
        elif opcaoProduto == "2":
            excluirProduto()
        elif opcaoProduto == "3":
            atualizarProduto()
        elif opcaoProduto == "4":
            consultarProduto()
        elif opcaoProduto == "5":
            print("Retornando ao menu principal...")
            continue
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")
    
    # Escolher opção para menu de promoções
    elif opcao == "4":
        exibirMenuPromocao()
        opcaoPromocao = input("\nDigite o número da opção desejada: ")
        if opcaoPromocao == "1":
            criarPromocao()
        elif opcaoPromocao == "2":
            excluirPromocao()
        elif opcaoPromocao == "3":
            atualizarPromocao()
        elif opcaoPromocao == "4":
            consultarPromocao()
        elif opcaoPromocao == "5":
            aplicarPromocao()
        elif opcaoPromocao == "6":
            print("Retornando ao menu principal...")
            continue
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")
    
    # Escolher opção para menu de pedido
    elif opcao == "5":
        exibirMenuPedido()
        opcaoPedido = input("\nDigite o número da opção desejada: ")
        if opcaoPedido == "1":
            fazerPedido()
        elif opcaoPedido == "2":
            print("Retornando ao menu principal...")
            continue
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")
    
    # Escolher opção para menu de pagamento
    elif opcao == "6":
        exibirMenuPagamento()
        opcaoPagamento = input("\nDigite o número da opção desejada: ")
        if opcaoPagamento == "1":
            computarPagamento()
        elif opcaoPagamento == "2":
            finalizarPagamento()
        elif opcaoPagamento == "3":
            print("Retornando ao menu principal...")
            continue
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")
    
    # Escolher opção para menu de nota fiscal
    elif opcao == "7":
        exibirMenuNotaFiscal()
        opcaoNotaFiscal = input("\nDigite o número da opção desejada: ")
        if opcaoNotaFiscal == "1":
            emitirNota()
        elif opcaoNotaFiscal == "2":
            print("Retornando ao menu principal...")
            continue
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")
    
    # Escolher opção para menu de entrega
    elif opcao == "8":
        exibirMenuEntrega()
        opcaoEntrega = input("\nDigite o número da opção desejada: ")
        if opcaoEntrega == "1":
            enviarEntrega()
        elif opcaoEntrega == "2":
            receberEntrega()
        elif opcaoEntrega == "3":
            print("Retornando ao menu principal...")
            continue
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")

    # Encerrar
    elif opcao == "9":
        print("Encerrando o programa...")
        break
    else:
        print("Opção inválida. Por favor, escolha uma opção válida.")
