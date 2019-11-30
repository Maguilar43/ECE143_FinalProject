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

    quarter = 'Spring'
    ax = compare_university(quarter)

    ax.plot()
    plt.yticks(np.arange(50, 101, step=10))
    plt.title('University Parking Trends (2000-2019) -- '+quarter+' Quarters')
    plt.ylabel('Percent Full')
    plt.xlabel('Year')

    plt.legend(loc = 'lower right')
    plt.xticks(range(2000, 2020))
    plt.locator_params(axis='x', nbins=10)

    plt.savefig('images/'+quarter+'_history.png')
    

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

def compare_university(quarter_name):
    '''
    Shows A,B,S usage trends through all years and quarters of data (Summer Excluded)
    '''
    frame_dict = collect_dictionary()
    percentage_dict = get_peak_percentages(frame_dict)


    letter = ['A', 'B', 'S', 'V']
    label = ['Admin', 'Grad', 'Student', 'Visitor']
    color = ['r', 'g', 'y', 'k']
    marker= [':', '-.', '-', '--']

    dfA = pd.read_csv('csv_data/University-wide/University_of_California,_San_Diego__A_Parking_Spaces.csv')
    dfB = pd.read_csv('csv_data/University-wide/University_of_California,_San_Diego__B_Parking_Spaces.csv')
    dfS = pd.read_csv('csv_data/University-wide/University_of_California,_San_Diego__S_Parking_Spaces.csv')
    dfV = pd.read_csv('csv_data/University-wide/University_of_California,_San_Diego__Visitor_Parking_Spaces.csv')

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

    

        series1 = np.array(l).astype(np.double) * 100
        s1mask = np.isfinite(series1)

        s2 = list(range(2000, 2020))
    
        s2[15:19] = [None] * 4

        s2 = np.array(s2).astype(np.double)
        s2mask = np.isfinite(s2)

        ax.plot(s2[s2mask],series1[s1mask], color[i] , label= label[i], linestyle = marker[i], linewidth=3)

    return ax


    
    
if __name__ == '__main__':
    main()