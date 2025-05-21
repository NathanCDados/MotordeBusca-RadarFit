from flask import Flask, render_template, request
import requests
from geopy.geocoders import Nominatim
import folium

app = Flask(__name__)

# Dicionário para converter nome de estado para sigla
estado_siglas = {
    'acre': 'AC', 'alagoas': 'AL', 'amapa': 'AP', 'amazonas': 'AM', 'bahia': 'BA',
    'ceara': 'CE', 'distrito federal': 'DF', 'espirito santo': 'ES', 'goias': 'GO',
    'maranhao': 'MA', 'mato grosso': 'MT', 'mato grosso do sul': 'MS', 'minas gerais': 'MG',
    'para': 'PA', 'paraiba': 'PB', 'parana': 'PR', 'pernambuco': 'PE', 'piaui': 'PI',
    'rio de janeiro': 'RJ', 'rio grande do norte': 'RN', 'rio grande do sul': 'RS',
    'rondonia': 'RO', 'roraima': 'RR', 'santa catarina': 'SC', 'sao paulo': 'SP',
    'sergipe': 'SE', 'tocantins': 'TO'
}

# Mapeamento direto para cidades conhecidas
cidades_conhecidas = {
    'salvador': 'Salvador, BA',
    'são paulo': 'São Paulo, SP',
    'rio de janeiro': 'Rio de Janeiro, RJ',
    'belo horizonte': 'Belo Horizonte, MG',
    'brasilia': 'Brasília, DF',
    'recife': 'Recife, PE',
    'fortaleza': 'Fortaleza, CE',
    'manaus': 'Manaus, AM',
    'curitiba': 'Curitiba, PR',
    'porto alegre': 'Porto Alegre, RS'
}

def normalizar_estado(place_name):
    place_lower = place_name.lower().strip()
    if place_lower in cidades_conhecidas:
        return cidades_conhecidas[place_lower]
    for estado, sigla in estado_siglas.items():
        if estado in place_lower:
            cidade = place_lower.replace(estado, '').strip().title()
            return f"{cidade}, {sigla}"
    return place_name

def geocode_location(place_name):
    place_name = place_name.strip().replace("–", "-").replace("—", "-")
    digits = ''.join(filter(str.isdigit, place_name))
    if len(digits) == 8:
        place_name = digits[:5] + '-' + digits[5:]
    place_name = normalizar_estado(place_name)
    geolocaliza = Nominatim(user_agent="teste-code")
    location = geolocaliza.geocode(place_name)
    return location

def get_wellhub_data(location, place_name, token):
    headers = {
        'accept': '*/*',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'authorization': f'Bearer {token}',
        'content-type': 'application/json',
        'origin': 'https://wellhub.com',
        'referer': 'https://wellhub.com/',
    }
    params = {
        'lat': location.latitude,
        'lon': location.longitude,
        'locale': 'pt-br',
        'query': place_name,
    }
    response = requests.get('https://mep-partner-bff.wellhub.com/v2/search', params=params, headers=headers)
    data = response.json()

    # Tenta buscar por bairro se não achar resultados
    if not data or (isinstance(data, list) and not data):
        suburb = location.raw.get('address', {}).get('suburb', '')
        neighborhood = None
        if suburb:
            for component in suburb.split(','):
                if component.strip():
                    neighborhood = component.strip()
                    break
        if neighborhood:
            params['query'] = neighborhood
            response = requests.get('https://mep-partner-bff.wellhub.com/v2/search', params=params, headers=headers)
            data = response.json()
    return data

def criar_mapa(data, location):
    mapa = folium.Map(location=[location.latitude, location.longitude], zoom_start=13)
    for item in data:
        lat = item.get('latitude') or item.get('lat')
        lon = item.get('longitude') or item.get('lon')
        nome = item.get('name', 'Academia')
        endereco = item.get('fullAddress', 'Endereço não informado')
        if lat and lon:
            folium.Marker(
                location=[lat, lon],
                popup=f"<b>{nome}</b><br>{endereco}",
                icon=folium.Icon(color='green', icon='dumbbell', prefix='fa')
            ).add_to(mapa)
    return mapa._repr_html_()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        place_name = request.form['place_name']
        location = geocode_location(place_name)
        if location:
            token = "79b04a6d36f4efaac4e8fbfe54398e276a99ac0d9021550e50406be01c99c608"
            data = get_wellhub_data(location, place_name, token)
            if isinstance(data, list) and data:
                mapa_html = criar_mapa(data, location)
                return render_template('index.html', results=data, mapa_html=mapa_html)
            else:
                return render_template('index.html', message="Nenhum resultado encontrado.")
        else:
            return render_template('index.html', message="Localização não encontrada.")
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
