# 🏋️‍♂️ RadarFit - Wellhub + Flask

Este projeto é um motor de busca de academias que utiliza **web scraping da Wellhub**, integração com **geolocalização via Geopy** e uma interface web simples feita com **Flask**. Basta digitar o nome de uma cidade ou local, e o sistema retorna academias próximas com base nos dados reais da Wellhub.

---

## 🚀 Funcionalidades

- Interface web simples para busca
- Geolocalização com `Nominatim`
- Requisições à API da Wellhub
- Visualização dos resultados diretamente no navegador


---

## 🛠️ Tecnologias Utilizadas

- Python 3.11
- Flask
- requests
- geopy

---

## 🗂️ Estrutura do Projeto

buscador-academias/
├── templates/
│ └── index.html # Interface HTML
├── app.py # Código principal
├── requirements.txt # Dependências
├── README.md # Documentação do projeto
└── .gitignore # Arquivos ignorados
