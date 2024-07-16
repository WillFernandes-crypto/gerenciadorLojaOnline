# -*- coding: utf-8 -*-
import mysql.connector
from datetime import datetime
import uuid

def conectar_banco():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="LojaOnlinev2"
    )

def emitirNota():
    try:
        # Conectar ao banco de dados
        connection = conectar_banco()

        if connection.is_connected():
            cursor = connection.cursor()

            # Solicitar o idPagamento ao usuário
            idPagamento = int(input("Digite o ID do pagamento: "))

            # Verificar se o pagamento existe e está finalizado
            cursor.execute("SELECT statusPagamento FROM Pagamento WHERE idPagamento = %s", (idPagamento,))
            pagamento_status = cursor.fetchone()

            if not pagamento_status or pagamento_status[0] != 'FINALIZADO':
                print("Não é possível emitir a nota fiscal para este pagamento.")
                return

            # Recuperar as informações necessárias para a nota fiscal
            cursor.execute("""
                SELECT p.idPagamento, p.valorTotal, p.formaPagamento, pp.idPedido, u.idUsuario, u.nome, pp.dataPedido
                FROM Pagamento p
                JOIN Pedido pp ON p.idPedido = pp.idPedido
                JOIN Usuario u ON pp.idCliente = u.idUsuario
                WHERE p.idPagamento = %s
            """, (idPagamento,))
            dados_pagamento = cursor.fetchone()

            # Recuperar os produtos associados ao pedido
            cursor.execute("""
                SELECT pr.nomeProduto, pr.valorProduto, pd.qtdEscolhida
                FROM ProdutosPedidos pd
                JOIN Produto pr ON pd.idProduto = pr.idProduto
                WHERE pd.idPedido = %s
            """, (dados_pagamento[3],))
            produtos_pedido = cursor.fetchall()

            # Gerar o nome único do arquivo
            nome_arquivo = f"nota_fiscal_{uuid.uuid4()}.txt"

            # Gerar o documento txt com as informações
            with open(nome_arquivo, "w") as arquivo:
                arquivo.write(f"ID do Pagamento: {dados_pagamento[0]}\n")
                arquivo.write(f"Valor Total: {dados_pagamento[1]}\n")
                arquivo.write(f"Forma de Pagamento: {dados_pagamento[2]}\n")
                arquivo.write(f"ID do Cliente: {dados_pagamento[4]}\n")
                arquivo.write(f"Nome do Cliente: {dados_pagamento[5]}\n")
                arquivo.write(f"Data do Pedido: {dados_pagamento[6]}\n\n")
                
                arquivo.write("Produtos:\n")
                for produto in produtos_pedido:
                    arquivo.write(f"Nome do Produto: {produto[0]}\n")
                    arquivo.write(f"Preço do Produto: {produto[1]}\n")
                    arquivo.write(f"Quantidade Pedido: {produto[2]}\n\n")
                
                arquivo.write(f"Data de Emissão da Nota Fiscal: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

            # Inserir os dados na tabela NotaFiscal apenas se não houver uma nota fiscal para este pagamento
            cursor.execute("""
                INSERT INTO NotaFiscal (idPagamento, dataEmissao)
                SELECT %s, %s
                FROM dual
                WHERE NOT EXISTS (SELECT 1 FROM NotaFiscal WHERE idPagamento = %s)
            """, (idPagamento, datetime.now(), idPagamento))

            # Se a nota fiscal foi inserida, prosseguir com a atualização da tabela Entrega
            if cursor.rowcount > 0:
                # Recuperar o idNotaFiscal recém-inserido
                cursor.execute("SELECT LAST_INSERT_ID()")
                idNotaFiscal = cursor.fetchone()[0]

                # Inserir o idNotaFiscal na tabela Entrega
                cursor.execute("""
                    INSERT INTO Entrega (idNotaFiscal)
                    VALUES (%s)
                """, (idNotaFiscal,))

                connection.commit()  # Confirmar a transação

                print(f"Nota fiscal emitida com sucesso! O arquivo '{nome_arquivo}' foi salvo no seu computador.")
            else:
                print("Nota fiscal já emitida anteriormente para este pagamento.")

    except mysql.connector.Error as error:
        print(f"Erro ao emitir nota fiscal: {error}")

    finally:
        # Fechar a conexão com o banco de dados
        if connection.is_connected():
            cursor.close()
            connection.close()
