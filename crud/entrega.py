import mysql.connector
from datetime import datetime

def conectar_banco():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="LojaOnlinev2"
    )

def enviarEntrega():
    try:
        # Conectar ao banco de dados
        connection = conectar_banco()

        if connection.is_connected():
            cursor = connection.cursor()

            # Solicitar o idEntrega ao usuário
            idEntrega = int(input("Digite o ID da entrega: "))

            # Verificar se o idEntrega existe no banco de dados e não está vazio
            cursor.execute("SELECT * FROM Entrega WHERE idEntrega = %s", (idEntrega,))
            entrega = cursor.fetchone()

            if not entrega:
                print("O ID da entrega fornecido não existe.")
                return

            # Verificar se a entrega já foi recebida
            if entrega[4] == 'RECEBIDO':
                print("A entrega já foi recebida. Não é possível enviar.")
                return

            # Verificar se já existe uma entrega ENVIANDO para este idEntrega
            if entrega[4] == 'ENVIANDO':
                print("Não é possível enviar a entrega, pois já está em andamento.")
                return

            # Solicitar a data de entrega prevista ao usuário
            dataEntregaPrevista = input("Digite a data de entrega prevista (no formato YYYY-MM-DD): ")

            # Atualizar os dados na tabela Entrega
            cursor.execute("""
                UPDATE Entrega
                SET dataEntregaPrevista = %s, statusEntrega = 'ENVIANDO'
                WHERE idEntrega = %s
            """, (dataEntregaPrevista, idEntrega))

            connection.commit()  # Confirmar a transação

            print("Entrega enviada com sucesso!")

    except mysql.connector.Error as error:
        print(f"Erro ao enviar entrega: {error}")

    finally:
        # Fechar a conexão com o banco de dados
        if connection.is_connected():
            cursor.close()
            connection.close()

def receberEntrega():
    try:
        # Conectar ao banco de dados
        connection = conectar_banco()

        if connection.is_connected():
            cursor = connection.cursor()

            # Solicitar o idEntrega ao usuário
            idEntrega = int(input("Digite o ID da entrega: "))

            # Verificar se o idEntrega existe no banco de dados e não está vazio
            cursor.execute("SELECT * FROM Entrega WHERE idEntrega = %s", (idEntrega,))
            entrega = cursor.fetchone()

            if not entrega:
                print("O ID da entrega fornecido não existe.")
                return

            # Verificar se a entrega já foi recebida
            if entrega[4] == 'RECEBIDO':
                print("A entrega já foi recebida.")
                return

            # Atualizar os dados na tabela Entrega
            dataEntregaReal = datetime.now().strftime('%Y-%m-%d')
            cursor.execute("""
                UPDATE Entrega
                SET dataEntregaReal = %s, statusEntrega = 'RECEBIDO'
                WHERE idEntrega = %s
            """, (dataEntregaReal, idEntrega))

            connection.commit()  # Confirmar a transação

            print("Entrega recebida com sucesso!")

    except mysql.connector.Error as error:
        print(f"Erro ao receber entrega: {error}")

    finally:
        # Fechar a conexão com o banco de dados
        if connection.is_connected():
            cursor.close()
            connection.close()
