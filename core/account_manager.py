import os
from database.db_handler import db_singleton

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def buscar_dados_completos_usuario(usuario_id):
    """Busca todos os detalhes do usuário, veículos e cartões."""
    conn = db_singleton.get_connection()
    
    veiculos = conn.execute("SELECT * FROM vehicles WHERE user_id = ?", (usuario_id,)).fetchall()
    
    cartoes = conn.execute("SELECT * FROM cards WHERE user_id = ?", (usuario_id,)).fetchall()
    
    return {
        "veiculos": veiculos,
        "cartoes": cartoes
        # "historico": historico
    }


def mostrar_minha_conta(usuario):
    while True:
        limpar_tela()
        conn = db_singleton.get_connection()
        
        # Atualizar dados 
        user_db = conn.execute("SELECT * FROM users WHERE id = ?", (usuario['id'],)).fetchone()
        
        # Contar veículos 
        qtd_veiculos = conn.execute("SELECT COUNT(*) as total FROM vehicles WHERE user_id = ?", (usuario['id'],)).fetchone()['total']

        print(f"👤   MINHA CONTA | VOLTLINK   ")
        print(f"------------------------------")
        print(f"Nome: {user_db['name']}")
        print(f"E-mail: {user_db['email']}")
        print(f"Telefone: {user_db['phone_number']}")
        print(f"Veículos Cadastrados: {qtd_veiculos}")
        print(f"------------------------------")
        print("1. Editar Nome/Telefone")
        print("2. Alterar Senha")
        print("3. EXCLUIR MINHA CONTA")
        print("4. Voltar")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            novo_nome = input("Novo Nome (deixe vazio para não alterar): ").strip() or user_db['name']
            novo_tel = input("Novo Telefone (deixe vazio para não alterar): ").strip() or user_db['phone_number']
            
            conn.execute("UPDATE users SET name = ?, phone_number = ? WHERE id = ?", (novo_nome, novo_tel, usuario['id']))
            conn.commit()
            print("\n✅ Dados atualizados!")
            input("Enter para continuar...")

        elif opcao == "2":
            nova_senha = input("Digite a nova senha (4-8 caracteres): ").strip()
            if 4 <= len(nova_senha) <= 8:
                conn.execute("UPDATE users SET password = ? WHERE id = ?", (nova_senha, usuario['id']))
                conn.commit()
                print("\n✅ Senha alterada!")
            else:
                print("\n❌ Senha inválida.")
            input("Enter...")

        elif opcao == "3":
            confirmar = input("⚠️ TEM CERTEZA? Isso apagará todos os seus dados. (S/N): ").upper()
            if confirmar == 'S':
                conn.execute("DELETE FROM users WHERE id = ?", (usuario['id'],))
                conn.commit()
                print("\nConta excluída. Sentiremos sua falta!")
                input("Enter para sair...")
                return "SAIR" # Sinalizamos que o usuário não existe mais

        elif opcao == "4":
            break
