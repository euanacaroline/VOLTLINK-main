import os 
from database.db_handler import db_singleton
from core.pagamento import cadastrar_cartao, buscar_cartoes_usuario
from core.station_manager import buscar_postos_proximos, enviar_avaliacao, criar_link_mapa, avaliar_posto_interface
from core.checkin import fazer_checkin

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu_entrada():
    '''Mostra as opções que usuario tem assim que entra no app'''
    while True:
        limpar_tela()
        print("⚡ BEM-VINDO AO VOLTLINK ⚡")
        print("1. Login")
        print("2. Cadastro")
        print("3, Esqueci minha senha")
        print("4. Sair")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == "1":
            tela_login()
        elif opcao == "2":
            tela_cadastro()
        elif opcao == "3":
            recuperar_senha()
        elif opcao == "4":
            print("\nObrigado por usar o VoltLink! Saindo...")
            break 
        else:
            print("\n Opção inválida! Tente novamente.")
            input("Aperte Enter para continuar...")


def tela_cadastro(): 
    limpar_tela()
    print("⚡   CADASTRO VOLTLINK   ⚡")

    nome = input("Digite seu nome completo: ").strip()

    while True:
        email = input("Digite seu email:  ").strip().lower()
        if not email: 
             print(" Erro: O campo e-mail não pode estar vazio.")
        elif "@" not in email or "." not in email or " " in email:
             print(" Erro: E-mail inválido! Certifique-se de que não há espaços e que possui '@' e '.'")
        elif "ufrpe" not in email and "gmail" not in email:
             print( " Erro: Aceitamos apenas email da UFRPE ou Gmail.")
        elif not (email.endswith(".com") or email.endswith(".br")):
             print(" Erro: O e-mail deve terminar em .com ou .br")
        else: 
             email_cadastrado = email
             print(f" Email {email_cadastrado} validado!")
             break 
        # Conecta ao banco para ver se o email já existe
        conn = db_singleton.get_connection()
        existe = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
        if existe:
            print("❌ Erro: Este e-mail já está cadastrado!")
        else:
            break

    while True:
        tel = input("Digite seu telefone (11 dígitos): ").strip()
        if not tel.isdigit():
            print(" Erro: Digite apenas números.")
        elif len(tel) != 11:
            print(" Erro: O telefone precisa de exatamente 11 dígitos.")
        else:
            numero_contato = tel
            break 
    
    while True:
        senha = input("Crie uma senha (4-8 caracteres, 1 numero, 1 maiuscula): ").strip()
        if not (4 <= len(senha) <= 8):
            print("Erro: A senha deve ter entre 4 a 8 caraceres.")
            continue
        if not any(char.isdigit() for char in senha):
            print("Erro: A senha deve conter pelo menos um número.")
            continue 
        if not any(char.isupper() for char in senha):
            print("Erro: A senha deve conter pelo menos uma letra maiúscula. ")
            continue

    
        confirmacao = input("Confirme sua senha: ").strip()
        if senha == confirmacao:
            break
        else:
             print(" Erro: As senhas não coincidem. Tente novamente.")
    try: 
        ''' Salva a senha no banco de dados. '''
        conn = db_singleton.get_connection()
        conn.execute("INSERT INTO users (name, email, phone_number, password, is_admin) VALUES (?, ?, ?, ?, ?)", 
                     (nome, email, tel, senha, 0))
        conn.commit()
        print("Cadastro realizado com sucesso!")
    except Exception as e: 
        print(f"Erro ao salvar: {e}")

    input("\nPressione Enter para voltar ao menu...")


def tela_login():
    '''Faz o login do usuário, para em seguida direcionar ao menu principal'''
    limpar_tela()
    print("⚡   LOGIN VOLTLINK   ⚡")


    email = input("E-mail: ").strip().lower()
    senha = input("Senha: ").strip()

    conn = db_singleton.get_connection()
    if not conn: 
        print("\n Erro de conexão! ")
        input("Pressione Enter para voltar...")
        return 

    usuario_encontrado = conn.execute(
        "SELECT * FROM users WHERE email = ?", (email,)
    ).fetchone()

    if not usuario_encontrado:
        print("\n Erro: usuário não encontrado ")
        input("Pressione Enter para tentar novamente")
    elif usuario_encontrado['password'] == senha: 
        dados_usuario = dict(usuario_encontrado)
        print(f"\n Pressione Enter para entrar no Painel")
        menu_principal_logado(dados_usuario)
    else: 
        print("\n Erro: Senha incorreta. ")
        input("Pressione Enter para tentar novamente...")


def recuperar_senha():
    limpar_tela()
    print("🔐   RECUPERAR SENHA VOLTLINK   ")
    
    email = input("\nDigite o e-mail da sua conta: ").strip().lower()
    telefone = input("Confirme seu telefone (11 dígitos): ").strip()

    conn = db_singleton.get_connection()
    # Primeiro, verificamos se o e-mail e o telefone batem (segurança básica)
    usuario = conn.execute(
        "SELECT * FROM users WHERE email = ? AND phone_number = ?", 
        (email, telefone)
    ).fetchone()

    if usuario:
        print(f"\nUsuário verificado: {usuario['name']}")
        nova_senha = input("Digite sua NOVA senha (4-8 caracteres): ").strip()
        confirmacao = input("Confirme a nova senha: ").strip()

        if nova_senha == confirmacao and 4 <= len(nova_senha) <= 8:
            # Aqui acontece a mágica do UPDATE
            conn.execute(
                "UPDATE users SET password = ? WHERE email = ?", 
                (nova_senha, email)
            )
            conn.commit()
            print("\n✅ Senha alterada com sucesso!")
        else:
            print("\n❌ Erro: As senhas não batem ou são inválidas.")
    else:
        print("\n❌ Erro: Dados não conferem. Não é possível alterar a senha.")
    
    input("\nPressione Enter para voltar...")


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


def menu_principal_logado(usuario):
    while True: 
        limpar_tela()
        status = "ADMIN" if usuario['is_admin'] == 1 else "MOTORISTA"
        print(f" ⚡  PAINEL DO USUÁRIO | Olá, {usuario['name']} [{status}]  ⚡")
       
        print("1. 🚗 Meus Veículos (Novo!)")
        print("2. ✅ Check-in")
        print("3. 💳 Gerenciar Cartões")
        print("4. 📍 Buscar Eletropostos")
        print("5. 👤 Minha Conta")
        print("6. 🚪 Sair")

        if usuario['is_admin'] == 1:
            print("7.  PAINEL ADMINISTRATIVO (Gestão)")

        opcao = input("\nEscolha uma opção: ")
        
        if opcao == "1":
            menu_veiculos(usuario) # Abre o submenu de veículos
        elif opcao == "2": 
            fazer_checkin(usuario)
        elif opcao == "3":
            limpar_tela()
            print("💳  MEUS CARTÕES SALVOS")
            cartoes = buscar_cartoes_usuario(usuario['id'])
            if not cartoes: 
                print("Você ainda não possui cartões cadastrados.")
            else: 
                for c in cartoes: 
                    num_final = c['card_number'][-4:]
                    print(f"• {c['method_type']} | Final: **** {num_final}")
            escolha = input("\nDeseja cadastrar um novo cartão? (S/N): ").upper()    
            if escolha == "S":
               cadastrar_cartao(usuario)
            input("\n Pressione Enter para voltar...")
            
        elif opcao == "4":
            print("\n" + "="*40)
            print("📍  BUSCAR ELETROPOSTOS PRÓXIMOS")
            print("="*40)
            local = input("Digite sua localização atual: ") 
            postos = buscar_postos_proximos(local)
            # MOSTRAR POSTOS ENCONTRADOS 
            if not postos:
                print("\n❌ Nenhum posto encontrado no sistema.")
            else:
                print(f"\n✅ Encontramos os {len(postos)} postos mais próximos de você:")
                for p in postos:
                    print(f"\n🔋 {p['name']}")
                    print(f"   📍 Endereço: {p['address']}")
                    print(f"   📏 Distância Estimada: {p['distance_km']} km")
                    print(f"   ⚡ Potência: {p['max_power_kw']} kW")
                    print(f"   🔌 Vagas: {p['available_chargers']}/{p['total_chargers']}")
                    
                    #LINK MAPS 
                    link = criar_link_mapa(local, p['address'])
                    print(f"   🔗 Rota: {link}")
                    print("-" * 30)

            input("\nPressione Enter para voltar ao menu...")          
               
        elif opcao == "5":
            mostrar_minha_conta(usuario)
        elif opcao == "6":
            print("Fazendo logout...")
            break # volta pro menu de entrada
        elif opcao == "7" and usuario['is_admin'] == 1: 
            menu_admin_gestao(usuario)
        else:
            print("Opção inválida! Escolha de 1 a {'8' if usuario['is_admin'] == 1 else '7'}.")
            input("Aperte Enter...")


def menu_admin_gestao(usuario_logado): 
    '''Tela acessada apenas por admin's'''
    while True:
        limpar_tela()
        print("⚡  SISTEMA VOLTLINK | GESTÃO ADMINISTRATIVA  ⚡")
        print(f"Admin: {usuario_logado['name']}")
        print("-" * 40)
        print("1. ➕ Cadastrar Novo Administrador")
        print("2. 🔌 Cadastrar Novo Eletroposto")
        print("3. 👥 Listar Todos os Usuários")
        print("0. ⬅️  Voltar ao Menu Principal")
        
        op = input("\nEscolha uma ação: ")
        
        if op == "1":
            nome = input("Nome do Novo Admin: ")
            email = input("E-mail: ").strip().lower()
            senha = input("Senha: ")
            telefone = "000000000" # Valor padrão já que não pediu no input

            conn = db_singleton.get_connection()
            try:
                conn.execute("""
                    INSERT INTO users (name, email, phone_number, password, is_admin)
                    VALUES (?, ?, ?, ?, ?)
                """, (nome, email, telefone, senha, 1)) # O '1' é o que torna ele ADMIN
                
                conn.commit() # ESSENCIAL: Salva as alterações no arquivo .db
                print(f"\n✅ {nome} agora é um administrador oficial no sistema!")
            except Exception as e:
                print(f"\n❌ Erro ao salvar novo admin: {e}")
            
            input("Pressione Enter para continuar...")

        elif op == "2":
            # Aqui você usa a função que já existe no seu station_manager.py
            from core.station_manager import cadastrar_posto
            nome_p = input("Nome do Posto: ")
            end_p = input("Endereço: ")
            vagas = int(input("Total de Vagas: "))
            potencia = float(input("Potência (kW): "))
            
            sucesso, msg = cadastrar_posto(nome_p, end_p, vagas, vagas, potencia)
            print(f"\n{msg}")
            input("Enter...")

        elif op == "3":
            print("\n--- LISTA DE USUÁRIOS CADASTRADOS ---")
            conn = db_singleton.get_connection()
            usuarios = conn.execute("SELECT name, email, is_admin FROM users").fetchall()
            
            for u in usuarios:
                tipo = "Admin" if u['is_admin'] == 1 else "Motorista"
                print(f"• {u['name']} ({u['email']}) - [{tipo}]")
                
            input("\nFim da lista. Enter para voltar.")

        elif op == "0":
            break


def menu_veiculos(usuario):
    while True:
        limpar_tela()
        print(f"🚗   MEUS VEÍCULOS | {usuario['name']}")
        print("1. Cadastrar Novo Veículo")
        print("2. Ver/Excluir Veículos Salvos")
        print("3. Voltar")
        
        op = input("\nEscolha: ")
        if op == "1": cadastrar_veiculo(usuario)
        elif op == "2": listar_excluir_veiculos(usuario)
        elif op == "3": break


def cadastrar_veiculo(usuario):
    limpar_tela()
    print("📝 CADASTRO DE VEÍCULO")
    marca_modelo = input("Marca e Modelo: ")
    placa = input("Placa: ").upper()
    entrada_capacidade = input("Capacidade da Bateria (kWh): ").replace(',', '.')
    capacidade = float(entrada_capacidade)
    conector = input("Tipo de Conector (Tipo 2 / CCS2): ")

    conn = db_singleton.get_connection()
    conn.execute("INSERT INTO vehicles (user_id, model, plate, battery_capacity, connector_type) VALUES (?, ?, ?, ?, ?)",
                 (usuario['id'], marca_modelo, placa, capacidade, conector))
    conn.commit()
    print("\n✅ Veículo salvo!")
    input("Enter para continuar...")


def listar_excluir_veiculos(usuario):
    while True:
        limpar_tela()
        conn = db_singleton.get_connection()
        veiculos = conn.execute("SELECT * FROM vehicles WHERE user_id = ?", (usuario['id'],)).fetchall()
        
        print("📋 SEUS VEÍCULOS:")
        for v in veiculos:
            print(f"ID: {v['id']} | {v['model']} [{v['plate']}]")
        
        print("\nPara excluir, digite o ID do veículo ou 'S' para sair.")
        escolha = input("Escolha: ").upper()
        
        if escolha == 'S': break
        else:
            # Comando DELETE do SQL
            conn.execute("DELETE FROM vehicles WHERE id = ? AND user_id = ?", (escolha, usuario['id']))
            conn.commit()
            print("🗑️ Veículo removido!")
            input("Enter...")