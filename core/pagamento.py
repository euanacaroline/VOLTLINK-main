import os
import time
from database.db_handler import db_singleton

def limpar_tela(): 
    os.system('cls' if os.name == 'nt' else 'clear')

def cadastrar_cartao(user_id, tipo_metodo): 
    print(f"\n    CADASTRO DE NOVO CARTÃO  ({tipo_metodo.upper()})   ")
    """Valida e salva um novo cartão no banco de dados."""

    nome_titular = input("Nome do Titular (como no cartão): ").strip().upper()
    if not nome_titular: 
        print(" Erro: O nome não pode estar vazio. ")
        return None

    numero_cartao = input("Número do cartão (16 dígitos):  ").replace(" ", " ") 
    if len(numero_cartao) != 16 or not numero_cartao.isdigit():
        print(" Erro: Cartão inválido! Digite os 16 números. ")
        return None 
    
    validade = input("Validade (MM/AA): ").strip()
    if "/" not in validade or len(validade) != 5: 
        print(" Erro:: Formato de validade inválido (use MM/AA).")
        return None 
    
    cvv = input("CVV (3 dígitos): ").strip()
    if len(cvv) != 3 or not cvv.isdigit():
        print(" Erro: CVV inválido!")
        return None 
    
    sucesso = cadastrar_cartao_no_banco(user_id, tipo_metodo, nome_titular, numero_cartao, validade)
    if sucesso: 
        print("\n ✅ Cartão salvo no banco de dados!")
    else: 
        print("n\ Erro ao salvar. ")


def cadastrar_cartao_no_banco(user_id, tipo_metodo, nome_titular, numero_cartao, validade): 
    conn = db_singleton.get_connection()
    if not conn: return (False, "Erro de conexão")

    final_cartao = "**** **** ****" + numero_cartao[-4:]
    try: 
        conn.execute('''
            INSERT INTO payment_methods (user_id, method_type, card_name, card_number, card_expiry)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, tipo_metodo, nome_titular, final_cartao, validade))
        conn.commit()
        return True 
    except Exception as e: 
        print(f"Erro: {e}")
        return False
  

def buscar_cartoes_usuario(id_usuario):
    """Busca no banco todos os cartões que pertencem ao usuário logado"""
    conn = db_singleton.get_connection()
    if not conn: return []
    return conn.execute("SELECT * FROM payment_methods WHERE user_id = ?", (id_usuario,)).fetchall()  #comando SELECT traz informações da tabela 

def excluir_cartao_banco(id_usuario, id_cartao):
    """Remove uma forma de pagamento."""
    conn = db_singleton.get_connection()
    try:
        '''Garante que o usuário apague um cartão que seja dele'''
        conn.execute("DELETE FROM payment_methods WHERE id = ? AND user_id = ?", (id_cartao, id_usuario))
        conn.commit()
        return (True, "Cartão removido com sucesso!")
    except Exception as e:
        return (False, f"Erro ao remover: {e}")

def atualizar_dados_cartao(id_usuario, id_cartao, nome_titular, numero_cartao, validade, cvv):
    """Edita os dados de um cartão cadastrado."""
    if not nome_titular:
        return (False, "Erro: O nome não pode estar vazio.")
    if len(numero_cartao) != 16 or not numero_cartao.isdigit():
        return (False, "Erro: Cartão inválido! Digite os 16 números.")
    if "/" not in validade or len(validade) != 5:
        return (False, "Erro: Formato de validade inválido (use MM/AA).")
    if len(cvv) != 3 or not cvv.isdigit():
        return (False, "Erro: CVV inválido!")

    conn = db_singleton.get_connection()
    final_cartao = "**** **** **** " + numero_cartao[-4:]
    try:
        '''Alterar dados nas colunas do banco de dados '''
        conn.execute("UPDATE payment_methods SET card_name = ?, card_number = ?, card_expiry = ? WHERE id = ? AND user_id = ?", (nome_titular, final_cartao, validade, id_cartao, id_usuario))
        conn.commit()
        return (True, "Cartão atualizado com sucesso!")
    except Exception as e:
        return (False, f"Erro ao atualizar: {e}")