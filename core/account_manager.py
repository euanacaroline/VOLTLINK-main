from database.db_handler import db_singleton

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