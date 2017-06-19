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


def get_positions_dict():
    positions = pd.read_csv('./data/positions.csv', index_col=0)
    return positions.to_dict()['position']


def get_status_dict():
    status = pd.read_csv('./data/status.csv', index_col=0)
    return status.to_dict()['status']

def update_columns(df: pd.DataFrame, column: str, data: dict, field:
                   Optional[str] = None,
                   new_column: Optional[str] = None,
                   category: bool = False):
    """
    Update column [column] of dataframe [df] using data [data] contained
    inside field [field]. Update name of column if new_column is
    specified, set column type to category if category is specified with
    True.
    """
    for key, value in data.items():
        item_name = value
        if field:
            item_name = item_name[field]
        idx = df[column] == int(key)
        df.loc[idx, column] = item_name

    if category:
        df[column] = df[column].astype('category')

    if new_column:
        df = df.rename(columns={column:new_column})

    return df


def prepare_round(round_filename):
    """
    Read data from the rounds adapting column names and normalizing.
    """
    with open(round_filename) as f:
        full_info = json.loads(f.read())
        players = pd.io.json.json_normalize(full_info['atletas'])

        teams = full_info['clubes']
        status = get_status_dict()
        positions = get_positions_dict()

        players = players.assign(team_position = players['clube_id'])

        players = update_columns(df=players,
                                 column='team_position',
                                 data=teams,
                                 field='posicao')

        players = update_columns(df=players,
                                 column='clube_id',
                                 data=teams,
                                 field='nome',
                                 new_column='team',
                                 category=True)

        players = update_columns(df=players,
                                 column='posicao_id',
                                 data=positions,
                                 new_column='position',
                                 category=True)

        players = update_columns(df=players,
                                 column='status_id',
                                 data=status,
                                 new_column='status',
                                 category=True)

        players = players.rename(columns={'atleta_id': 'player_id',
                                          'nome': 'name'})
        #players = players.rename(columns=get_scouts_dict())

        return players


if __name__ == '__main__':
    players = prepare_round(sys.argv[1])
    players.to_pickle(sys.argv[2])
