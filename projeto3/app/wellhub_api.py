import requests
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderUnavailable, GeocoderTimedOut

def geocode_location(place_name):
    geolocaliza = Nominatim(user_agent="teste-code")
    try:
        location = geolocaliza.geocode(place_name)
        if location:
            print(f"🔍 Localização encontrada: {location.address} (Lat: {location.latitude}, Lon: {location.longitude})")
        else:
            print("❌ Localização não encontrada. Verifique se o CEP está correto.")
        return location
    except (GeocoderUnavailable, GeocoderTimedOut):
        print("⚠️ Serviço de geolocalização indisponível no momento.")
        return None

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
    return response

def resultados_exibidos(data):
    if isinstance(data, list) and data:
        for result in data:
            name = result.get("name", "Nome não disponível")
            full_address = result.get("fullAddress", "Endereço completo não disponível")
            cep = result.get("cep", "CEP não localizado")
            activities = result.get("activities", [])
            print(f"🏋️ Nome: {name}")
            print(f"📍 Endereço Completo: {full_address}")
            print(f"🧾 CEP: {cep}")
            print(f"🔥 Atividades: {', '.join(activities) if activities else 'Nenhuma atividade disponível'}")
            print("-" * 50)
    else:
        print("❌ Nenhum resultado encontrado ou resposta inválida da API.")

def main():
    place_name = input("Digite o nome do lugar (cidade, bairro ou CEP): ").strip()
    location = geocode_location(place_name)
    
    if location:
        token = "79b04a6d36f4efaac4e8fbfe54398e276a99ac0d9021550e50406be01c99c608"
        response = get_wellhub_data(location, place_name, token)
        
        if response.status_code == 200:
            try:
                data = response.json()
                resultados_exibidos(data)
            except ValueError:
                print("❌ Erro ao decodificar JSON. A resposta não está no formato esperado.")
        elif response.status_code == 401:
            print("🚫 ERRO DE AUTORIZAÇÃO. VERIFIQUE O TOKEN BEARER.")
        elif response.status_code == 404:
            print("🔎 RECURSO NÃO ENCONTRADO.")
        elif response.status_code == 500:
            print("⚠️ ERRO 500. POSSÍVEL CONFLITO COM O CABEÇALHO.")
        else:
            print(f"⚠️ Erro {response.status_code}: {response.text}")
    else:
        print("❌ Não foi possível localizar o local informado.")

if __name__ == "__main__":
    main()
