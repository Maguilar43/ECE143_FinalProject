import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.dates as md
import datetime as dt   
from find_parking import collect_dictionary
from xcel_to_df import xcel_to_df

def main():

    # quarter = 'Spring'
    # ax = compare_university(quarter)

    dist_2000 = get_spot_distribution(2000)
    dist_2015 = get_spot_distribution(2015)
    dist_2019 = get_spot_distribution(2019)

    plt.subplot(1, 3, 1)
    plt.pie(dist_2000, autopct='%1.0f%%', colors=['red', 'green', '#FFC133', 'gray'])
    plt.title('Year 2000')

    plt.subplot(1, 3, 2)
    plt.pie(dist_2019, autopct='%1.0f%%',  colors=['red', 'green', '#FFC133', 'gray'])
    plt.title('Year 2019')

    plt.subplot(1, 3, 3)
    plt.pie(dist_2015, autopct='%1.0f%%',  colors=['red', 'green', '#FFC133', 'gray'])
    plt.title('Year 2015')


    plt.legend(['Admin (A)', 'Grad (B)', 'Student (S)', 'Visitor (V)'], loc = 'lower left', bbox_to_anchor=(-0.4, -.24, 0.5, 0.5))
    plt.savefig('../images/Spot Distributions', dpi=300)
    

    # ax.plot()
    # plt.yticks(np.arange(50, 101, step=10))
    # plt.title('University Parking Trends (2000-2019) -- '+quarter+' Quarters', fontsize=18)
    # plt.ylabel('Percent Full')
    # plt.xlabel('Year')
# 
    # plt.legend(loc = 'lower right')
    # plt.xticks(range(2000, 2020))
    # plt.locator_params(axis='x', nbins=10)
# 
    # plt.savefig('../images/'+quarter+'_history.png')
    
def compare_university(quarter_name):
    '''
    Shows A,B,S, V usage trends through all years for a specified quarter

    :param quarter_name: What quarter to view the trends throughout all years
    :type  quarter_name: str
    '''
    assert isinstance(quarter_name, str)

    quarters = ['Spring', 'Winter', 'Fall']
    assert quarter_name in quarters

    frame_dict = collect_dictionary()
    percentage_dict = get_peak_percentages(frame_dict)


    letter = ['A', 'B', 'S', 'V']
    label = ['Admin', 'Grad', 'Student', 'Visitor']
    color = ['r', 'g', 'y', 'k']
    marker= [':', '-.', '-', '--']

    dfA = pd.read_csv('../csv_data/University-wide/University_of_California,_San_Diego__A_Parking_Spaces.csv')
    dfB = pd.read_csv('../csv_data/University-wide/University_of_California,_San_Diego__B_Parking_Spaces.csv')
    dfS = pd.read_csv('../csv_data/University-wide/University_of_California,_San_Diego__S_Parking_Spaces.csv')
    dfV = pd.read_csv('../csv_data/University-wide/University_of_California,_San_Diego__Visitor_Parking_Spaces.csv')

    frames = [dfA, dfB, dfS, dfV]

    f, ax = plt.subplots(figsize=(10,5))

    for i, frame in enumerate(frames):
        l = [0] * (2020 - 2000)
        

        frame = frame[frame['quarter'] == quarter_name]
        fill = frame.loc[:, ['quarter', '%_occupied']]
        l[0:16] = list(fill['%_occupied'])
        
        

        l[15:19] = [None] * 4

        if quarter_name == 'Winter': 
            l[-1] = percentage_dict[letter[i]]['Win19']
        elif quarter_name ==  'Spring':
            l[-1] = percentage_dict[letter[i]]['Sp19']

    

        series1 = np.array(l).astype(np.double) * 100 #turn into percent values
        s1mask = np.isfinite(series1)

        s2 = list(range(2000, 2020))
    
        s2[15:19] = [None] * 4

        s2 = np.array(s2).astype(np.double)
        s2mask = np.isfinite(s2)

        ax.plot(s2[s2mask],series1[s1mask], color[i] , label= label[i], linestyle = marker[i], linewidth=3) #stackoverflow: connect lines betwenn 'None'

    return ax

def get_spot_distribution(year):
    '''
    For a specified year, get the University's spot distribution by type of 
    parking spot.

    :param year: what year to look at spot distributions
    :type  year: int

    Returns list of percentages in order of [A, B, S, V]
    '''
    assert isinstance(year, int)
    assert 1999 < year < 2016 or year==2019 , "Year not in dataset"

    if year < 2016: 
    
        dfA = pd.read_csv('../csv_data/University-wide/University_of_California,_San_Diego__A_Parking_Spaces.csv')
        dfB = pd.read_csv('../csv_data/University-wide/University_of_California,_San_Diego__B_Parking_Spaces.csv')
        dfS = pd.read_csv('../csv_data/University-wide/University_of_California,_San_Diego__S_Parking_Spaces.csv')
        dfV = pd.read_csv('../csv_data/University-wide/University_of_California,_San_Diego__Visitor_Parking_Spaces.csv')

        frames = [dfA, dfB, dfS, dfV]

        total_spaces = 0
        type_totals = np.zeros(4)

        frame_year_idx = (year-2000) * 3 # 3 quarters in each year, so skips every 3 to get to new year 

        for i,frame in enumerate(frames): 
        
            type_totals[i] = frame.iloc[frame_year_idx]['parking_spaces']
            total_spaces += type_totals[i]

    elif year == 2019: 
        dfA = xcel_to_df('../excel_data/2019_data/Sp19_wk2_A.xlsx')
        dfB = xcel_to_df('../excel_data/2019_data/Sp19_wk2_B.xlsx')
        dfS = xcel_to_df('../excel_data/2019_data/Sp19_wk2_S.xlsx')
        dfV = xcel_to_df('../excel_data/2019_data/Sp19_wk2_V.xlsx')

        frames = [dfA, dfB, dfS, dfV]
        total_spaces = 0
        type_totals = np.zeros(4)

        for i,frame in enumerate(frames): 

            type_totals[i] = frame.loc[:, 'Total Spaces'].sum()
            total_spaces += type_totals[i]

    else: 
        assert 0 , "Year couldn't be found in dataset"


    return type_totals / total_spaces

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