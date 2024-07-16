# -*- coding: utf-8 -*-
import mysql.connector
from datetime import datetime

def conectar_banco():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="LojaOnlinev2"
    )

def fazerPedido():
    try:
        # Conectar ao banco de dados
        connection = conectar_banco()

        if connection.is_connected():
            cursor = connection.cursor()

            # Solicitar o id do usuário
            idUsuario = int(input("Digite o ID do usuário: "))

            # Verificar se o usuário é do tipo cliente
            cursor.execute("SELECT tipoUsuario FROM Usuario WHERE idUsuario = %s", (idUsuario,))
            tipoUsuario = cursor.fetchone()
            print(f"DEBUG: tipoUsuario retornado do banco de dados: {tipoUsuario}")

            if not tipoUsuario or tipoUsuario[0] != 'CLI':
                print("Apenas usuários do tipo cliente podem fazer pedidos.")
                return

            # Solicitar os produtos desejados e suas quantidades
            produtos = {}
            while True:
                produto_id_input = input("Digite o ID do produto desejado (ou 0 para encerrar): ")
                if not produto_id_input:
                    print("O ID do produto não pode ser vazio.")
                    continue
                produto_id = int(produto_id_input)
                if produto_id == 0:
                    break
                quantidade_input = input("Digite a quantidade desejada: ")
                if not quantidade_input:
                    print("A quantidade não pode ser vazia.")
                    continue
                quantidade = int(quantidade_input)
                produtos[produto_id] = quantidade

            # Verificar se algum produto foi escolhido
            if not produtos:
                print("Nenhum produto foi escolhido. Pedido não realizado.")
                return

            # Verificar se os produtos existem e a quantidade disponível
            total_pedido = 0
            for produto_id, quantidade in produtos.items():
                cursor.execute("SELECT valorProduto, qtdEstoque FROM Produto WHERE idProduto = %s", (produto_id,))
                produto = cursor.fetchone()

                if not produto:
                    print(f"O produto com o ID {produto_id} não foi encontrado.")
                    return

                valor_produto = produto[0]
                quantidade_estoque = produto[1]

                if quantidade > quantidade_estoque:
                    print(f"A quantidade desejada do produto com ID {produto_id} excede a quantidade disponível.")
                    return

                total_pedido += valor_produto * quantidade

            # Verificar se a transação já está em andamento
            if not connection.in_transaction:
                connection.start_transaction()

            # Inserir o pedido na tabela Pedido
            data_pedido = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            status_pedido = 'ATIVO'

            cursor.execute("INSERT INTO Pedido (idCliente, dataPedido, statusPedido) VALUES (%s, %s, %s)", (idUsuario, data_pedido, status_pedido))
            id_pedido = cursor.lastrowid

            # Inserir os produtos do pedido na tabela ProdutosPedidos
            for produto_id, quantidade in produtos.items():
                cursor.execute("INSERT INTO ProdutosPedidos (idPedido, idProduto, qtdEscolhida) VALUES (%s, %s, %s)", (id_pedido, produto_id, quantidade))

                # Atualizar o estoque do produto
                novo_estoque = quantidade_estoque - quantidade
                cursor.execute("UPDATE Produto SET qtdEstoque = %s WHERE idProduto = %s", (novo_estoque, produto_id))

            # Inserir o pedido na tabela Pagamento
            cursor.execute("INSERT INTO Pagamento (idPedido, valorTotal, dataPagamento, formaPagamento, statusPagamento) VALUES (%s, %s, %s, %s, %s)", (id_pedido, total_pedido, data_pedido, 'credito', 'Pendente'))

            connection.commit()
            print("Pedido realizado com sucesso!")

    except mysql.connector.Error as error:
        # Rollback em caso de erro
        connection.rollback()
        print(f"Erro ao fazer o pedido: {error}")

    finally:
        # Fechar a conexão com o banco de dados
        if connection.is_connected():
            cursor.close()
            connection.close()
