# -*- coding: utf-8 -*-
import mysql.connector
from mysql.connector import Error

# Função para conectar ao banco de dados
def conectar_banco():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="LojaOnlinev2"
    )

# Função para verificar se o produto existe
def verificar_produto_existente(idProduto):
    try:
        connection = conectar_banco()

        if connection.is_connected():
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM Produto WHERE idProduto = %s", (idProduto,))
            produto = cursor.fetchone()

            if not produto:
                print("O produto com o ID especificado não foi encontrado.")
                return False
            else:
                return True

    except Error as e:
        print(f"Erro ao verificar a existência do produto: {e}")
        return False

    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

# Função para criar uma nova promoção
def criarPromocao():
    connection = None
    
    try:
        idProduto = input("Digite o ID do produto associado à promoção: ")
        if not idProduto:
            print("O ID do produto não pode estar vazio.")
            return
        elif not verificar_produto_existente(idProduto):
            return
        
        infoPromocao = input("Digite a descrição da promoção: ")
        if not infoPromocao:
            print("A descrição da promoção não pode estar vazia.")
            return
        
        desconto_str = input("Digite o desconto da promoção (em decimal, por exemplo, 0.15 para 15%): ")
        if not desconto_str:
            print("O desconto da promoção não pode estar vazio.")
            return
        desconto = float(desconto_str)

        dataInicio = input("Digite a data de início da promoção (no formato AAAA-MM-DD): ")
        if not dataInicio:
            print("A data de início da promoção não pode estar vazia.")
            return
        
        dataTermino = input("Digite a data de término da promoção (no formato AAAA-MM-DD): ")
        if not dataTermino:
            print("A data de término da promoção não pode estar vazia.")
            return

        connection = conectar_banco()

        if connection.is_connected():
            cursor = connection.cursor()

            query = """INSERT INTO Promocao (idProduto, infoPromocao, desconto, dataInicio, dataTermino)
                       VALUES (%s, %s, %s, %s, %s)"""

            cursor.execute(query, (idProduto, infoPromocao, desconto, dataInicio, dataTermino))
            connection.commit()
            print("Promoção criada com sucesso!")
            
    except Error as e:
        print(f"Erro ao criar a promoção: {e}")

    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

# Função para excluir uma promoção existente
def excluirPromocao():
    idPromocao = input("Digite o ID da promoção que deseja excluir: ")
    if not idPromocao:
        print("O campo idPromocao não pode estar vazio.")
        return

    try:
        connection = conectar_banco()

        if connection.is_connected():
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM Promocao WHERE idPromocao = %s", (idPromocao,))
            promocao = cursor.fetchone()

            if not promocao:
                print("A promoção com o ID especificado não foi encontrada.")
                return

            confirmacao = input("Tem certeza que deseja excluir a promoção? (s/n): ").lower()

            if confirmacao == 's':
                cursor.execute("DELETE FROM Promocao WHERE idPromocao = %s", (idPromocao,))
                connection.commit()
                print("Promoção excluída com sucesso!")
            else:
                print("Exclusão da promoção cancelada.")

    except Error as e:
        print(f"Erro ao excluir a promoção: {e}")

    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

# Função para atualizar uma promoção existente
def atualizarPromocao():
    idPromocao = input("Digite o ID da promoção que deseja atualizar: ")
    if not idPromocao:
        print("O campo idPromocao não pode estar vazio.")
        return

    try:
        connection = conectar_banco()

        if connection.is_connected():
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM Promocao WHERE idPromocao = %s", (idPromocao,))
            promocao = cursor.fetchone()

            if not promocao:
                print("A promoção com o ID especificado não foi encontrada.")
                return

            infoPromocao = input("Digite a nova descrição da promoção (deixe em branco para não modificar): ")
            desconto_str = input("Digite o novo desconto da promoção (em decimal, por exemplo, 0.15 para 15%, deixe em branco para não modificar): ")

            desconto = float(desconto_str) if desconto_str else None

            dataInicio = input("Digite a nova data de início da promoção (no formato AAAA-MM-DD, deixe em branco para não modificar): ")
            dataTermino = input("Digite a nova data de término da promoção (no formato AAAA-MM-DD, deixe em branco para não modificar): ")

            if infoPromocao or desconto is not None or dataInicio or dataTermino:
                query = "UPDATE Promocao SET "
                fields = []

                if infoPromocao:
                    fields.append(f"infoPromocao = '{infoPromocao}'")
                if desconto is not None:
                    fields.append(f"desconto = {desconto}")
                if dataInicio:
                    fields.append(f"dataInicio = '{dataInicio}'")
                if dataTermino:
                    fields.append(f"dataTermino = '{dataTermino}'")

                query += ", ".join(fields)
                query += f" WHERE idPromocao = {idPromocao}"

                cursor.execute(query)
                connection.commit()
                print("Promoção atualizada com sucesso!")
            else:
                print("Nenhum dado foi modificado.")

    except Error as e:
        print(f"Erro ao atualizar a promoção: {e}")

    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

# Função para consultar os detalhes de uma promoção existente
def consultarPromocao():
    idPromocao = input("Digite o ID da promoção que deseja consultar: ")
    if not idPromocao:
        print("O campo idPromocao não pode estar vazio.")
        return

    try:
        connection = conectar_banco()

        if connection.is_connected():
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM Promocao WHERE idPromocao = %s", (idPromocao,))
            promocao = cursor.fetchone()

            if not promocao:
                print("A promoção com o ID especificado não foi encontrada.")
                return

            print("Detalhes da promoção:")
            print(f"ID da promoção: {promocao[0]}")
            print(f"ID do produto associado: {promocao[1]}")
            print(f"Descrição da promoção: {promocao[2]}")
            print(f"Desconto da promoção: {promocao[3]}")
            print(f"Data de início da promoção: {promocao[4]}")
            print(f"Data de término da promoção: {promocao[5]}")

    except Error as e:
        print(f"Erro ao consultar a promoção: {e}")

    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

# Função para aplicar uma promoção a um produto
def aplicarPromocao():
    try:
        connection = conectar_banco()

        if connection.is_connected():
            cursor = connection.cursor()

            id_promocao = input("Digite o ID da promoção que deseja aplicar: ")
            if not id_promocao:
                print("O campo idPromocao não pode estar vazio.")
                return

            cursor.execute("SELECT * FROM Promocao WHERE idPromocao = %s", (id_promocao,))
            promocao = cursor.fetchone()

            if not promocao:
                print("A promoção com o ID especificado não foi encontrada.")
                return

            id_produto = promocao[1]  # ID do produto associado à promoção

            cursor.execute("SELECT * FROM Produto WHERE idProduto = %s", (id_produto,))
            produto = cursor.fetchone()

            if not produto:
                print("O produto associado à promoção não foi encontrado.")
                return

            desconto = promocao[3]

            preco_produto = produto[5]

            novo_preco = preco_produto * (1 - desconto)

            cursor.execute("UPDATE Produto SET valorProduto = %s WHERE idProduto = %s", (novo_preco, id_produto))
            connection.commit()

            print("Promoção aplicada com sucesso!")

    except Error as e:
        print(f"Erro ao aplicar a promoção: {e}")

    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
