# read files by s, b, a. find area with best probability at a certain time
# 1. collect all by s, b, or a 
# 2. how have peak times changed
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.dates as md
import datetime as dt   

def main():
    pass

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

    dfA = dfA[dfA['quarter'] != 'Summer']
    dfB = dfB[dfB['quarter'] != 'Summer']
    dfS = dfS[dfS['quarter'] != 'Summer']
    
    a_fill = dfA.loc[:,['quarter', '%_occupied']]
    b_fill = dfB.loc[:, ['quarter', '%_occupied']]
    s_fill = dfS.loc[:, ['quarter', '%_occupied']]

    plt.plot(np.arange(len(a_fill['quarter'])),a_fill['%_occupied'], 'r')
    plt.plot(np.arange(len(a_fill['quarter'])),b_fill['%_occupied'], 'g')
    plt.plot(np.arange(len(a_fill['quarter'])),s_fill['%_occupied'], 'y')
    
    print(len(a_fill['quarter']))
    
    plt.xticks(np.arange(len(a_fill['quarter'])), a_fill['quarter'], rotation=90)
    
    
if __name__ == '__main__':
    main()