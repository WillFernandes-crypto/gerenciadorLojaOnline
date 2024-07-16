import mysql.connector

# Função para conectar ao banco de dados
def conectar_banco():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="LojaOnlinev2"
    )

# Função para cadastrar novos usuários
def inserirUsuario():
    nome = input("Digite o nome do novo usuário: ")
    if not nome:
        print("O nome do usuário não pode ser vazio.")
        return
    cpf = input("Digite o CPF do novo usuário: ")
    if not cpf:
        print("O CPF do usuário não pode ser vazio.")
        return
    telefone = input("Digite o telefone do novo usuário: ")
    if not telefone:
        print("O telefone do usuário não pode ser vazio.")
        return
    tipo_usuario_input = input("Digite o tipo de usuário (1 para cliente, 2 para fornecedor): ")
    if tipo_usuario_input not in ('1', '2'):
        print("Opção inválida. Digite 1 para cliente ou 2 para fornecedor.")
        return
    email = input("Digite o email do novo usuário: ")
    if not email:
        print("O email do usuário não pode ser vazio.")
        return

    tipo_usuario = "CLI" if tipo_usuario_input == '1' else "FOR"

    connection = conectar_banco()
    cursor = connection.cursor()

    sql = "INSERT INTO Usuario (nome, tipoUsuario, cpf, telefone, email) VALUES (%s, %s, %s, %s, %s)"
    data = (nome, tipo_usuario, cpf, telefone, email)

    cursor.execute(sql, data)
    connection.commit()

    userid = cursor.lastrowid

    # Verifica o tipo de usuário e insere na tabela correspondente
    if tipo_usuario_input == '1':
        end_entrega = input("Digite o endereço de entrega do cliente: ")
        if not end_entrega:
            print("O endereço de entrega não pode ser vazio.")
            return

        sql_cliente = "INSERT INTO Cliente (idCliente, endEntrega, tipoUsuario) VALUES (%s, %s, %s)"
        data_cliente = (userid, end_entrega, tipo_usuario)
        cursor.execute(sql_cliente, data_cliente)
        connection.commit()
    elif tipo_usuario_input == '2':
        cnpj = input("Digite o CNPJ do fornecedor: ")
        if not cnpj:
            print("O CNPJ do fornecedor não pode ser vazio.")
            return
        elif len(cnpj) > 14:
            print("O CNPJ do fornecedor não pode exceder 14 caracteres.")
            return

        sql_fornecedor = "INSERT INTO Fornecedor (idFornecedor, cnpj, tipoUsuario) VALUES (%s, %s, %s)"
        data_fornecedor = (userid, cnpj, tipo_usuario)
        cursor.execute(sql_fornecedor, data_fornecedor)
        connection.commit()

    cursor.close()
    connection.close()

    print("Foi cadastrado o novo usuário de ID:", userid)




# Função para atualizar informações dos usuários
def atualizarUsuario():
    user_id = input("Digite o ID do usuário que deseja atualizar: ")
    if not user_id:
        print("O ID do usuário não pode ser vazio.")
        return
    novo_nome = input("Digite o novo nome do usuário: ")
    novo_cpf = input("Digite o novo CPF do usuário: ")
    novo_telefone = input("Digite o novo telefone do usuário: ")
    novo_email = input("Digite o novo email do usuário: ")

    connection = conectar_banco()
    cursor = connection.cursor()

    sql = "UPDATE Usuario SET"
    data = []

    if novo_nome:
        sql += " nome = %s,"
        data.append(novo_nome)
    if novo_cpf:
        sql += " cpf = %s,"
        data.append(novo_cpf)
    if novo_telefone:
        sql += " telefone = %s,"
        data.append(novo_telefone)
    if novo_email:
        sql += " email = %s,"
        data.append(novo_email)

    # Remover a última vírgula da consulta SQL
    sql = sql.rstrip(',')

    # Adicionar a cláusula WHERE
    sql += " WHERE idUsuario = %s"
    data.append(user_id)

    # Executar a consulta SQL
    cursor.execute(sql, data)
    connection.commit()

    cursor.close()
    connection.close()

    print("Os dados do usuário com ID", user_id, "foram atualizados com sucesso.")

# Função para excluir um usuário
def excluirUsuario():
    user_id = input("Digite o ID do usuário que deseja excluir: ")
    if not user_id:
        print("O ID do usuário não pode ser vazio.")
        return

    connection = conectar_banco()
    cursor = connection.cursor()

    try:
        # Excluir primeiro os registros dependentes na tabela Fornecedor
        sql_fornecedor = "DELETE FROM Fornecedor WHERE idFornecedor = %s"
        cursor.execute(sql_fornecedor, (user_id,))
        connection.commit()

        # Em seguida, excluir o usuário da tabela Usuario
        sql_usuario = "DELETE FROM Usuario WHERE idUsuario = %s"
        cursor.execute(sql_usuario, (user_id,))
        connection.commit()

        print("O usuário com ID", user_id, "foi excluído com sucesso.")
    except mysql.connector.Error as err:
        print("Erro ao excluir o usuário:", err)
    finally:
        cursor.close()
        connection.close()
    
# Função para consultar e exibir informações de um usuário utilizando JOIN
def consultarExibirUsuarioJoin():
    id_usuario = input("Digite o ID do usuário que deseja consultar: ")
    if not id_usuario:
        print("O ID do usuário não pode ser vazio.")
        return

    connection = conectar_banco()
    cursor = connection.cursor()

    try:
        sql = """
            SELECT U.nome, U.cpf, U.telefone, U.email, U.tipoUsuario, C.endEntrega, F.cnpj
            FROM Usuario U
            LEFT JOIN Cliente C ON U.idUsuario = C.idCliente
            LEFT JOIN Fornecedor F ON U.idUsuario = F.idFornecedor
            WHERE U.idUsuario = %s
        """
        cursor.execute(sql, (id_usuario,))
        usuario_info = cursor.fetchone()

        if usuario_info:
            print("Informações do usuário:")
            print("Nome:", usuario_info[0])
            print("CPF:", usuario_info[1])
            print("Telefone:", usuario_info[2])
            print("Email:", usuario_info[3])
            print("Tipo de usuário:", usuario_info[4])
            if usuario_info[4] == 'CLI':
                print("Endereço de Entrega:", usuario_info[5])
            elif usuario_info[4] == 'FOR':
                print("CNPJ:", usuario_info[6])
        else:
            print("Usuário não encontrado.")
    except mysql.connector.Error as err:
        print("Erro ao consultar o usuário:", err)
    finally:
        cursor.close()
        connection.close()


# Função para consultar e exibir informações de um usuário utilizando subconsulta aninhada
def consultarExibirUsuarioSubconsulta():
    id_usuario = input("Digite o ID do usuário que deseja consultar: ")
    if not id_usuario:
        print("O ID do usuário não pode ser vazio.")
        return

    connection = conectar_banco()
    cursor = connection.cursor()

    try:
        sql = """
            SELECT U.idUsuario, U.nome, U.cpf, U.telefone, U.email, U.tipoUsuario,
            CASE
                WHEN U.tipoUsuario = 'CLI' THEN C.endEntrega
                WHEN U.tipoUsuario = 'FOR' THEN F.cnpj
            END AS 'Informação Específica'
            FROM Usuario U
            LEFT JOIN Cliente C ON U.idUsuario = C.idCliente
            LEFT JOIN Fornecedor F ON U.idUsuario = F.idFornecedor
            WHERE U.idUsuario = %s
        """
        cursor.execute(sql, (id_usuario,))
        usuario_info = cursor.fetchone()

        if usuario_info:
            print("Informações do usuário:")
            print("ID:", usuario_info[0])
            print("Nome:", usuario_info[1])
            print("CPF:", usuario_info[2])
            print("Telefone:", usuario_info[3])
            print("Email:", usuario_info[4])
            print("Tipo de usuário:", usuario_info[5])
            print("Informação Específica:", usuario_info[6])
        else:
            print("Usuário não encontrado.")
    except mysql.connector.Error as err:
        print("Erro ao consultar o usuário:", err)
    finally:
        cursor.close()
        connection.close()
        
# Função para verificar se o ID do fornecedor existe na tabela Fornecedor
def verificarFornecedorExiste(id_fornecedor):
    connection = conectar_banco()
    cursor = connection.cursor()

    try:
        sql = "SELECT COUNT(*) FROM Fornecedor WHERE idFornecedor = %s"
        cursor.execute(sql, (id_fornecedor,))
        resultado = cursor.fetchone()[0]
        return resultado > 0
    except mysql.connector.Error as err:
        print("Erro ao verificar o fornecedor:", err)
        return False
    finally:
        cursor.close()
        connection.close()


