import urllib.parse     #biblioteca de URL
import random           #biblioteca para criar coisas aleatórias (id de transação, pin, etc)
from database.db_handler import db_singleton       # importar um arquivo que já criamos

def cadastrar_posto(nome, endereço, total_carregadores, disponiveis, potencia_kw):
    """Cadastra um novo eletroposto no banco de dados."""
    conn = db_singleton.get_connection()
    if not conn:
        return (False, "Erro: Sem conexão com o banco de dados.")
    
    try:
        conn.execute("INSERT INTO stations (name, address, total_chargers, available_chargers, max_power_kw) VALUES (?, ?, ?, ?, ?)", (nome, endereço, total_carregadores, disponiveis, potencia_kw))
        conn.commit()
        return (True, "Eletroposto cadastrado com sucesso!")
    except Exception as e:
        return (False, f"Erro ao cadastrar eletroposto: {e}")  # esse "{e}" mostra o motivo do erro

def buscar_postos_proximos(endereco_atual, limite=3):
    """Busca eletropostos e simula a distância até o endereço atual."""
    conn = db_singleton.get_connection()
    if not conn: return []
    
    lista_postos = conn.execute("SELECT * FROM stations").fetchall()   #fetchall: pega tds os postos os postos proximos dentro do limite
    
    resultados = []
    for posto in lista_postos:
        dicionario_posto = dict(posto)
        # Simulando uma distância aleatória entre 1km e 15km para o projeto acadêmico
        dicionario_posto['distance_km'] = round(random.uniform(1.0, 15.0), 1)
        resultados.append(dicionario_posto)
    
    # Ordena do mais perto para o mais distante (3)
    resultados.sort(key=lambda x: x['distance_km'])
    return resultados[:limite]

def criar_link_mapa(origem, destino):
    """Cria o link que abre o Google Maps com a rota."""
    base_url = "https://www.google.com/maps/dir/?api=1"
    origem_formatada = urllib.parse.quote(origem)
    destino_formatado = urllib.parse.quote(destino)
    return f"{base_url}&origin={origem_formatada}&destination={destino_formatado}"

def buscar_todos_postos():
    """Mostra a lista todos os eletropostos cadastrados."""
    conn = db_singleton.get_connection()
    if not conn: return []
    return conn.execute("SELECT * FROM stations").fetchall()

'''PRÓXIMA VA'''

def atualizar_vagas_posto(id_posto, novos_disponiveis):
    """Atualiza a quantidade de carregadores disponíveis de um eletroposto."""
    conn = db_singleton.get_connection()
    if not conn:
        return (False, "Erro: Erro de conexão.")
    try:
        conn.execute("UPDATE stations SET available_chargers = ? WHERE id = ?", (novos_disponiveis, id_posto))
        conn.commit()
        return (True, "Vagas atualizadas!")
    except Exception as e:
        return (False, f"Erro ao atualizar carregadores: {e}")

def enviar_avaliacao(id_posto, usuario, nota, comentario):
    """Adiciona uma avaliação a um eletroposto."""
    conn = db_singleton.get_connection()
    try:
        conn.execute("""
            INSERT INTO reviews (station_id, user_name, rating, comment) 
            VALUES (?, ?, ?, ?)
        """, (id_posto, usuario['name'], nota, comentario))
        
        conn.commit()
        return (True, "Avaliação enviada!")
    
    except Exception as e:
        print("Erro interno: {e}")
        return False, f"erro ao enviar avaliação: {e}"

def avaliar_posto_interface(usuario, id_posto):
    """Faz as perguntas no terminal e chama a gravação no banco."""
    print("\n" + "="*30)
    print(" ⭐ AVALIAR ELETROPOSTO ")
    print("="*30)
    
    try:
        nota = int(input("Nota de 1 a 5: "))
        if nota < 1 or nota > 5:
            print("❌ Nota inválida! Escolha entre 1 e 5.")
            return
            
        comentario = input("Comentário: ").strip()
        
        sucesso, msg = enviar_avaliacao(id_posto, usuario, nota, comentario)
        
        if sucesso:
            print(f"\n✅ {msg}")
        else:
            print(f"\n❌ {msg}")
            
    except ValueError:
        print("❌ Erro: Digite um número inteiro para a nota.")

'''PRÓXIMA VA '''

def buscar_avaliacoes_postos(id_posto):
    """Retorna todas as avaliações de um eletroposto específico."""
    conn = db_singleton.get_connection()
    if not conn: return []
    return conn.execute("SELECT * FROM reviews WHERE station_id = ? ORDER BY created_at DESC", (id_posto,)).fetchall()

def calcular_media_posto(id_posto):
    """Retorna a média de avaliações de um eletroposto."""
    conn = db_singleton.get_connection()
    if not conn: return 0.0
    resultado = conn.execute("SELECT AVG(rating) as avg_rating FROM reviews WHERE station_id = ?", (id_posto,)).fetchone() #pega a media de avaliação do posto selecionado
    if resultado and resultado['avg_rating']:
        return round(resultado['avg_rating'], 1)
    return 0.0