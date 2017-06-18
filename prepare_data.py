#!/usr/bin/env python3
"""
Prepare a data file.
"""

import sys
import json
import pandas as pd
from typing import Optional

def get_scouts_dict():
    scouts = pd.read_csv('./data/scouts.csv')
    return dict(zip(map(lambda x: 'scout.' + x, scouts.scout), scouts.text))


def update_columns(df: pd.DataFrame, column: str, data: dict, field: str,
                   new_column: Optional[str] = None,
                   category: Optional[bool] = False):
    for item in data:
        item_name = data[item][field]
        idx = df[column] == int(item)
        df.loc[idx, column] = item_name

    if category:
        df[column] = df[column].astype('category')

    if new_column:
        df = df.rename(columns={column:new_column})

    return df


def prepare_round(round_filename):
    with open(round_filename) as f:
        full_info = json.loads(f.read())
        players = pd.io.json.json_normalize(full_info['atletas'])

        teams = full_info['clubes']
        status = full_info['status']
        positions = full_info['posicoes']

        players = players.assign(team_position = players['clube_id'])

        players = update_columns(df=players,
                                 column='team_position',
                                 data=teams,
                                 field='posicao')

        players = update_columns(df=players,
                                 column='clube_id',
                                 data=teams,
                                 field='nome',
                                 new_column='clube',
                                 category=True)

        players = update_columns(df=players,
                                 column='posicao_id',
                                 data=positions,
                                 field='nome',
                                 new_column='posicao',
                                 category=True)
        players = update_columns(df=players,
                                 column='status_id',
                                 data=status,
                                 field='nome',
                                 new_column='status',
                                 category=True)

        players = players.rename(columns=get_scouts_dict())

        return players


if __name__ == '__main__':
    players = prepare_round(sys.argv[1])
    players.to_pickle(sys.argv[2])
