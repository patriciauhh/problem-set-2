
'''
PART 1: ETL the two datasets and save each in `data/` as .csv's
'''

import pandas as pd 
import os 

def perform_etl():

    save_dir = 'data'
    os.makedirs(save_dir, exist_ok=True)

    pred_universe_raw = pd.read_csv('src/universe_lab6.feather')
    arrest_events_raw = pd.read_csv('src/arrest_events_lab6.feather')

    pred_universe_raw['arrest_date_univ'] = pd.to_datetime(pred_universe_raw['filing_date'])
    arrest_events_raw['arrest_date_event'] = pd.to_datetime(arrest_events_raw['filing_date'])


    pred_universe_raw.drop(columns=['filing_date'], inplace=True)
    arrest_events_raw.drop(columns=['filing_date'], inplace=True)


    pred_universe_raw.to_csv(os.path.join(save_dir, 'pred_universe_raw.csv'), index=False)
    arrest_events_raw.to_csv(os.path.join(save_dir, 'arrest_events_raw.csv'), index=False)

    print(f"Files saved in {save_dir} directory.")

