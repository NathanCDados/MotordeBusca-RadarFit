from flask import Flask, render_template, request
import requests
from geopy.geocoders import Nominatim

app = Flask(__name__)

def geocode_location(place_name):
    geolocaliza = Nominatim(user_agent="teste-code")
    return geolocaliza.geocode(place_name)

def get_wellhub_data(location, place_name, token):
    headers = {
        'accept': '*/*',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'authorization': 'Bearer 79b04a6d36f4efaac4e8fbfe54398e276a99ac0d9021550e50406be01c99c608',
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
    return response.json()  # Retorna os dados da resposta já convertidos para JSON

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        place_name = request.form['place_name']
        location = geocode_location(place_name)
        
        if location:
            token = "79b04a6d36f4efaac4e8fbfe54398e276a99ac0d9021550e50406be01c99c608"
            data = get_wellhub_data(location, place_name, token)
            
            if isinstance(data, list) and data:
                return render_template('index.html', results=data)
            else:
                return render_template('index.html', message="Nenhum resultado encontrado.")
        else:
            return render_template('index.html', message="Localização não encontrada.")
    
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
