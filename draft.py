import pandas as pd
from utils.prepare_data import *

from sklearn import *
from pylab import *


rounds = list(map(prepare_round,
             ['./data/players-score-round-1.bz2',
              './data/players-score-round-2.bz2',
              './data/players-score-round-3.bz2',
              './data/players-score-round-4.bz2',
              './data/players-score-round-5.bz2',
              './data/players-score-round-6.bz2',
              './data/players-score-round-7.bz2']))

parameters, _ = get_valid_scouts(rounds[0])

parameters.extend(['points',
                   'team_position',
                   'status_code'])
models = {}
for position in ['midfielder', 'striker', 'goalkeeper', 'defender', 'coach',
                 'fullback']:
    players = list(map(lambda x: get_data_for_position(x, position), rounds))

    for i in range(1,5):
        players[i-1]['next_points'] = players[i][players[i].player_id.eq(players[i-1].player_id)].points
        players[i-1]['round'] = str(i - 1)
        players[i-1].reset_index()

    all_data = pd.concat(players[:-1], axis=0)

    all_data['id'] = all_data['player_id'].apply(str) + all_data['round']

    train_sample = all_data.sample(frac=0.7)
    test_sample = all_data[~all_data.id.isin(train_sample.id)]

    reg = linear_model.ElasticNet()

    reg.fit(all_data[parameters].fillna(0),
            all_data['next_points'].fillna(0))

    predicted = reg.predict(players[-1][parameters].fillna(0))

    for_position = players[-1]
    for_position['next_points'] = predicted
    for_position = for_position.sort_values(by='next_points')

    print(f'{20 * "*"} {position} {20 * "*"}')
    print(for_position[['nickname', 'team', 'next_points']].tail(10))

    models[position] = for_position
