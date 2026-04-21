import sys
import os
import time

# Garante que o Python sempre encontre a pasta VOLTLINK, independente de onde o terminal foi aberto
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import db_handler
from ui import terminal_menu
from ui import logo_VoltLink

def main():
    """Função principal que inicia a aplicação."""
    # 1. Garante que o banco de dados e as tabelas existam.
    db_handler.create_tables()

    # 2. Exibe a animação de inicialização.
    logo_VoltLink.run_animation(show_cursor=False)
    time.sleep(2) # Pausa para o usuário ver o logo.

    # 3. Inicia a interface do usuário.
    terminal_menu.show_main_menu()

    # 4. Ao sair do menu, fecha a conexão com o banco de dados.
    db_handler.db_singleton.close_connection()

if __name__ == "__main__":
    main()