'''
PART 2: Pre-processing
- Take the time to understand the data before proceeding
- Load `pred_universe_raw.csv` into a dataframe and `arrest_events_raw.csv` into a dataframe
- Perform a full outer join/merge on 'person_id' into a new dataframe called `df_arrests`
- Create a column in `df_arrests` called `y` which equals 1 if the person was arrested for a felony crime in the 365 days after their arrest date in `df_arrests`. 
- - So if a person was arrested on 2016-09-11, you would check to see if there was a felony arrest for that person between 2016-09-12 and 2017-09-11.
- - Use a print statment to print this question and its answer: What share of arrestees in the `df_arrests` table were rearrested for a felony crime in the next year?
- Create a predictive feature for `df_arrests` that is called `current_charge_felony` which will equal one if the current arrest was for a felony charge, and 0 otherwise. 
- - Use a print statment to print this question and its answer: What share of current charges are felonies?
- Create a predictive feature for `df_arrests` that is called `num_fel_arrests_last_year` which is the total number arrests in the one year prior to the current charge. 
- - So if someone was arrested on 2016-09-11, then you would check to see if there was a felony arrest for that person between 2015-09-11 and 2016-09-10.
- - Use a print statment to print this question and its answer: What is the average number of felony arrests in the last year?
- Print the mean of 'num_fel_arrests_last_year' -> pred_universe['num_fel_arrests_last_year'].mean()
- Print pred_universe.head()
- Return `df_arrests` for use in main.py for PART 3; if you can't figure this out, save as a .csv in `data/` and read into PART 3 in main.py
'''

# import the necessary packages
import pandas as pd 
import os 

def preprocess_data():
    save_dir = 'data'


# loading csv files into dataframe 
    pred_universe = pd.read_csv(os.path.join(save_dir, 'pred_universe_raw.csv'))
    arrest_events = pd.read_csv(os.path.join(save_dir, 'arrest_events_raw.csv'))

    pred_universe['arrest_date_univ'] = pd.to_datetime(pred_universe['arrest_date_univ'])
    arrest_events['arrest_date_event'] = pd.to_datetime(arrest_events['arrest_date_event'])

# full outer join/merge 

    df_arrests = pd.merge(pred_universe, arrest_events, on='person_id', how='outer')


# column y 
    def was_rearrested(row):
        arrest_date_univ = row['arrest_date_univ']
        person_id = row['person_id']
        end_date = arrest_date_univ + pd.Timedelta(days=365)
    
        felony_arrests = arrest_events[
        (arrest_events['person_id'] == person_id) &
        (arrest_events['arrest_date_event'] > arrest_date_univ) &
        (arrest_events['arrest_date_event'] <= end_date) &
        (arrest_events['charge_type_event'] == 'felony')
    ]
    return 1 if not felony_arrests.empty else 0

    df_arrests['y'] = df_arrests.apply(was_rearrested, axis=1)

#  What share of arrestees in the `df_arrests` table were rearrested for a felony crime in the next year?
    share_rearrested = df_arrests['y'].mean()
    print(f"What share of arrestees in the `df_arrests` table were rearrested for a felony crime in the next year? {share_rearrested:.2%}")

# What is the average number of felony arrests in the last year?
    df_arrests['current_charge_felony'] = df_arrests['charge_type_univ'].apply(lambda x: 1 if x == 'felony' else 0)
#  What share of current charges are felonies?
    share_current_felonies = df_arrests['current_charge_felony'].mean()
    print(f"What share of current charges are felonies? {share_current_felonies:.2%}")


# pred feature 

    def felony_arrests_last_year(row):
        arrest_date_univ = row['arrest_date_univ']
        person_id = row['person_id']
        start_date = arrest_date_univ - pd.Timedelta(days=365)
    
        felony_arrests = arrest_events[
            (arrest_events['person_id'] == person_id) &
            (arrest_events['arrest_date_event'] >= start_date) &
            (arrest_events['arrest_date_event'] < arrest_date_univ) &
            (arrest_events['charge_type_event'] == 'felony')
        ]
    return felony_arrests.shape[0]

    df_arrests['num_fel_arrests_last_year'] = df_arrests.apply(felony_arrests_last_year, axis=1)

# What is the average number of felony arrests in the last year?
    average_felony_arrests_last_year = df_arrests['num_fel_arrests_last_year'].mean()
    print(f"What is the average number of felony arrests in the last year? {average_felony_arrests_last_year:.2f}")

# Print the mean of 'num_fel_arrests_last_year'
    print(f"Mean of 'num_fel_arrests_last_year': {df_arrests['num_fel_arrests_last_year'].mean():.2f}")

# Print the head of the dataframe
    print(df_arrests.head())

# Save the dataframe as CSV for use in main.py
    df_arrests.to_csv(os.path.join(save_dir, 'df_arrests.csv'), index=False)
