from xcel_to_df import xcel_to_df, combine_lists
from statistics import mode
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd 
import math
import os
import re 




def main():
    '''
    frame_dictionary
    |
    |
    |---A---|
    |       |----Winter 19----|
    |       |                 |
    |       |                 |----Week 1
    |       |                 |
    |       |                 |----Week 2
    |       |                
    |       |
    |       |----Spring 19----|
    |       
    |---B---|     


    '''

    frame_dictionary = collect_dictionary()

    get_peak_percentages(frame_dictionary)

  

   

    lot, values = get_best_lot_times(frame_dictionary, 'S', 'Mon')

    print(lot, values)

    plt.bar(['8am', '10am', '12pm', '2pm'], values)
    plt.title('Open Student Parking for Lot '+lot)
    plt.xlabel('Time of Day')
    plt.ylabel('Number of Open Spaces')
    plt.savefig('images/best_lot.png')
   

    # plt.bar([[l8[0], l10[0], l12[0], l2[0]], [l8[1], l10[1],l12[1], l2[1]])
    # plt.title('Student Spots on Mondays')
    # plt.savefig('test.png')
  
    
    #find best lots throughout the day? best spot for 8am-2pm

def collect_dictionary():
    '''
    Here is where we hand pick the dataframes we want to work with and 
    return them in an orderly manner
    '''
    path = 'excel_data/2019_data/'
    d = {}

    for filename in os.listdir(path):
        df = xcel_to_df(path+filename)
        direct = re.split('[_ .]',filename)
        quarter = direct[0]
        week = direct[1]
        pType= direct[2]

        if pType not in d: 
            d[pType] = {quarter: {week: df} }

        else: 
            if quarter not in d[pType]: 
                d[pType][quarter] = {week: df}
            
            else: 
                d[pType][quarter][week] = df
        
    return d

def get_best_lot_times(aDict, aType, aDay):
    '''
    Find the best lot on a specific day for a specified type of lot 

    :param aDict: dictionary formed from collect_dictionary for all lots
    :type  aDict: dict

    :param aType: single character representing the type of space user is looking forl
    :type  aType: str / chr

    :param aDay: the day of the week the user is looking for ['Mon', 'Tue', ...]
    :type  aDay: str     
    '''
    assert isinstance(aDict, dict)
    assert isinstance(aType, str)
    assert isinstance(aDay, str)
    assert aType.isalpha() and aType.isupper()
    assert len(aDay) == 3

    times = [8, 10, 12, 2]

    col_names = [ aDay+'-'+str(time) for time in times ]

    best_lots = [find_best_lot(aDict, aType, aDay, time) for time in times]

    lots = [el[0] for el in best_lots]
    max_times = [el[1] for el in best_lots]
    max_times = np.array(max_times)

    try:
        top_lot = mode(lots)
    except:
        best_time_idx = np.argmax(max_times)
        top_lot = lots[best_time_idx]

    df = aDict[aType]['Sp19']['wk2']
    
    try: 
        row = df[df['Structure'] == top_lot]
        if row.empty:
            raise ValueError
    except:
        row = df.loc[df['Lot'] == top_lot]

    vals = row.loc[:, col_names[0]: col_names[-1]]
    vals = vals.values.tolist()[0]

    return top_lot, vals
        


def find_best_lot(aDict, aType, aDay, aTime):
    '''
    With given parameters, return the lot name for a specific spot type, day, and time
    that has the most amount of available spots

    :param aDict: dictionary formed from collect_dictionary for all lots
    :type  aDict: dict

    :param aType: single character representing the type of space user is looking forl
    :type  aType: str / chr

    :param aDay: the day of the week the user is looking for ['Mon', 'Tue', ...]
    :type  aDay: str 

    :param aTime: time of day the user is looking for [8, 10, 12, 2]
    :type  aTime: int
    '''
    assert isinstance(aDict, dict)
    assert isinstance(aType, str)
    assert isinstance(aDay, str)
    assert isinstance(aTime, int)
    assert aType.isalpha() and aType.isupper()
    assert len(aDay) == 3
    assert 0 < aTime

    lot = 'aLot'
    n_spots = 0

    col = aDay + '-' + str(aTime)

    type_dict = aDict[aType]
    

    for quarter in type_dict: 
        
        for week in type_dict[quarter]: 
            df = type_dict[quarter][week]

            max_in_col = int(df[col].max())

            if max_in_col > n_spots: 
                n_spots = max_in_col
                idx = df[col].idxmax()
                row = df.iloc[idx]

                try:
                    checker = math.isnan(row['Structure'])
                    lot = row['Lot'] if checker else row['Structure']
                except:
                    checker = row['Structure']=='NaN' or row['Structure'] == "nan"
                    lot = row['Lot'] if checker else row['Structure']

                


    return (lot, n_spots )

def get_peak_percentages(frame_dict):
    '''
    Return the dictionary for max peak time percentages per quarter per spot

    - find min of row between mon-fri 
    - max full is ( total - min_row )
    - percent_full = sum(row_full) / sum(total_spaces)
    - take average of weeks, return per type per quarter
    '''
    assert isinstance(frame_dict, dict) 

    percent_occupied = {
        'A': {  'Win19': 0,
                'Sp19' : 0},
        'B': {  'Win19': 0,
                'Sp19' : 0},
        'S': {  'Win19': 0,
                'Sp19' : 0},
        'V': {  'Win19': 0,
                'Sp19' : 0},
    }

    for pType in frame_dict: 
        for quarter in frame_dict[pType]:
            space_total = 0
            occupied_total = 0
            for week in frame_dict[pType][quarter]:
                df = frame_dict[pType][quarter][week]
                space_total += df['Total Spaces'].sum()

                times = [0] * 5 # 8am, 10am, 12pm, 2pm
            

                days_by_time = df.iloc[:, 3:] # gets mon-8 --> fri-2

                for i in range(0,4): # 0-4 relates to 8am-2pm cuts
                    at_time = days_by_time.iloc[:, [i, i+4, i+8, i+12, i+16]].astype('float64').mean(axis=1)
                    times[i] = at_time
                    
                data = {'8': times[0], '10': times[1], '12': times[2], '2': times[3]}
                time_df = pd.DataFrame(data)


                occupied_total += (df['Total Spaces'] - time_df.min(axis=1) ).sum()
              
    
            percent_occupied[pType][quarter] = occupied_total / space_total

    return percent_occupied



if __name__ == '__main__':
    main()