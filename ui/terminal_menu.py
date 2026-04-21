import os
import webbrowser
from core import user_manager, station_manager, pagamento
from ui import logo_VoltLink

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_registration_screen():
    """Exibe a tela de cadastro e gerencia o fluxo."""
    name = ""
    email = ""
    phone = ""

    while True:
        clear_screen()
        print("   CADASTRO VOLTLINK   ")
        if name or email or phone:
            print("   (Dica: Deixe em branco e pressione Enter para manter o dado já digitado)\n")
        
        new_name = input(f"Digite seu nome completo [{name}]: " if name else "Digite seu nome completo: ").strip()
        if new_name: name = new_name
        
        new_email = input(f"Digite seu email [{email}]: " if email else "Digite seu email: ").strip().lower()
        if new_email: email = new_email
        
        new_phone = input(f"Digite seu telefone (11 dígitos) [{phone}]: " if phone else "Digite seu telefone (11 dígitos, apenas números): ").strip()
        if new_phone: phone = new_phone
        
        # Senhas sempre precisam ser redigitadas por segurança
        password = input("Crie uma senha (4-8 caracteres, 1 número, 1 maiúscula): ").strip()
        confirm_password = input("Confirme sua senha: ").strip()

        is_valid, message = user_manager.validate_registration_data(name, email, phone, password, confirm_password)

        if not is_valid:
            print(f"\n{message}")
            opcao = input("\nDeseja corrigir os dados agora? (S/N): ").strip().upper()
            if opcao == 'N':
                return
            continue

        # Se a validação passou, registra o usuário
        user_manager.register_new_user(name, email, phone, password)
        print("\nCadastro realizado com sucesso!")
        print(f"Usuário: {name} ({email})")
        input("\nPressione Enter para voltar ao menu...")
        break

def show_login_screen():
    """Exibe a tela de login e gerencia o fluxo."""
    clear_screen()
    logo_VoltLink.display_header()
    print("   LOGIN VOLTLINK   ")
    
    email = input("Digite seu email: ").strip().lower()
    password = input("Digite sua senha: ").strip()

    # Chama a função do core para validar o login
    is_logged_in, result = user_manager.login_user(email, password)

    if is_logged_in:
        print(f"\nLogin bem-sucedido! Bem-vindo(a) de volta, {result['name']}!")
        input("\nPressione Enter para continuar...")
        show_user_dashboard(result)
    else:
        error_message = result
        print(f"\n{error_message}")
        input("\nPressione Enter para voltar ao menu...")

def show_user_dashboard(user_data):
    """Exibe o menu do usuário após o login."""
    user_name = user_data['name']
    is_admin = user_data.get('is_admin', 0) == 1

    while True:
        try:
            clear_screen()
            logo_VoltLink.display_header()
            tipo_conta = "ADMINISTRADOR" if is_admin else "USUÁRIO"
            print(f"   PAINEL DO {tipo_conta} - {user_name.upper()}   \n")
            
            print("1. Localização e Planeamento de Rotas")
            print("2. Gestão de Pagamentos")
            print("3. Dados sobre o Veículo")
            print("4. Check-in")
            print("5. Avaliar Eletropostos")
            print("6. Fazer Logout")
            
            if is_admin:
                print("7. [Admin] Cadastrar Eletroposto")
                print("8. [Admin] Atualizar Carregadores Disponíveis")
            
            option = input("\nEscolha uma opção: ")
            
            if option == '1':
                clear_screen()
                logo_VoltLink.display_header()
                print("📍 Localização e Planeamento de Rotas \n")
                print("Esta funcionalidade é o coração do seu planeamento. Com base na sua localização atual")
                print("ou no ponto inicial da viagem, o VoltLink calcula as rotas mais eficientes,")
                print("priorizando os postos de carregamento mais próximos e estratégicos.\n")
                
                endereco = input("Digite seu endereço atual (Rua, Número, Cidade): ").strip()
                if endereco:
                    print("\nBuscando os 3 eletropostos VOLTLINK mais próximos...")
                    postos_proximos = station_manager.get_closest_stations(endereco, limit=3)
                    
                    if not postos_proximos:
                        print("\nNenhum eletroposto cadastrado no sistema ainda.")
                    else:
                        for i, st in enumerate(postos_proximos, 1):
                            avg_rating = station_manager.get_station_average_rating(st['id'])
                            estrelas = f"{avg_rating} ⭐" if avg_rating > 0 else "Sem avaliações"
                            status = "🟢 Disponível" if st['available_chargers'] > 0 else "🔴 Ocupado"
                            print(f"{i}. {st['name']} - {st['address']}")
                            print(f"   └─ Avaliação: {estrelas}")
                            print(f"   └─ Status: {status} ({st['available_chargers']}/{st['total_chargers']} livres)")
                            print(f"   └─ Potência: {st['max_power_kw']} kW | Distância: {st['distance_km']} km\n")
                        
                        escolha = input("\nEscolha o número do eletroposto para navegar (ou Enter para voltar): ")
                        if escolha.isdigit() and 1 <= int(escolha) <= len(postos_proximos):
                            st_escolhido = postos_proximos[int(escolha)-1]
                            link = station_manager.generate_maps_link(endereco, st_escolhido['address'])
                            
                            print(f"\nRota para {st_escolhido['name']} gerada com sucesso!")
                            print("Tentando abrir no seu navegador...")
                            print(f"Caso não abra, acesse o link: {link}")
                            
                            # Abre o navegador automaticamente
                            webbrowser.open(link)

                input("\nPressione Enter para voltar ao painel...")
            elif option == '2':
                while True:
                    clear_screen()
                    logo_VoltLink.display_header()
                    print("💳 Gestão de Pagamentos \n")
                    
                    methods = pagamento.get_payment_methods(user_data['id'])
                    if not methods:
                        print("Nenhuma forma de pagamento cadastrada.\n")
                    else:
                        print("Suas formas de pagamento:")
                        for m in methods:
                            print(f"ID: {m['id']:<2} | [{m['method_type']}] {m['card_name']} - {m['card_number']} (Val: {m['card_expiry']})")
                        print("")

                    print("Opções:")
                    print("1. Adicionar Cartão de Crédito")
                    print("2. Adicionar Cartão de Débito")
                    print("3. Editar Cartão")
                    print("4. Remover Forma de Pagamento")
                    print("0. Voltar ao Painel")

                    sub_opt = input("\nEscolha uma opção: ").strip()
                    if sub_opt in ['1', '2']:
                        m_type = "CRÉDITO" if sub_opt == '1' else "DÉBITO"
                        print(f"\n--- Novo Cartão de {m_type} ---")
                        nome = input("Nome do Titular: ").strip().upper()
                        num = input("Número do Cartão (16 dígitos): ").replace(" ", "")
                        val = input("Validade (MM/AA): ").strip()
                        cvv = input("CVV (apenas para validação): ").strip()
                        success, msg = pagamento.add_card(user_data['id'], m_type, nome, num, val, cvv)
                        print(f"\n{msg}")
                        input("\nPressione Enter para continuar...")
                    elif sub_opt == '3':
                        try:
                            m_id = int(input("\nDigite o ID do cartão que deseja editar: ").strip())
                            novo_nome = input("Novo Nome do Titular: ").strip().upper()
                            novo_num = input("Novo Número do Cartão (16 dígitos): ").replace(" ", "")
                            nova_val = input("Nova Validade (MM/AA): ").strip()
                            novo_cvv = input("Novo CVV (apenas para validação): ").strip()
                            success, msg = pagamento.update_card(user_data['id'], m_id, novo_nome, novo_num, nova_val, novo_cvv)
                            print(f"\n{msg}")
                        except ValueError:
                            print("\nID inválido.")
                        input("\nPressione Enter para continuar...")
                    elif sub_opt == '4':
                        try:
                            m_id = int(input("\nDigite o ID da forma de pagamento a remover: ").strip())
                            success, msg = pagamento.delete_payment_method(user_data['id'], m_id)
                            print(f"\n{msg}")
                        except ValueError:
                            print("\nID inválido.")
                        input("\nPressione Enter para continuar...")
                    elif sub_opt == '0':
                        break
                    else:
                        print("\nOpção inválida.")
                        input("\nPressione Enter para tentar novamente...")
            elif option == '3':
                clear_screen()
                logo_VoltLink.display_header()
                print("🚗 Dados sobre o Veículo \n")
                print("-" * 40)
                print("AVISO: Função em desenvolvimento!")
                print("-" * 40)
                input("\nPressione Enter para voltar ao painel...")
            elif option == '4':
                clear_screen()
                logo_VoltLink.display_header()
                print("✅ Check-in \n")
                print("-" * 40)
                print("AVISO: Função em desenvolvimento!")
                print("-" * 40)
                input("\nPressione Enter para voltar ao painel...")
            elif option == '5':
                clear_screen()
                logo_VoltLink.display_header()
                print("⭐ Avaliar Eletropostos \n")
                
                stations = station_manager.get_all_stations()
                if not stations:
                    print("Nenhum eletroposto cadastrado.")
                else:
                    for st in stations:
                        avg_rating = station_manager.get_station_average_rating(st['id'])
                        estrelas = f"{avg_rating} ⭐" if avg_rating > 0 else "Sem avaliações"
                        print(f"ID: {st['id']:<3} | {st['name']} ({estrelas})")
                    
                    print("\nOpções:")
                    print("1. Ver avaliações de um eletroposto")
                    print("2. Fazer uma nova avaliação")
                    print("0. Voltar")
                    
                    sub_opt = input("\nEscolha uma opção: ").strip()
                    if sub_opt == '1':
                        try:
                            st_id = int(input("Digite o ID do eletroposto: ").strip())
                            reviews = station_manager.get_station_reviews(st_id)
                            print("\n--- Avaliações ---")
                            if not reviews:
                                print("Nenhuma avaliação encontrada para este posto.")
                            else:
                                for rev in reviews:
                                    print(f"[{rev['rating']} ⭐] {rev['user_name']}: {rev['comment']}")
                        except ValueError:
                            print("ID inválido.")
                    elif sub_opt == '2':
                        try:
                            st_id = int(input("Digite o ID do eletroposto que deseja avaliar: ").strip())
                            rating = int(input("Nota (0 a 5): ").strip())
                            if 0 <= rating <= 5:
                                comment = input("Deixe um comentário (opcional): ").strip()
                                success, msg = station_manager.add_review(st_id, user_name, rating, comment)
                                print(f"\n{msg}")
                            else:
                                print("\nErro: A nota deve ser entre 0 e 5.")
                        except ValueError:
                            print("\nErro: Entrada inválida.")
                input("\nPressione Enter para voltar ao painel...")
            elif option == '6':
                print("\nFazendo logout...")
                break
            elif option == '7' and is_admin:
                clear_screen()
                logo_VoltLink.display_header()
                print("🛠️  [Admin] Cadastrar Eletroposto \n")
                nome_posto = input("Nome do Eletroposto (ex: VoltLink Centro): ").strip()
                end_posto = input("Endereço completo (ex: Av. Paulista, 1000, São Paulo): ").strip()
                try:
                    total_chargers = int(input("Quantidade total de carregadores: ").strip())
                    available_chargers = int(input("Quantidade de carregadores disponíveis agora: ").strip())
                    max_power = float(input("Potência máxima por carregador (kW): ").strip())
                    success, msg = station_manager.add_station(nome_posto, end_posto, total_chargers, available_chargers, max_power)
                    print(f"\n{msg}")
                except ValueError:
                    print("\nErro: Você deve digitar números válidos para quantidade e potência.")
                input("\nPressione Enter para voltar ao painel...")
            elif option == '8' and is_admin:
                clear_screen()
                logo_VoltLink.display_header()
                print("🔄  [Admin] Atualizar Carregadores Disponíveis \n")
                
                stations = station_manager.get_all_stations()
                if not stations:
                    print("Nenhum eletroposto cadastrado.")
                else:
                    for st in stations:
                        print(f"ID: {st['id']:<3} | {st['name']} ({st['available_chargers']}/{st['total_chargers']} livres)")
                    
                    try:
                        st_id = int(input("\nDigite o ID do eletroposto que deseja atualizar (ou 0 para cancelar): ").strip())
                        if st_id != 0:
                            novos_disponiveis = int(input("Nova quantidade de carregadores disponíveis: ").strip())
                            success, msg = station_manager.update_available_chargers(st_id, novos_disponiveis)
                            print(f"\n{msg}")
                    except ValueError:
                        print("\nErro: Você deve digitar números válidos.")
                input("\nPressione Enter para voltar ao painel...")
            else:
                print("\nOpção inválida!")
                input("Pressione Enter para tentar novamente...")
        except KeyboardInterrupt:
            print("\n\nVoltando ao menu principal...")
            break

def show_main_menu():
    """Exibe o menu principal e direciona o usuário."""
    while True:
        try:
            clear_screen()
            logo_VoltLink.display_header()

            print("1. Login")
            print("2. Cadastro")
            print("3. Sair")
            
            option = input("\nEscolha uma opção: ")
            
            if option == '1':
                show_login_screen()
            elif option == '2':
                show_registration_screen()
            elif option == '3':
                print("\nObrigado por usar o VoltLink! Saindo...")
                break
        except KeyboardInterrupt:
            print("\n\nSessão encerrada pelo usuário (Ctrl+C). Saindo...")
            break