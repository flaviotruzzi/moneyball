import sys
import urllib.request

import pandas as pd
from bs4 import BeautifulSoup


def url_4_round(round):
    return f'http://globoesporte.globo.com/servico/esportes_campeonato/responsivo/widget-uuid/1fa965ca-e21b-4bca-ac5c-bbc9741f2c3d/fases/fase-unica-seriea-2017/rodada/{round}/jogos.html'


def parse_match(match):
    home, visitors = match.find_all('span',
                                    class_='placar-jogo-equipes-nome')
    home = home.text
    visitors = visitors.text

    home_goals = match.find('span',
                            class_='placar-jogo-equipes-placar-mandante')
    visitor_goals = match.find('span',
                               class_='placar-jogo-equipes-placar-visitante')

    try:
        home_goals = int(home_goals.text)
        visitor_goals = int(visitor_goals.text)
    except:
        home_goals = None
        visitor_goals = None

    return home, home_goals, visitors, visitor_goals


def parse_round(round):
    html = urllib.request.urlopen(url_4_round(round)).read()

    soup = BeautifulSoup(html, 'html.parser')

    matches = [parse_match(match) for match in soup.find_all('li')]

    return pd.DataFrame(matches, columns=['home', 'home_goals', 'visitor',
                                          'visitor_goals'])

if __name__ == '__main__':
    round_id = int(sys.argv[1])
    round_df = parse_round(round_id)
    round_df.to_csv(f'matches_round_{round_id}.csv')

