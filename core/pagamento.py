from database.db_handler import db_singleton

def add_card(user_id, method_type, card_name, card_number, card_expiry, cvv):
    """Valida e salva um novo cartão no banco de dados."""
    if not card_name:
        return (False, "Erro: O nome não pode estar vazio.")
    if len(card_number) != 16 or not card_number.isdigit():
        return (False, "Erro: Cartão inválido! Digite os 16 números.")
    if "/" not in card_expiry or len(card_expiry) != 5:
        return (False, "Erro: Formato de validade inválido (use MM/AA).")
    if len(cvv) != 3 or not cvv.isdigit():
        return (False, "Erro: CVV inválido!")

    conn = db_singleton.get_connection()
    if not conn: return (False, "Erro de banco de dados.")

    # Por segurança, guardamos apenas os 4 últimos dígitos do cartão
    masked_number = "**** **** **** " + card_number[-4:]

    try:
        conn.execute("INSERT INTO payment_methods (user_id, method_type, card_name, card_number, card_expiry) VALUES (?, ?, ?, ?, ?)",
                     (user_id, method_type, card_name, masked_number, card_expiry))
        conn.commit()
        return (True, f"Cartão de {method_type} cadastrado com sucesso!")
    except Exception as e:
        return (False, f"Erro ao salvar cartão: {e}")

def get_payment_methods(user_id):
    """Retorna todas as formas de pagamento de um usuário."""
    conn = db_singleton.get_connection()
    if not conn: return []
    return conn.execute("SELECT * FROM payment_methods WHERE user_id = ?", (user_id,)).fetchall()

def delete_payment_method(user_id, method_id):
    """Remove uma forma de pagamento."""
    conn = db_singleton.get_connection()
    try:
        conn.execute("DELETE FROM payment_methods WHERE id = ? AND user_id = ?", (method_id, user_id))
        conn.commit()
        return (True, "Forma de pagamento removida com sucesso!")
    except Exception as e:
        return (False, f"Erro ao remover: {e}")

def update_card(user_id, method_id, card_name, card_number, card_expiry, cvv):
    """Edita os dados de um cartão cadastrado."""
    if not card_name:
        return (False, "Erro: O nome não pode estar vazio.")
    if len(card_number) != 16 or not card_number.isdigit():
        return (False, "Erro: Cartão inválido! Digite os 16 números.")
    if "/" not in card_expiry or len(card_expiry) != 5:
        return (False, "Erro: Formato de validade inválido (use MM/AA).")
    if len(cvv) != 3 or not cvv.isdigit():
        return (False, "Erro: CVV inválido!")

    conn = db_singleton.get_connection()
    masked_number = "**** **** **** " + card_number[-4:]
    try:
        conn.execute("UPDATE payment_methods SET card_name = ?, card_number = ?, card_expiry = ? WHERE id = ? AND user_id = ?", (card_name, masked_number, card_expiry, method_id, user_id))
        conn.commit()
        return (True, "Cartão atualizado com sucesso!")
    except Exception as e:
        return (False, f"Erro ao atualizar: {e}")