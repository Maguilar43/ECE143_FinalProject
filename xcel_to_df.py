import pandas as pd 
import itertools as it

def main():
    df = pd.read_excel('excel_data/2019_data/Sp19_wk1_S.xlsx')

    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
    times= ['8', '10', '12', '2']

    col_names = combine_lists(days, times)

    if needs_formatting(df):
        df = reformat_multiple_columns(df, col_names, start=3, end=7)
        print('Fixed formatting')

    
    print(df)

def xcel_to_df(file):
    '''
    read from 2019 data and bring it into a dataframe, format if needed
    '''
    assert isinstance(file, str)
    assert file.endswith('.xlsx')
    
    df = pd.read_excel(file)

    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
    times= ['8', '10', '12', '2']

    col_names = combine_lists(days, times)

    if needs_formatting(df):
        df = reformat_multiple_columns(df, col_names, start=3, end=7)

    df = clean_df(df)
   
    return df 


def combine_lists(L1, L2, sep='-'):
    '''
    Return all combinations between two lists into one list in product format as strings

    :param L1: starting list
    :param L2: following list
    :type L1,L2: list

    :param sep: what to seperat elements of the list by
    :type  sep: char/str

    ex: 
        days = ['mon', 'tues']
        times= ['8', '10']

        >> combine_lists(days, times)
        ['mon-8', 'mon-10', 'tues-8', 'tues-10']
    '''

    assert isinstance(L1, list)
    assert isinstance(L2, list)
    assert len(L1) and len(L2)
    assert isinstance(sep, str)

    
    return [ comb[0] + sep + comb[1] for comb in it.product(L1, L2) ] 

def needs_formatting(df): 
    try: 
        col = df["Available Spaces-Mon"]
        return True
    except: 
        return False

def reformat_multiple_columns(df, labels, start=0, end=-1):
    '''
    splot columns into evenly split columns depending on labels

    :param df: dataframe to pull from 
    :type  df: pandas.DataFrame

    :param start, end: start and end column indices
    :type  start, end: int

    :param labels: new names for the columns to split
    :type  labels: list
    '''

    assert isinstance(df, pd.DataFrame)
    assert isinstance(start, int)
    assert isinstance(end, int)
    assert isinstance(labels, list)
    assert start >= 0 
    assert end > start
   
    split_size = len(labels) / (end+1 - start)
    split_size= int(split_size)

    cuts = [df.iloc[:, col] for col in range(start, end+1)]

    df = df.drop(df.iloc[:,start:end+1], axis=1)
    
    for i,el in enumerate(cuts):
        cuts[i] = reformat_single_column(el, labels[i*split_size: i*split_size + split_size])
        df = pd.concat([df, cuts[i]], axis=1)
       
    return df



def reformat_single_column(aCol, labels, aType=int):
    '''
    split a dataframe into multiple based off label input

    :param aCol: column that needs to be split into multiple
    :type  aCol: pandas.core.series.Series

    :param labels: new titles for the new columns
    :type  labels: list of strings

    :param aType: type to change the columns to
    :type  aType: python data type
    '''

    assert isinstance(aCol, pd.core.series.Series)
    assert isinstance(labels, list)
    assert labels
    assert all( isinstance(name, str) for name in labels)
    assert isinstance(aType, type)

    return aCol.str.split(expand=True).set_axis(labels, axis=1, inplace=False)

def clean_df(df):
    df.loc[:, 'Total Spaces': 'Fri-2'] = df.loc[:,'Total Spaces': 'Fri-2'].replace(to_replace= '-', value=0)
    
    return df


if __name__ == '__main__':
    main()


