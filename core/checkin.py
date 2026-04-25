import os
from database.db_handler import db_singleton
# Importamos o pagamento para chamar após o check-in
from core.pagamento import tela_pagamento 

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

    # 2. Dados da Recarga
    bateria_atual = int(input("Nível atual da bateria (%): "))
    bateria_desejada = int(input("Deseja carregar até quanto (%): "))
    
    # 3. Seleção do Posto
    # Aqui listamos os postos do banco
    postos = conn.execute("SELECT id, name FROM stations").fetchall()
    print("\nPostos Disponíveis:")
    for p in postos:
        print(f"ID: {p['id']} - {p['name']}")
    id_posto = input("\nDigite o ID do posto onde você está: ")

    # 4. Cálculo (kWh necessário * preço simbólico de R$ 2.00)
    diferenca_percentual = bateria_desejada - bateria_atual
    kwh_a_carregar = (veiculo_selecionado['battery_capacity'] * diferenca_percentual) / 100
    valor_total = kwh_a_carregar * 2.00

    print(f"\n--- RESUMO ---")
    print(f"Energia: {kwh_a_carregar:.2f} kWh")
    print(f"Valor a pagar: R$ {valor_total:.2f}")
    
    input("\nConfirmar e ir para o Pagamento... (Enter)")
    
    # 5. Chama o módulo de pagamento (Passando o valor calculado)
    # tela_pagamento(valor_total) 
    
    print("\n✅ Recarga iniciada! Você receberá uma notificação ao concluir.")
    input("Pressione Enter para finalizar...")


# cálculos recarga

    print(f"\n--- RESUMO DA RECARGA ---")
    print(f"Posto: {id_posto}")
    print(f"Total: R$ {valor_total:.2f}")
    
    input("\nConfirmar e ir para o Pagamento... (Enter)")
    
    
    from core.pagamento import processar_pagamento
    '''chamar função de pagamento '''
    pagou = processar_pagamento(usuario, valor_total)
    
    if pagou:
        print("\n⚡ PAGAMENTO APROVADO!")
        print("Iniciando transferência de energia...")
        # Aqui você pode colocar um mini loop de "Carregando..."
        print("\n✅ Recarga concluída com sucesso! Dirija com segurança.")
    else:
        print("\n❌ Recarga cancelada: Pagamento não realizado.")
    
    input("\nPressione Enter para voltar ao menu...")