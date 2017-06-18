#!/usr/bin/env python3
import sys
import json
import pandas as pd


def round_score(round_num):
    previous_round = round_num - 1
    previous_market_file = f'./data/mercado-rodada-{previous_round}/mercado-rodada-{previous_round}.json'
    previous_market = json.loads(open(previous_market_file).read())
    df_previous = pd.read_json(json.dumps(previous_market['atletas'])).set_index('atleta_id')

    market_file = f'./data/mercado-rodada-{round_num}/mercado-rodada-{round_num}.json'
    market = json.loads(open(market_file).read())
    df = pd.read_json(json.dumps(market['atletas'])).set_index('atleta_id')

    for index, row in df.iterrows():
        if index in df_previous.index:
            scout = row['scout']
            scout_previous = df_previous.loc[index]['scout']
            if type(scout) is dict and type(scout_previous) is dict:
                scout_diff = {key: scout[key] - scout_previous.get(key, 0) for key in scout.keys()}
                df.set_value(index, 'scout', scout_diff)
    return df

if __name__ == '__main__':
    round = int(sys.argv[1])
    players_score = round_score(round)
    players_score.to_csv(f'data/players-score-round-{round - 1}.csv')
    players_score.to_pickle(f'data/players-score-round-{round - 1}.bz2')
