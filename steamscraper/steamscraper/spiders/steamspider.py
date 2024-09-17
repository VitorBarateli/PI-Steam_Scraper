import scrapy
import requests
import re

#Links:
    # https://gg.deals/
    # https://steamcharts.com/
    # https://steambase.io/

class ChartspiderSpider(scrapy.Spider):
    name = "chartspider"
    allowed_domains = ["steamcharts.com"]
    start_urls = ["https://steamcharts.com/top"]

    def parse(self, response):
        games = response.css("div.content > table.common-table > tbody > tr")
        for game in games:
            link = game.css('td.game-name.left > a::attr(href)').get()
            yield response.follow(link, self.parse_chart)

        next_page = response.css('div.pagination > a:contains("Next")::attr(href)').get()
        if next_page is not None and next_page != '/top/p.200':
            next_page_url = 'https://steamcharts.com' + next_page
            yield response.follow(next_page_url, self.parse)

    def parse_chart(self, response):
        nome = response.css('div#content-wrapper > h1 > a::text').get()
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
            'X-Requested-With': 'XMLHttpRequest',
            'DNT': '1',
            'Sec-GPC': '1',
            'Connection': 'keep-alive',
            'Referer': response.url,
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'If-Modified-Since': 'Tue, 03 Sep 2024 11:59:13 GMT',
        }

        network_response = response = requests.get(response.url + '/chart-data.json', headers=headers)
        chart_data = network_response.json()
        chart = [line[1] for line in chart_data]

        yield{
            'Nome' : nome,
            'Charts' : chart
        }


class SalespiderSpider(scrapy.Spider):
    name = "salesspider"
    allowed_domains = ["steambase.io"]
    start_urls = ["https://steambase.io/sales/"]

    def parse(self, response):
        ano = 2018
        for ano in range(2018, 2025, 1):
            yield response.follow(str(ano), self.parse_sales)

    def parse_sales(self, response):
        nome = response.css("section.mx-auto.mb-16.flex.flex-col.items-center.space-y-8.pt-8.lg\\:pt-16 h1::text").get()
        promocoes = []
        sales = response.css('div.grid.grid-cols-1.md\\:grid-cols-2.gap-4 > a.w-full.flex.flex-col.space-y-4.justify-between.px-4.py-4.border.rounded-lg.border-slate-700.hover\\:border-blue-400')
        for sale in sales:
            name = sale.css('div > div > h3::text').get()
            date_start = sale.css('ul > li:nth-child(1)::text').get()
            date_end = sale.css('ul > li:nth-child(2)::text').get()
            promocoes.append([name, date_start, date_end])

        yield{
            'Nome' : nome.strip(),
            'Promoções' : promocoes
        }


class GamesspiderSpider(scrapy.Spider):
    name = "gamesspider"
    allowed_domains = ["steamcharts.com", "gg.deals"]
    start_urls = ["https://steamcharts.com/top"]

    def parse(self, response):
        games = response.css("div.content > table.common-table > tbody > tr")
        for game in games:
            nome = game.css('td.game-name.left > a::text').get().strip()
            nome = re.sub(r'\s+', ' ', nome)
            nome = re.sub(r'®', '', nome)
            nome = re.sub(r'™', '', nome)
            yield response.follow('https://gg.deals/games/?title=' + nome, self.parse_title, meta={'nome': nome})

        next_page = response.css('div.pagination > a:contains("Next")::attr(href)').get()
        if next_page is not None and next_page != '/top/p.200':
            next_page_url = 'https://steamcharts.com' + next_page
            yield response.follow(next_page_url, self.parse)

    def parse_title(self, response):
        nome = response.meta.get('nome')
        games = response.css('div.d-flex.flex-wrap.relative.list-items.shadow-box-small-lighter > div')
        game = games[0]
        titulo = game.css('a::text').get()

        if(titulo == nome):
            link = game.css('a::attr(href)').get()
            yield response.follow(link, self.parse_game)
        

    def parse_game(self, response):
        id = response.css('div.col-left > div::attr(data-container-game-id)').get()
        cookies = {
            'gg-session': 'bu8prtq0l3vq95s4n8hoskqc4s',
            'firstVisit': '1725106615',
            'gg_csrf': '8a2c6e66fe9b13739a093a0e7727e49288f6c4d7s^%^3A88^%^3A^%^22aEx-SGUxZFppWEFSUVltcUNQYjE0bU9lNUViVjhmS3LuxB59DhwEf3FbAQsBCWLJm7NcXkIAwywAdLVpJmWixQ^%^3D^%^3D^%^22^%^3B',
        }
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
            'X-Requested-With': 'XMLHttpRequest',
            'DNT': '1',
            'Sec-GPC': '1',
            'Connection': 'keep-alive',
            'Referer': 'https://gg.deals/game/black-myth-wukong/',
            'Sec-Fetch-Site': 'same-origin',
        }
        params = {
            'showKeyshops': '0',
        }

        nome = response.css('div.container.breadcrumbs-container > ul > li:last-child > a > span::text').get()
        lançamento = response.css('div.game-info-details-section.game-info-details-section-release > p::text').get()
        network_response = requests.get(f'https://gg.deals/br/games/chartHistoricalData/{id}', params=params, cookies=cookies, headers=headers)
        precos = network_response.json()
        precos = precos['chartData']['retail']

        steam_found = any(preco.get('shop') == 'Steam' for preco in precos)
        valor = any(preco.get('y') == 0 for preco in precos)
        
        if steam_found:
            precos_steam = [item for item in precos if item['shop'] == 'Steam']
            precos_steam = [
                {key: value for key, value in item.items() if key not in ['x', 'shop']}
                for item in precos_steam
            ]
            if valor:
                if len(precos_steam) >= 2:
                    precos_steam = [precos_steam[-2]]
        elif valor:
            precos = [preco for preco in precos if preco.get('y') == 0]
            if len(precos) >= 2:
                    precos_steam = [precos[-2]]
            else:
                precos_steam = [precos[0]]

            precos_steam = [
                {key: value for key, value in item.items() if key not in ['x', 'shop']}
                for item in precos_steam
            ]
        else:
            precos_steam = precos
            precos_steam = [
                {key: value for key, value in item.items() if key not in ['x', 'shop']}
                for item in precos_steam
            ]

        if len(precos_steam) == 2:
            penultimo_item = precos_steam[-2]
            ultimo_item = precos_steam[-1]

            if penultimo_item['y'] == ultimo_item['y']:
                precos_steam = [penultimo_item]
        
        cpu_min =  response.xpath("//div[strong[contains(text(), 'Minimum:')]]//ul[@class='bb_ul']/li[strong[contains(text(), 'Processor')]]/text()").get()  
        gpu_min = response.xpath("//div[strong[contains(text(), 'Minimum:')]]//ul[@class='bb_ul']/li[strong[contains(text(), 'Graphics')]]/text()").get()  
        ram_min = response.xpath("//div[strong[contains(text(), 'Minimum:')]]//ul[@class='bb_ul']/li[strong[contains(text(), 'Memory')]]/text()").get()  
        config_minima = [cpu_min, gpu_min, ram_min]

        cpu = response.xpath("//div[strong[contains(text(), 'Recommended:')]]//ul[@class='bb_ul']/li[strong[contains(text(), 'Processor')]]/text()").get()  
        gpu = response.xpath("//div[strong[contains(text(), 'Recommended:')]]//ul[@class='bb_ul']/li[strong[contains(text(), 'Graphics')]]/text()").get()  
        ram = response.xpath("//div[strong[contains(text(), 'Recommended:')]]//ul[@class='bb_ul']/li[strong[contains(text(), 'Memory')]]/text()").get()  
        config_recomendada = [cpu, gpu, ram]

        if precos_steam:
            yield{
                'Nome': nome,
                'Preços': precos_steam,
                'Configuração Mínima' : config_minima,
                'Configuração Recomendada' : config_recomendada,
                'Data de Lançamento' : lançamento
            }