import pandas as pd
from utils.prepare_data import *


old_round = prepare_round('./data/mercado-rodada-2/mercado-rodada-2.json')

new_round = prepare_round('./data/mercado-rodada-3/mercado-rodada-3.json')

# Priors per position
strikers_old = get_data_for_position(new_round, 'striker')
strikers_new = get_data_for_position(new_round, 'striker')

parameters, _ = get_valid_scouts(strikers_old)

parameters.extend(['points',
                   'team_position',
                   'status_code'])

strikers_new['status_code'] = strikers_new['status'].cat.codes
strikers_old['status_code'] = strikers_old['status'].cat.codes


strikers_old['next_points'] = strikers_new[strikers_new.player_id==strikers_old.player_id].points

train_sample = strikers_old.sample(frac=0.7)
test_sample = strikers_old[~strikers_old.player_id.isin(train_sample.player_id)]





