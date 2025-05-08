## RadarFit - API Wellhub + Flask  

## (LOGOTIPO)

![logoradarfit (1)](https://github.com/user-attachments/assets/68b31344-0112-4455-9c2f-d1842b62ad75)

Este projeto é um motor de busca de academias que utiliza **Coleta de dados de uma API**, integração com **geolocalização via Geopy** e uma interface web simples feita com **Flask**. Basta digitar o nome de uma cidade ou local, e o sistema retorna academias próximas com base nos dados reais do site da Wellhub.

---

## Funcionalidades

- Interface web simples para busca
- Geolocalização com `Nominatim`
- Requisições à API da Wellhub
- Visualização dos resultados diretamente no navegador


---

## Tecnologias Utilizadas

- Python 3.11
- Flask
- requests
- geopy

---

## Estrutura do Projeto

buscador-academias/
├── templates/
│ └── index.html # Interface HTML
├── app.py # Código principal
├── requirements.txt # Dependências
├── README.md # Documentação do projeto
└── .gitignore # Arquivos ignorados
