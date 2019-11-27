from xcel_to_df import xcel_to_df
import pandas as pd 
import os
import re 


def main():
    '''
    frame_dictionary
    |
    |
    |---A----|
    |        |----Winter 19-----
    |        |                 |
    |        |                 |----Week 1
    |        |                 |
    |        |                 |----Week 2
    |        |                
    |        |
    |        |----Spring 19----|
    |       
    |---B---     


    '''

    frame_dictionary = collect_dictioary()
    print(frame_dictionary)

def collect_dictioary():
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
    


if __name__ == '__main__':
    main()