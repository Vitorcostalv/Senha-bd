import sqlite3
import random
import string
import hashlib
import time

# Configuração do banco de dados
conn = sqlite3.connect('senhas.db')
cursor = conn.cursor()

# Criação das tabelas no banco de dados
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS administradores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS lixo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL,
    data_remocao TIMESTAMP NOT NULL
)
''')
conn.commit()

# Função para criptografar senhas
def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

# Função para gerar uma senha aleatória
def gerar_senha(tamanho=12):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    senha = ''.join(random.choice(caracteres) for _ in range(tamanho))
    return senha

# Função para registrar o administrador inicial
def registrar_administrador_inicial():
    admin_login = "adm"
    admin_senha = "adm123"
    senha_hash = hash_senha(admin_senha)
    try:
        cursor.execute('INSERT INTO administradores (login, senha) VALUES (?, ?)', (admin_login, senha_hash))
        conn.commit()
    except sqlite3.IntegrityError:
        pass

# Função para autenticar administrador
def autenticar_administrador(login, senha):
    senha_hash = hash_senha(senha)
    cursor.execute('SELECT * FROM administradores WHERE login = ? AND senha = ?', (login, senha_hash))
    return cursor.fetchone() is not None

# Função para registrar um novo administrador
def registrar_novo_administrador(admin_login, admin_senha):
    if autenticar_administrador(admin_login, admin_senha):
        cursor.execute('SELECT COUNT(*) FROM administradores')
        total_admins = cursor.fetchone()[0]
        if total_admins >= 3:
            print("O limite de 3 administradores já foi alcançado.")
            return
        
        novo_login = input("Digite o login do novo administrador: ")
        nova_senha = input("Digite a senha do novo administrador (máximo 12 caracteres): ")
        if len(nova_senha) > 12:
            print("Erro: A senha deve ter no máximo 12 caracteres.")
            return
        
        senha_hash = hash_senha(nova_senha)
        try:
            cursor.execute('INSERT INTO administradores (login, senha) VALUES (?, ?)', (novo_login, senha_hash))
            conn.commit()
            print(f"Novo administrador {novo_login} registrado com sucesso.")
            print("Cuidado para não perder sua senha, pois ela não pode ser redefinida.")
        except sqlite3.IntegrityError:
            print("Erro: Este login já está registrado.")
    else:
        print("Autenticação falhou. Apenas administradores podem registrar novos administradores.")

# Função para registrar novo usuário
def registrar_usuario(login, senha=None):
    if senha is None:
        senha = gerar_senha()
    if len(senha) > 12:
        print("Erro: A senha deve ter no máximo 12 caracteres.")
        return
    
    try:
        cursor.execute('INSERT INTO usuarios (login, senha) VALUES (?, ?)', (login, senha))
        conn.commit()
        print(f"Usuário registrado com sucesso!\nLogin: {login}\nSenha: {senha}")
    except sqlite3.IntegrityError:
        print("Erro: Este login já está registrado.")

# Função para listar minha senha
def listar_minha_senha(login):
    cursor.execute('SELECT login, senha FROM usuarios WHERE login = ?', (login,))
    usuario = cursor.fetchone()
    if usuario:
        print(f"Login: {usuario[0]}\nSenha: {usuario[1]}")
    else:
        print("\n-------------------------")
        print("Login não encontrado.")
        print("\n-------------------------")
# Funções de administrador (apenas após autenticação inicial)
def listar_usuarios():
    cursor.execute('SELECT login FROM usuarios')
    usuarios = cursor.fetchall()
    if usuarios:
        print("\n--- Usuários Cadastrados ---")
        for login in usuarios:
            print(f"Login: {login[0]}")
    else:
        print("Nenhum usuário encontrado.")

def excluir_usuario(login):
    cursor.execute('SELECT * FROM usuarios WHERE login = ?', (login,))
    usuario = cursor.fetchone()
    if usuario:
        cursor.execute('DELETE FROM usuarios WHERE login = ?', (login,))
        cursor.execute('INSERT INTO lixo (login, senha, data_remocao) VALUES (?, ?, ?)',
                       (usuario[1], usuario[2], time.time()))
        conn.commit()
        print(f"Usuário {login} removido.\nCaso queira, pode restaurar em até 3 dias. Caso contrário, será excluído permanentemente.")
    else:
        print("Usuário não encontrado.")

def restaurar_usuario(login):
    cursor.execute('SELECT * FROM lixo WHERE login = ?', (login,))
    usuario = cursor.fetchone()
    if usuario:
        tempo_remocao = usuario[3]
        if time.time() - tempo_remocao <= 259200:  # 3 dias em segundos
            cursor.execute('DELETE FROM lixo WHERE login = ?', (login,))
            cursor.execute('INSERT INTO usuarios (login, senha) VALUES (?, ?)', (usuario[1], usuario[2]))
            conn.commit()
            print(f"Usuário {login} restaurado com sucesso.")
        else:
            print("O período de restauração de 3 dias expirou. O usuário foi excluído permanentemente.")
    else:
        print("Usuário não encontrado na tabela de lixo.")

# Registrar administrador inicial
registrar_administrador_inicial()

# Tela inicial
def tela_inicial():
    while True:
       
        print("\n--- Gerenciador de Senhas ---")
        print("1. Registrar")
        print("2. Administrador")
        print("3. Sair")
        escolha = input("Escolha uma opção: ")


        if escolha == "1":
            print("\n-------------------------")
            print("\n--- Registrar ---")
            print("1. Registrar novo usuário (senha aleatória)")
            print("2. Registrar novo usuário (senha manual)")
            print("3. Listar minha senha")
            print("4. Sair")
            opcao = input("Escolha uma opção: ")
            print("\n-------------------------")

            if opcao == "1":
                login = input("Digite o login do novo usuário: ")
                registrar_usuario(login)
            elif opcao == "2":
                login = input("Digite o login do novo usuário: ")
                senha = input("Digite a senha (máximo 12 caracteres): ")
                registrar_usuario(login, senha)
            elif opcao == "3":
                login = input("Digite seu login: ")
                listar_minha_senha(login)
            elif opcao == "4":
                continue
            else:
                print("Opção inválida.")
        
        elif escolha == "2":
            print("\n-------------------------")
            login = input("Digite o login do administrador: ")
            senha = input("Digite a senha do administrador: ")
            if autenticar_administrador(login, senha):
                while True:
                    print("\n-------------------------")
                    print("\n--- Administrador ---")
                    print("1. Listar usuários cadastrados")
                    print("2. Excluir usuário")
                    print("3. Restaurar usuário")
                    print("4. Registrar novo administrador (adm/new)")
                    print("5. Sair")
                    opcao = input("Escolha uma opção: ")
                    print("\n--------------------------")

                    if opcao == "1":
                        listar_usuarios()
                    elif opcao == "2":
                        usuario_login = input("Digite o login do usuário a ser excluído: ")
                        excluir_usuario(usuario_login)
                    elif opcao == "3":
                        usuario_login = input("Digite o login do usuário a ser restaurado: ")
                        restaurar_usuario(usuario_login)
                    elif opcao == "4":
                        registrar_novo_administrador(login, senha)
                    elif opcao == "5":
                        break
                    else:
                        print("Opção inválida.")
            else:
                print("Credenciais inválidas.")
        
        elif escolha == "3":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

# Executar tela inicial
tela_inicial()

# Fechar conexão com o banco
conn.close()
