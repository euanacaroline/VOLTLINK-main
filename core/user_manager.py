from database.db_handler import db_singleton

def validate_registration_data(name, email, phone, password, confirm_password):
    """Valida os dados de cadastro de um novo usuário. Retorna (True, "Sucesso") ou (False, "Mensagem de Erro")."""
    if not name or not email or not phone or not password:
        return (False, "Erro: Todos os campos são obrigatórios.")
    if "@" not in email or "." not in email or " " in email:
        return (False, "Erro: E-mail inválido!")
    if not phone.isdigit() or len(phone) != 11:
        return (False, "Erro: O telefone precisa de exatamente 11 dígitos numéricos.")
    if not (4 <= len(password) <= 8):
        return (False, "Erro: A senha deve ter entre 4 a 8 caracteres.")
    if not any(char.isdigit() for char in password):
        return (False, "Erro: A senha deve conter pelo menos um número.")
    if not any(char.isupper() for char in password):
        return (False, "Erro: A senha deve conter pelo menos uma letra maiúscula.")
    if password != confirm_password:
        return (False, "Erro: As senhas não coincidem.")
    
    # Verifica se o email já existe no banco de dados
    conn = db_singleton.get_connection()
    if not conn:
        return (False, "Erro: Falha na comunicação com o banco de dados.")

    user = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
    # A conexão não é fechada aqui.
    if user:
        return (False, "Erro: Email já cadastrado!")

    return (True, "Validação bem-sucedida.")

def register_new_user(name, email, phone, password):
    """Insere um novo usuário no banco de dados."""
    conn = db_singleton.get_connection()
    if not conn:
        print("ERRO: Não foi possível registrar o usuário pois a conexão com o banco de dados falhou.")
        return

    # Define como admin se for um email específico de controle
    is_admin = 1 if email == 'admin@voltlink.com' else 0

    # Aqui você poderia também hashear a senha antes de salvar!
    conn.execute("INSERT INTO users (name, email, phone_number, password, is_admin) VALUES (?, ?, ?, ?, ?)", (name, email, phone, password, is_admin))
    conn.commit()
    # A conexão não é fechada aqui.

def login_user(email, password):
    """
    Verifica as credenciais do usuário no banco de dados.
    Retorna (True, user_data_dict) em caso de sucesso,
    ou (False, error_message) em caso de falha.
    """
    conn = db_singleton.get_connection()
    if not conn:
        return (False, "Erro: Falha na comunicação com o banco de dados.")

    # Busca o usuário pelo email
    user_row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()

    if not user_row:
        return (False, "Erro: Email não encontrado.")

    # AVISO: Comparação de senha em texto puro. Isto é muito inseguro para produção!
    # O ideal é usar hash de senhas (ex: bcrypt), que podemos implementar a seguir.
    if user_row['password'] == password:
        # Retorna os dados do usuário como um dicionário para facilitar o acesso
        return (True, dict(user_row))
    else:
        return (False, "Erro: Senha incorreta.")