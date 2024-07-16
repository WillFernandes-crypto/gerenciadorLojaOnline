import mysql.connector
from datetime import datetime

def conectar_banco():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="LojaOnlinev2"
    )

def obter_tipo_pagamento():
    while True:
        print("Escolha o tipo de pagamento:")
        print("1 - débito")
        print("2 - crédito")
        print("3 - boleto")
        print("4 - pix")
        opcao = input("Digite o número correspondente: ")
        if opcao in ['1', '2', '3', '4']:
            if opcao == '1':
                return 'debito'
            elif opcao == '2':
                return 'credito'
            elif opcao == '3':
                return 'boleto'
            elif opcao == '4':
                return 'pix'
        else:
            print("Opção inválida. Por favor, digite 1, 2, 3 ou 4.")

def verificar_pagamento_existente(idPedido):
    try:
        connection = conectar_banco()
        if connection.is_connected():
            cursor = connection.cursor()

            cursor.execute("SELECT COUNT(*) FROM Pagamento WHERE idPedido = %s", (idPedido,))
            count = cursor.fetchone()[0]
            return count > 0

    except mysql.connector.Error as error:
        print(f"Erro ao verificar pagamento existente: {error}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def verificar_pagamento_finalizado(idPedido):
    try:
        connection = conectar_banco()
        if connection.is_connected():
            cursor = connection.cursor()

            cursor.execute("SELECT statusPagamento FROM Pagamento WHERE idPedido = %s", (idPedido,))
            statusPagamento = cursor.fetchone()

            if statusPagamento:
                return statusPagamento[0] == 'FINALIZADO'
            else:
                return False

    except mysql.connector.Error as error:
        print(f"Erro ao verificar pagamento finalizado: {error}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def computarPagamento():
    try:
        connection = conectar_banco()
        if connection.is_connected():
            cursor = connection.cursor()

            idPedido = int(input("Digite o ID do pedido: "))

            if verificar_pagamento_existente(idPedido):
                print("O pagamento para este pedido já foi computado.")
                return

            if verificar_pagamento_finalizado(idPedido):
                print("O pagamento para este pedido já foi finalizado.")
                return

            cursor.execute("SELECT statusPedido FROM Pedido WHERE idPedido = %s", (idPedido,))
            statusPedido = cursor.fetchone()

            if not statusPedido:
                print("O pedido não existe.")
                return
            elif statusPedido[0] != 'ATIVO':
                print("O pedido já foi finalizado.")
                return

            cursor.execute("SELECT SUM(valorProduto * qtdEscolhida) FROM ProdutosPedidos JOIN Produto ON ProdutosPedidos.idProduto = Produto.idProduto WHERE idPedido = %s", (idPedido,))
            valorTotal = cursor.fetchone()[0]

            tipoPagamento = obter_tipo_pagamento()

            dataAtual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            statusPagamento = 'ATIVO'
            cursor.execute("INSERT INTO Pagamento (idPedido, valorTotal, dataPagamento, formaPagamento, statusPagamento) VALUES (%s, %s, %s, %s, %s)", (idPedido, valorTotal, dataAtual, tipoPagamento, statusPagamento))
            connection.commit()
            print("Pagamento computado com sucesso!")

    except mysql.connector.Error as error:
        print(f"Erro ao computar pagamento: {error}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def finalizarPagamento():
    try:
        connection = conectar_banco()
        if connection.is_connected():
            cursor = connection.cursor()

            idPagamento = int(input("Digite o ID do pagamento: "))

            cursor.execute("SELECT statusPagamento, idPedido FROM Pagamento WHERE idPagamento = %s", (idPagamento,))
            pagamento_info = cursor.fetchone()

            if not pagamento_info:
                print("O pagamento não existe.")
                return
            elif pagamento_info[0] == 'FINALIZADO':
                print("O pagamento já foi finalizado.")
                return

            idPedido = pagamento_info[1]

            if verificar_pagamento_finalizado(idPedido):
                print("O pagamento para este pedido já foi finalizado.")
                return

            cursor.execute("UPDATE Pedido SET statusPedido = 'FINALIZADO' WHERE idPedido = %s", (idPedido,))
            cursor.execute("UPDATE Pagamento SET statusPagamento = 'FINALIZADO' WHERE idPagamento = %s", (idPagamento,))
            
            connection.commit()
            print("Pagamento finalizado com sucesso!")

    except mysql.connector.Error as error:
        print(f"Erro ao finalizar pagamento: {error}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
