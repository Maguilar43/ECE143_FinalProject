# read files by s, b, a. find area with best probability at a certain time
# 1. collect all by s, b, or a 
# 2. how have peak times changed
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.dates as md
import datetime as dt   
from find_parking import *

def main():
    compare_university()

def where_to_park(quarter='Fall', time='10am', spot_type='S'):
    '''
    Based on past data, which area of campus are you most likeley to find a spot 
    at? Provide the user with a few visuals so they can determine where they 
    would like to go to
    
    Note:   I will work on this in this application later, I just want to get what
            I have up on github incase we can't all meet with the TA together
                -Matthew
    '''
    pass
    
def view_quarter_peaks():
    '''
    See how the peak times change for a specific quarter through the years
    
    NOTE:   This visualization seems confusing and will probably not be used or
            the visualization should be changed before use. 
                -Matthew
    '''
    df = pd.read_csv('csv_data/University-wide/University_of_California,_San_Diego__A_Parking_Spaces.csv')
    fall = df.loc[df['quarter'] == 'Spring']
    f_times = fall.loc[:,'8am':'5pm']
    years = fall.loc[:, 'year'].values
  
    s_yr = []
    
    for el in years:      
        s_yr.append(el[2:el.find('/')]) # change 2000/01 --> 00 for all years
        
    
    str_times = f_times.idxmin(axis=1) # returns the column where the Peak time occurs

    fixed = ['12pm' if el=='12am' else el for el in str_times]

    peak_times = pd.to_datetime(fixed, format='%I%p')
  
    df = pd.DataFrame({'peak':peak_times.values, 'year' : s_yr})
     
    plt.plot(df.year, df.peak)
    plt.xticks(s_yr)

def compare_university():
    '''
    Shows A,B,S usage trends through all years and quarters of data (Summer Excluded)
    '''
    dfA = pd.read_csv('csv_data/University-wide/University_of_California,_San_Diego__A_Parking_Spaces.csv')
    dfB = pd.read_csv('csv_data/University-wide/University_of_California,_San_Diego__B_Parking_Spaces.csv')
    dfS = pd.read_csv('csv_data/University-wide/University_of_California,_San_Diego__S_Parking_Spaces.csv')
    dfV = pd.read_csv('csv_data/University-wide/University_of_California,_San_Diego__Visitor_Parking_Spaces.csv')

    dfA = dfA[dfA['quarter'] != 'Summer']
    dfB = dfB[dfB['quarter'] != 'Summer']
    dfS = dfS[dfS['quarter'] != 'Summer']
    dfV = dfV[dfV['quarter'] != 'Summer']
    
    a_fill = dfA.loc[:,['quarter', '%_occupied']]
    b_fill = dfB.loc[:, ['quarter', '%_occupied']]
    s_fill = dfS.loc[:, ['quarter', '%_occupied']]
    v_fill = dfV.loc[:, ['quarter', '%_occupied']]

    frame_dict = collect_dictionary()
    percentage_dict = get_peak_percentages(frame_dict)

    aList = list(a_fill['%_occupied'])
    bList = list(b_fill['%_occupied'])
    sList = list(s_fill['%_occupied'])
    vList = list(v_fill['%_occupied'])

    aList.append(percentage_dict['A']['Win19'])
    aList.append(percentage_dict['A']['Sp19'])
    bList.append(percentage_dict['B']['Win19'])
    bList.append(percentage_dict['B']['Sp19'])
    sList.append(percentage_dict['S']['Win19'])
    sList.append(percentage_dict['S']['Sp19'])
    vList.append(percentage_dict['V']['Win19'])
    vList.append(percentage_dict['V']['Sp19'])

    plt.figure(figsize=(10,5))

    plt.plot(np.arange(len(a_fill['quarter'])+2),aList, 'r', label="Admin")
    plt.plot(np.arange(len(a_fill['quarter'])+2),bList, 'g', label='Grad')
    plt.plot(np.arange(len(a_fill['quarter'])+2),sList, 'y', label='Student')
    plt.plot(np.arange(len(a_fill['quarter'])+2),vList, 'k', label='Visitor')

    plt.yticks(range(2))
    plt.title('University Parking Spaces Usage Trends (2000-2019)')
    

    plt.legend()
    
    # plt.xticks(np.arange(len(a_fill['quarter'])), a_fill['quarter'], rotation=90)

    plt.savefig('images/historical.png')
    
    
if __name__ == '__main__':
    main()