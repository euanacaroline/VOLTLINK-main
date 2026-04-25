import sqlite3
import os

# garatir que o banco de dados seja encontrado em qualquer computador 
DB_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'voltlink.db')


# isso é para conseguir salvar diferentes informações "ao mesmo dempo" sem travar 
class Database:
    """
    Classe Singleton para gerenciar a conexão com o banco de dados SQLite.
    Garante que apenas uma conexão seja aberta durante a vida útil da aplicação.
    """
    _instance = None
    _connection = None

    def __new__(cls):
        if cls._instance is None:
            print("Criando nova instância do Singleton de banco de dados.")
            cls._instance = super(Database, cls).__new__(cls)
            try:
                # check_same_thread=False é importante para aplicações que podem ter threads,
                # mesmo que a UI de terminal seja single-threaded.
                cls._connection = sqlite3.connect(DB_FILE, check_same_thread=False)
                cls._connection.row_factory = sqlite3.Row
                print("Conexão com o banco de dados estabelecida com sucesso.")
            except sqlite3.Error as e:
                print(f"ERRO: Falha ao conectar ao banco de dados: {e}")
                cls._connection = None
        return cls._instance

    def get_connection(self):
        """Retorna a instância única da conexão com o banco de dados."""
        return self._connection

    def close_connection(self):
        """Fecha a conexão com o banco de dados, se estiver aberta."""
        if self._connection:
            self._connection.close()
            Database._connection = None
            print("Conexão com o banco de dados fechada.")

# Instância única (Singleton) que será usada em toda a aplicação.
db_singleton = Database()

def create_tables():
    """Cria as tabelas iniciais do banco de dados, se não existirem."""
    conn = db_singleton.get_connection()
    if not conn:
        print("ERRO: Não foi possível criar as tabelas pois a conexão com o banco de dados falhou.")
        return

    cursor = conn.cursor()

    # Usuários
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        phone_number TEXT NOT NULL,
        password TEXT NOT NULL,
        is_admin INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Tabela de Eletropostos (Stations)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        address TEXT NOT NULL,
        total_chargers INTEGER DEFAULT 0,
        available_chargers INTEGER DEFAULT 0,
        max_power_kw REAL DEFAULT 0.0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Tabela de Avaliações (Reviews)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        station_id INTEGER NOT NULL,
        user_name TEXT NOT NULL,
        rating INTEGER NOT NULL,
        comment TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (station_id) REFERENCES stations (id)
    );
    """)

    # Formas de Pagamento
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payment_methods (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        method_type TEXT NOT NULL,
        card_name TEXT,
        card_number TEXT,
        card_expiry TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    );
    """)


    # VEÍCULOS 
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vehicles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        model TEXT NOT NULL,
        plate TEXT NOT NULL,
        battery_capacity REAL NOT NULL,
        connector_type TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    );
    """)


    # CRIAR ADMIN PADRÃO (Se não existir)
    cursor.execute("SELECT COUNT(*) FROM users WHERE email = ?", ('admin@voltlink.com',))
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO users (name, email, phone_number, password, is_admin)
            VALUES (?, ?, ?, ?, ?)
        """, ('Administrador Master', 'admin@voltlink.com', '999999999', 'admin123', 1))
        print("✅ Usuário Admin (admin@voltlink.com) criado!")


    # POSTOS INICIAIS 
    cursor.execute("SELECT COUNT(*) FROM stations")
    if cursor.fetchone()[0] == 0:
        postos_iniciais = [
             ('Eletroposto Shopping Recife', 'Rua Padre Carapuceiro, 777, Boa Viagem', 10, 8, 50.0),
             ('Eletroposto RioMar Shopping', 'Av. Republica do Libano, 251, Pina', 12, 5, 60.0),
             ('Posto Shell - Agamenon', 'Av. Gov. Agamenon Magalhães, 3000', 6, 0, 40.0),
             ('Eletroposto Parque da Jaqueira', 'Rua do Futuro, s/n, Graças', 4, 2, 22.0)
             ]
        cursor.executemany("""
            INSERT INTO stations (name, address, total_chargers, available_chargers, max_power_kw)
            VALUES (?, ?, ?, ?, ?)
        """, postos_iniciais)
        print("Postos de teste adicionados com sucesso!")


    conn.commit()
    # A conexão não é fechada aqui, pois é gerenciada pelo Singleton.
    print("Banco de dados e tabelas verificados/criados com sucesso.")


