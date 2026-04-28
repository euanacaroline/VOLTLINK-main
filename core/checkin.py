import os
from database.db_handler import db_singleton
from core.pagamento import processar_pagamento 
from core.station_manager import avaliar_posto_interface
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def fazer_checkin(usuario):
    limpar_tela()
    print(f"⚡   INICIANDO CHECK-IN | {usuario['name']}   ⚡")
    
    conn = db_singleton.get_connection()
    
    # 1. Seleção do Veículo
    veiculos = conn.execute("SELECT * FROM vehicles WHERE user_id = ?", (usuario['id'],)).fetchall()
    if not veiculos:
        print("\n❌ Erro: Você não tem veículos cadastrados.")
        input("Pressione Enter para voltar...")
        return

    print("\nSelecione o veículo para recarga:")
    for i, v in enumerate(veiculos):
        print(f"{i+1}. {v['model']} [{v['plate']}]")
    
    try:
        escolha = int(input("\nOpção: ")) - 1
        veiculo_selecionado = veiculos[escolha]
    except:
        print("Opção inválida.")
        return

    # 2. RECARGA
    try:
        '''Pede nível da bateria, valida, manda alerta'''
        bateria_input = int(input("Nível atual da bateria (%): "))
    
        if bateria_input < 0 or bateria_input > 100:
            print("\n❌ Erro: O nível de bateria deve estar entre 0 e 100.")
            input("Pressione Enter para tentar novamente...")
            return 
            
        bateria_atual = bateria_input # Se passou na validação, aceita o valor

        if bateria_atual <= 20:
            print("\n🚨 ALERTA: POUCA BATERIA!")
        elif 21 <= bateria_atual <= 50:
            print("\n⚠️ Nível médio.")
        elif 51 <= bateria_atual <= 100:
            print("\n✅ Bateria bem.")

        bateria_desejada = int(input("Deseja carregar até quanto (%): "))
        
        if bateria_desejada < 0 or bateria_desejada > 100:
            print("\n❌ Erro: O objetivo de carga deve estar entre 0 e 100.")
            input("Pressione Enter para tentar novamente...")
            return
            
        if bateria_desejada <= bateria_atual:
            print("\n❌ Erro: A bateria desejada deve ser maior que a atual.")
            input("Pressione Enter para tentar novamente...")
            return
            
    except ValueError:
        print("\n❌ Erro: Digite apenas números inteiros para a bateria.")
        input("Pressione Enter para tentar novamente...")
        return
    

    # 3. Seleção do Posto
    postos = conn.execute("SELECT id, name FROM stations").fetchall()
    print("\nPostos Disponíveis:")
    for p in postos:
        print(f"ID: {p['id']} - {p['name']}")
    id_posto = input("\nDigite o ID do posto onde você está: ")

    # 4. Cálculo (kWh necessário * preço simbólico de R$ 2.00)
    diferenca_percentual = bateria_desejada - bateria_atual
    kwh_a_carregar = (veiculo_selecionado['battery_capacity'] * diferenca_percentual) / 100
    valor_total = kwh_a_carregar * 2.00
    
    #5. Resumo e Confirmação
    print(f"\n--- RESUMO ---")
    print(f"Energia: {kwh_a_carregar:.2f} kWh")
    print(f"Valor a pagar: R$ {valor_total:.2f}")
    
    confirmar = input("\nConfirmar início da recarga e pagamento? (S/N): ").upper()
    
    if confirmar == "S":
        pagou = processar_pagamento(usuario, valor_total)
        if pagou:
            print("\n⚡ PAGAMENTO APROVADO!")
            print("⏳ Iniciando transferência de energia...")
            print("\n✅ Recarga concluída com sucesso! Dirija com segurança.")
            pergunta = input("\nDeseja avaliar este posto? (S/N): ").upper()
            if pergunta == 'S':
                # id_posto_input é a variável que você coletou no passo 3 do check-in
                avaliar_posto_interface(usuario, id_posto)
        else:
            print("\n❌ Recarga cancelada: Pagamento não realizado.")
    else:
        print("\n❌ Operação cancelada pelo usuário.")
    input("\nPressione Enter para voltar ao menu...")