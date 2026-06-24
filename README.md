# 🎮 Steam Data Scraper
Um ecossistema de Web Scraping robusto desenvolvido em Python utilizando o framework **Scrapy** e **Requests**. O projeto foi projetado para minerar, cruzar e consolidar dados analíticos de jogos da plataforma Steam a partir de múltiplas fontes especializadas da web, unificando métricas de engajamento, precificação histórica e requisitos de hardware.

---

## 📌 Sumário
- [Fontes de Dados](#-fontes-de-dados)
- [Funcionalidades](#-funcionalidades)
- [Tecnologias Utilizadas](#%EF%B8%8F-tecnologias-utilizadas)
- [Arquitetura dos Spiders](#%EF%B8%8F-arquitetura-dos-spiders)
- [Instalação e Pré-requisitos](#-instalação-e-pré-requisitos)
- [Como Executar](#-como-executar)

---

## 🌐 Fontes de Dados

O sistema realiza o cruzamento de dados extraindo informações de três ecossistemas principais:
* **SteamCharts:** Histórico de jogadores simultâneos e tendências de atividade.
* **GG.deals:** Histórico completo de preços, promoções e flutuação de valores no varejo digital.
* **SteamBase:** Mapeamento cronológico de grandes eventos de descontos e sales da Steam.

---

## 🚀 Funcionalidades

* **Mineração Híbrida (HTML + API):** Combina seletores CSS/XPath para raspagem de páginas estáticas com requisições diretas a endpoints de APIs internas das plataformas para extração de payloads JSON puros.
* **Tratamento de Strings Avançado:** Limpeza automatizada de títulos de jogos via Expressões Regulares (`re`) para garantir casamento perfeito de chaves de busca entre diferentes sites.
* **Extração de Requisitos de Hardware:** Parseamento fino de componentes de hardware (CPU, GPU, RAM) divididos entre configurações Mínimas e Recomendadas.
* **Filtros Adaptativos de Preço:** Lógica interna para isolar flutuações de preços da loja oficial (Steam) e descartar anomalias ou keyshops de terceiros.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.10+**
* **Scrapy Framework:** Tratamento de concorrência, pipelines e gerenciamento de requisições assíncronas.
* **Requests:** Utilizado para requisições síncronas complementares a APIs internas durante o fluxo do Spider.
* **CSS Selectors & XPath:** Motores de navegação no DOM HTML.
* **Regex (re):** Sanitização e normalização textual de metadados.

---

## 🕷️ Arquitetura dos Spiders

O projeto divide suas responsabilidades em três agentes autônomos de coleta:

| Spider | Ponto de Partida | Dados Coletados |
| :--- | :--- | :--- |
| **`chartspider`** | `steamcharts.com/top` | Coleta o ranking dos jogos mais jogados e consome a API de dados históricos de contagem de players simultâneos. |
| **`salesspider`** | `steambase.io/sales/` | Realiza paginação cronológica (2018 a 2024) capturando o nome, data de início e término de todas as promoções sazonais. |
| **`gamesspider`** | `steamcharts.com/top` | Mapeia o topo da SteamCharts, faz o cruzamento de dados dinâmico via query parameters no `gg.deals`, extrai o histórico de preços da Steam e faz o parse dos requisitos de sistema. |

---

## 📦 Instalação e Pré-requisitos

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/VitorBarateli/PI-Steam_Scraper.git
   cd steam-data-scraper
   ```
2. **Cria e ativa um ambiente virtual:**
   ```bash
   python -m venv venv
   # No Windows:
   venv\Scripts\activate
   # No Linux/Mac:
   source venv/bin/activate
   ```
3. **Instala as dependências necessárias:**
   ```bash
   pip install scrapy requests
   ```

---

## 💻 Como Executar

Para rodar os spiders e exportar os dados estruturados para arquivos locais (ex: .json ou .csv), executa os comandos abaixo na raiz do projeto:

1. **Coletar Histórico de Atividade (Players)**
   ```bash
   scrapy crawl chartspider -o dados_charts.json
   ```
2. **Coletar Histórico de Sales da Steam**
   ```bash
   scrapy crawl salesspider -o dados_sales.json
   ```
3. **Executar o Pipeline Completo (Jogos + Preços + Hardware)**
   ```bash
   scrapy crawl gamesspider -o dados_jogos.json
   ```
