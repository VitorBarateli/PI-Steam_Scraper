# Steam Data Scraper

## Descrição
Projeto de web scraping desenvolvido para coletar e integrar dados de jogos da plataforma Steam a partir de múltiplas fontes. O sistema utiliza spiders para extrair informações como número de jogadores, histórico de preços, promoções e requisitos de sistema.

Os dados são obtidos de sites como SteamCharts e GG.deals, combinando diferentes informações para gerar uma visão mais completa sobre os jogos.

---

## Tecnologias
- Python
- Scrapy
- Requests
- CSS Selectors
- XPath

---

## Funcionalidades
- Coleta de dados dos jogos mais jogados da Steam
- Extração de histórico de jogadores (SteamCharts)
- Coleta de promoções e eventos (SteamBase)
- Extração de preços históricos (GG.deals)
- Extração de requisitos mínimos e recomendados
- Integração de dados de múltiplas fontes

---

## Spiders disponíveis

O projeto possui múltiplos spiders, cada um com uma responsabilidade:

- **chartspider**  
  Coleta dados de jogadores simultâneos e histórico de atividade dos jogos

- **salesspider**  
  Coleta informações sobre promoções e eventos da Steam ao longo dos anos

- **gamesspider**  
  Integra dados de diferentes fontes, incluindo preços históricos, configurações de hardware e informações gerais dos jogos

---

## Como executar o projeto

### Instalação
```bash
pip install scrapy
```

### Execução
```bash
scrapy crawl chartspider
scrapy crawl salesspider
scrapy crawl gamesspider