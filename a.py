import pandas as pd
from prepare_data import *

scouts = pd.read_csv('./data/scouts.csv')

new_round = prepare_round('./data/mercado-rodada-2/mercado-rodada-2.json')

valid_scouts = [s for s in scouts['text'] if s in new_round.keys()]

used_fields = ['nome', 'clube', 'status'] + valid_scouts

new_round = new_round[used_fields]
