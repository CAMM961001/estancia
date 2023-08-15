import os
import re

from numpy import arange
import pandas as pd

from settings import Settings


# --------------------------------------------- Process resources and constants
settings = Settings()
DATA_DIRECTORY = os.path.join(settings.ROOT, 'data', 'datos-produccion-maiz')
TIME_FRAMES = [(2005,2035), (2035,2065), (2065,2099)]

list_of_historical_files = [
    file for file in os.listdir(DATA_DIRECTORY)
    if file.startswith('hist')]


# ------------------------------------------------------------------- Main loop
print('Historical files aggregation')

for file in list_of_historical_files:
    print(f"\t{file}")

    # Open file as pandas dataframe
    input_df = pd.read_csv(
        os.path.join(DATA_DIRECTORY, file))

    # Timeframe aggregation loop
    for id_tf, _tf in enumerate(TIME_FRAMES):

        # List of years in timeframe
        years = arange(TIME_FRAMES[id_tf][0], TIME_FRAMES[id_tf][1])

        # Dataframe aggregation
        _temp_agg_data = (
            input_df
            # Filter years from timeframe
            .query("year in @years")
            # Aggregate timeframe mean by id
            .groupby(by='id')
            .mean()
            # Add timeframe index column
            .assign(
                period = '-'.join([str(val) for val in _tf]))
            # Drop year column
            .drop(columns=['year'])
            # Reset coordinate index
            .reset_index()
        )

        # Initialize dataframe with first instance of loop
        if id_tf == 0:
            output_df = _temp_agg_data
            continue

        # Concatenate rows to output dataframe
        output_df = pd.concat([output_df, _temp_agg_data], axis=0)

    # Format columns
    output_df.columns = [
        re.sub(
            pattern=r'[-\. ]'
            ,repl='_'
            ,string=colname.lower().strip())
        for colname in output_df.columns]

    # Save aggregated data as csv
    output_file_name = os.path.join(
        DATA_DIRECTORY
        ,file.replace('hist', 'agg'))
    
    output_df.to_csv(
        output_file_name
        ,index=False)
    

if __name__ == '__main__':
    pass
