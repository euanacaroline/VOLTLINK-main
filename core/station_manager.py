import urllib.parse     #biblioteca de URL
import random           #biblioteca para criar coisas aleatórias (id de transação, pin, etc)
from database.db_handler import db_singleton       # importar um arquivo que já criamos

def add_station(name, address, total_chargers, available_chargers, max_power_kw):
    """Cadastra um novo eletroposto no banco de dados."""
    conn = db_singleton.get_connection()
    if not conn:
        return (False, "Erro: Falha na comunicação com o banco de dados.")
    
    try:
        conn.execute("INSERT INTO stations (name, address, total_chargers, available_chargers, max_power_kw) VALUES (?, ?, ?, ?, ?)", (name, address, total_chargers, available_chargers, max_power_kw))
        conn.commit()
        return (True, "Eletroposto cadastrado com sucesso!")
    except Exception as e:
        return (False, f"Erro ao cadastrar eletroposto: {e}")

def get_closest_stations(current_address, limit=3):
    """Busca eletropostos e simula a distância até o endereço atual."""
    conn = db_singleton.get_connection()
    if not conn: return []
    
    stations = conn.execute("SELECT * FROM stations").fetchall()
    
    results = []
    for st in stations:
        st_dict = dict(st)
        # Simulando uma distância aleatória entre 1km e 15km para o projeto acadêmico
        st_dict['distance_km'] = round(random.uniform(1.0, 15.0), 1)
        results.append(st_dict)
    
    # Ordena da menor distância para a maior e retorna o limite (3)
    results.sort(key=lambda x: x['distance_km'])
    return results[:limit]

def generate_maps_link(origin, destination):
    """Gera uma URL de rotas do Google Maps baseada na origem e destino."""
    base_url = "https://www.google.com/maps/dir/?api=1"
    origin_encoded = urllib.parse.quote(origin)
    dest_encoded = urllib.parse.quote(destination)
    return f"{base_url}&origin={origin_encoded}&destination={dest_encoded}"

def get_all_stations():
    """Retorna todos os eletropostos cadastrados."""
    conn = db_singleton.get_connection()
    if not conn: return []
    return conn.execute("SELECT * FROM stations").fetchall()

def update_available_chargers(station_id, available_chargers):
    """Atualiza a quantidade de carregadores disponíveis de um eletroposto."""
    conn = db_singleton.get_connection()
    if not conn:
        return (False, "Erro: Falha na comunicação com o banco de dados.")
    try:
        conn.execute("UPDATE stations SET available_chargers = ? WHERE id = ?", (available_chargers, station_id))
        conn.commit()
        return (True, "Status de carregadores atualizado com sucesso!")
    except Exception as e:
        return (False, f"Erro ao atualizar carregadores: {e}")

def add_review(station_id, user_name, rating, comment):
    """Adiciona uma avaliação a um eletroposto."""
    conn = db_singleton.get_connection()
    if not conn:
        return (False, "Erro: Falha na comunicação com o banco de dados.")
    try:
        conn.execute("INSERT INTO reviews (station_id, user_name, rating, comment) VALUES (?, ?, ?, ?)", (station_id, user_name, rating, comment))
        conn.commit()
        return (True, "Avaliação enviada com sucesso!")
    except Exception as e:
        return (False, f"Erro ao enviar avaliação: {e}")

def get_station_reviews(station_id):
    """Retorna todas as avaliações de um eletroposto específico."""
    conn = db_singleton.get_connection()
    if not conn: return []
    return conn.execute("SELECT * FROM reviews WHERE station_id = ? ORDER BY created_at DESC", (station_id,)).fetchall()

def get_station_average_rating(station_id):
    """Retorna a média de avaliações de um eletroposto."""
    conn = db_singleton.get_connection()
    if not conn: return 0.0
    result = conn.execute("SELECT AVG(rating) as avg_rating FROM reviews WHERE station_id = ?", (station_id,)).fetchone()
    if result and result['avg_rating']:
        return round(result['avg_rating'], 1)
    return 0.0