# -*- coding: utf-8 -*-
import mysql.connector

# Função para conectar ao banco de dados
def conectar_banco():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="LojaOnlinev2"
    )

# Função para cadastrar uma nova categoria
def cadastrarCategoria():
    nome_categoria = input("Digite o nome da nova categoria: ")
    if not nome_categoria.strip():
        print("O nome da categoria não pode ser vazio.")
        return

    info_categoria = input("Digite as informações adicionais da nova categoria: ")
    if not info_categoria.strip():
        print("As informações adicionais da categoria não podem ser vazias.")
        return

    connection = conectar_banco()
    cursor = connection.cursor()

    try:
        sql = "INSERT INTO Categoria (nomeCategoria, infoCategoria) VALUES (%s, %s)"
        data = (nome_categoria, info_categoria)

        cursor.execute(sql, data)
        connection.commit()

        categoria_id = cursor.lastrowid

        print("A nova categoria foi cadastrada com sucesso com o ID:", categoria_id)
    except mysql.connector.Error as err:
        print("Erro ao cadastrar a categoria:", err)
    finally:
        cursor.close()
        connection.close()

# Função para verificar se uma categoria existe no banco de dados
def verificarCategoriaExiste(id_categoria):
    connection = conectar_banco()
    cursor = connection.cursor()

    try:
        sql = "SELECT COUNT(*) FROM Categoria WHERE idCategoria = %s"
        cursor.execute(sql, (id_categoria,))
        resultado = cursor.fetchone()[0]

        return resultado > 0
    except mysql.connector.Error as err:
        print("Erro ao verificar a existência da categoria:", err)
    finally:
        cursor.close()
        connection.close()

# Função para excluir uma categoria
def excluirCategoria():
    id_categoria_input = input("Digite o ID da categoria que deseja excluir: ")
    if not id_categoria_input:
        print("O ID da categoria não pode ser vazio.")
        return
    id_categoria = int(id_categoria_input)

    # Verificar se o idCategoria existe no banco de dados
    if not verificarCategoriaExiste(id_categoria):
        print("O ID da categoria fornecido não existe no banco de dados.")
        return

    connection = conectar_banco()
    cursor = connection.cursor()

    try:
        sql = "DELETE FROM Categoria WHERE idCategoria = %s"
        cursor.execute(sql, (id_categoria,))
        connection.commit()

        print("A categoria com ID", id_categoria, "foi excluída com sucesso.")
    except mysql.connector.Error as err:
        print("Erro ao excluir a categoria:", err)
    finally:
        cursor.close()
        connection.close()

# Função para atualizar os dados de uma categoria
def atualizarCategoria():
    id_categoria_input = input("Digite o ID da categoria que deseja atualizar: ")
    if not id_categoria_input:
        print("O ID da categoria não pode ser vazio.")
        return
    id_categoria = int(id_categoria_input)

    # Verificar se o idCategoria existe no banco de dados
    if not verificarCategoriaExiste(id_categoria):
        print("O ID da categoria fornecido não existe no banco de dados.")
        return

    novo_nome = input("Digite o novo nome da categoria (deixe em branco para manter o mesmo): ")
    nova_info = input("Digite as novas informações da categoria (deixe em branco para manter as mesmas): ")

    connection = conectar_banco()
    cursor = connection.cursor()

    try:
        sql = "UPDATE Categoria SET"
        data = []

        if novo_nome.strip():
            sql += " nomeCategoria = %s,"
            data.append(novo_nome)
        if nova_info.strip():
            sql += " infoCategoria = %s,"
            data.append(nova_info)

        # Remover a última vírgula da consulta SQL
        sql = sql.rstrip(',')

        # Adicionar a cláusula WHERE
        sql += " WHERE idCategoria = %s"
        data.append(id_categoria)

        # Executar a consulta SQL
        cursor.execute(sql, data)
        connection.commit()

        print("Os dados da categoria com ID", id_categoria, "foram atualizados com sucesso.")
    except mysql.connector.Error as err:
        print("Erro ao atualizar a categoria:", err)
    finally:
        cursor.close()
        connection.close()

# Função para consultar os dados de uma categoria
def consultarCategoria():
    id_categoria_input = input("Digite o ID da categoria que deseja consultar: ")
    if not id_categoria_input:
        print("O ID da categoria não pode ser vazio.")
        return
    id_categoria = int(id_categoria_input)

    # Verificar se o idCategoria existe no banco de dados
    if not verificarCategoriaExiste(id_categoria):
        print("O ID da categoria fornecido não existe no banco de dados.")
        return

    connection = conectar_banco()
    cursor = connection.cursor()

    try:
        sql = "SELECT nomeCategoria, infoCategoria FROM Categoria WHERE idCategoria = %s"
        cursor.execute(sql, (id_categoria,))
        categoria = cursor.fetchone()

        if categoria:
            print("Nome da categoria:", categoria[0])
            print("Informações adicionais da categoria:", categoria[1])
        else:
            print("Não foi possível encontrar informações para a categoria com ID", id_categoria)
    except mysql.connector.Error as err:
        print("Erro ao consultar a categoria:", err)
    finally:
        cursor.close()
        connection.close()

# Menu Principal
def menu():
    while True:
        print("\nMenu Categorias:")
        print("1. Cadastrar nova categoria")
        print("2. Excluir uma categoria")
        print("3. Atualizar dados de uma categoria")
        print("4. Consultar uma categoria")
        print("5. Sair")

        opcao = input("Digite o número da opção desejada: ")

        if opcao == "1":
            cadastrarCategoria()
        elif opcao == "2":
            excluirCategoria()
        elif opcao == "3":
            atualizarCategoria()
        elif opcao == "4":
            consultarCategoria()
        elif opcao == "5":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

