# -*- coding: utf-8 -*-
import mysql.connector

from usuario import verificarFornecedorExiste
from categoria import verificarCategoriaExiste

# Função para conectar ao banco de dados
def conectar_banco():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="LojaOnlinev2"
    )

# Função para cadastrar um novo produto
def cadastrarProduto():
    try:
        nome_produto = input("Digite o nome do novo produto: ").strip()
        if not nome_produto:
            print("O nome do produto não pode ser vazio.")
            return

        valor_produto_input = input("Digite o valor do novo produto: ").strip()
        if not valor_produto_input:
            print("O valor do produto não pode ser vazio.")
            return
        valor_produto = float(valor_produto_input)

        qtd_estoque_input = input("Digite a quantidade em estoque do novo produto: ").strip()
        if not qtd_estoque_input:
            print("A quantidade em estoque do produto não pode ser vazia.")
            return
        qtd_estoque = int(qtd_estoque_input)

        info_produto = input("Digite as informações adicionais do novo produto: ").strip()
        if not info_produto:
            print("As informações adicionais do produto não podem ser vazias.")
            return

        id_categoria_input = input("Digite o ID da categoria do novo produto: ").strip()
        if not id_categoria_input:
            print("O ID da categoria do produto não pode ser vazio.")
            return
        id_categoria = int(id_categoria_input)

        id_fornecedor_input = input("Digite o ID do fornecedor do novo produto: ").strip()
        if not id_fornecedor_input:
            print("O ID do fornecedor do produto não pode ser vazio.")
            return
        id_fornecedor = int(id_fornecedor_input)

        # Verificar se o idCategoria existe na tabela Categoria
        if not verificarCategoriaExiste(id_categoria):
            print("O ID da categoria fornecido não existe na tabela Categoria.")
            return

        # Verificar se o idFornecedor existe na tabela Fornecedor
        if not verificarFornecedorExiste(id_fornecedor):
            print("O ID do fornecedor fornecido não existe na tabela Fornecedor.")
            return

        connection = conectar_banco()
        cursor = connection.cursor()

        sql = "INSERT INTO Produto (nomeProduto, valorProduto, qtdEstoque, infoProduto, idCategoria, idFornecedor) VALUES (%s, %s, %s, %s, %s, %s)"
        data = (nome_produto, valor_produto, qtd_estoque, info_produto, id_categoria, id_fornecedor)

        cursor.execute(sql, data)
        connection.commit()

        produto_id = cursor.lastrowid

        cursor.close()
        connection.close()

        print("O novo produto foi cadastrado com sucesso com o ID:", produto_id)
        
    except mysql.connector.Error as error:
        print(f"Erro ao cadastrar o produto: {error}")


# Função para verificar se o ID do produto existe na tabela Produto
def verificarProdutoExiste(id_produto):
    try:
        connection = conectar_banco()
        cursor = connection.cursor()

        sql = "SELECT COUNT(*) FROM Produto WHERE idProduto = %s"
        cursor.execute(sql, (id_produto,))
        resultado = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        return resultado > 0
    
    except mysql.connector.Error as error:
        print(f"Erro ao verificar a existência do produto: {error}")
        return False

# Função para excluir um produto
def excluirProduto():
    try:
        id_produto_input = input("Digite o ID do produto que deseja excluir: ").strip()
        if not id_produto_input:
            print("O ID do produto não pode ser vazio.")
            return
        id_produto = int(id_produto_input)

        # Verificar se o idProduto existe no banco de dados
        if not verificarProdutoExiste(id_produto):
            print("O ID do produto fornecido não existe no banco de dados.")
            return

        connection = conectar_banco()
        cursor = connection.cursor()

        sql = "DELETE FROM Produto WHERE idProduto = %s"
        data = (id_produto,)

        cursor.execute(sql, data)
        connection.commit()

        cursor.close()
        connection.close()

        print("O produto com ID", id_produto, "foi excluído com sucesso.")
    
    except mysql.connector.Error as error:
        print(f"Erro ao excluir o produto: {error}")

# Função para atualizar os dados de um produto
def atualizarProduto():
    try:
        id_produto_input = input("Digite o ID do produto que deseja atualizar: ").strip()
        if not id_produto_input:
            print("O ID do produto não pode ser vazio.")
            return
        id_produto = int(id_produto_input)

        # Verificar se o idProduto existe no banco de dados
        if not verificarProdutoExiste(id_produto):
            print("O ID do produto fornecido não existe no banco de dados.")
            return

        novo_nome = input("Digite o novo nome do produto (deixe em branco para manter o mesmo): ").strip()
        novo_preco = input("Digite o novo preço do produto (deixe em branco para manter o mesmo): ").strip()
        nova_qtd_estoque = input("Digite a nova quantidade em estoque do produto (deixe em branco para manter a mesma): ").strip()
        nova_info = input("Digite as novas informações do produto (deixe em branco para manter as mesmas): ").strip()
        novo_id_categoria = input("Digite o novo ID da categoria do produto (deixe em branco para manter o mesmo): ").strip()
        novo_id_fornecedor = input("Digite o novo ID do fornecedor do produto (deixe em branco para manter o mesmo): ").strip()

        # Verificar se o novo ID da categoria existe na tabela Categoria
        if novo_id_categoria and not verificarCategoriaExiste(novo_id_categoria):
            print("O novo ID da categoria fornecido não existe na tabela Categoria.")
            return

        # Verificar se o novo ID do fornecedor existe na tabela Fornecedor
        if novo_id_fornecedor and not verificarFornecedorExiste(novo_id_fornecedor):
            print("O novo ID do fornecedor fornecido não existe na tabela Fornecedor.")
            return

        connection = conectar_banco()
        cursor = connection.cursor()

        # Construir a consulta SQL e os dados a serem atualizados
        sql = "UPDATE Produto SET"
        data = []

        if novo_nome:
            sql += " nomeProduto = %s,"
            data.append(novo_nome)
        if novo_preco:
            sql += " valorProduto = %s,"
            data.append(float(novo_preco))
        if nova_qtd_estoque:
            sql += " qtdEstoque = %s,"
            data.append(int(nova_qtd_estoque))
        if nova_info:
            sql += " infoProduto = %s,"
            data.append(nova_info)
        if novo_id_categoria:
            sql += " idCategoria = %s,"
            data.append(int(novo_id_categoria))
        if novo_id_fornecedor:
            sql += " idFornecedor = %s,"
            data.append(int(novo_id_fornecedor))

        # Remover a última vírgula da consulta SQL
        sql = sql.rstrip(',')

        # Adicionar a cláusula WHERE
        sql += " WHERE idProduto = %s"
        data.append(id_produto)

        # Executar a consulta SQL
        cursor.execute(sql, data)
        connection.commit()

        cursor.close()
        connection.close()

        print("Os dados do produto com ID", id_produto, "foram atualizados com sucesso.")
    
    except mysql.connector.Error as error:
        print(f"Erro ao atualizar o produto: {error}")

# Função para consultar um produto
def consultarProduto():
    try:
        id_produto_input = input("Digite o ID do produto que deseja consultar: ").strip()
        if not id_produto_input:
            print("O ID do produto não pode ser vazio.")
            return
        id_produto = int(id_produto_input)

        # Verificar se o idProduto existe no banco de dados
        if not verificarProdutoExiste(id_produto):
            print("O ID do produto fornecido não existe no banco de dados.")
            return

        connection = conectar_banco()
        cursor = connection.cursor()

        # Consulta SQL para obter as informações do produto com o ID fornecido
        sql = """
            SELECT 
                P.nomeProduto, 
                P.valorProduto, 
                P.qtdEstoque, 
                P.infoProduto, 
                C.nomeCategoria, 
                U.nome
            FROM 
                Produto AS P
                JOIN Categoria AS C ON P.idCategoria = C.idCategoria
                JOIN Usuario AS U ON P.idFornecedor = U.idUsuario
            WHERE 
                P.idProduto = %s
        """
        cursor.execute(sql, (id_produto,))
        produto = cursor.fetchone()

        cursor.close()
        connection.close()

        if produto:
            nome_produto, preco_produto, qtd_estoque, info_produto, nome_categoria, nome_fornecedor = produto
            print("Nome do Produto:", nome_produto)
            print("Preço do Produto:", preco_produto)
            print("Quantidade em Estoque:", qtd_estoque)
            print("Informações do Produto:", info_produto)
            print("Categoria:", nome_categoria)
            print("Fornecedor:", nome_fornecedor)
        else:
            print("Não foi possível encontrar informações para o produto com ID", id_produto)
    
    except mysql.connector.Error as error:
        print(f"Erro ao consultar o produto: {error}")
