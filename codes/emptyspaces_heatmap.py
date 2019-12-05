import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
from xcel_to_df import xcel_to_df, combine_lists, needs_formatting, reformat_multiple_columns

def find_19_dataframe(file_prefix, quarter):
    '''

    This function is used to get 2019 dataframe into the format
    previous dataftame is and use it to get the heatmap

    :param file_prefix: str, the prefix of our file
    :param quarter: str, the quarter of this data
    :return: dict, a dict of dataframe denotes 2019 Spring and Winter datas
    '''

    assert isinstance(file_prefix, str)
    assert isinstance(quarter, str)

    prefix = '../excel_data/2019_data/'
    files = os.listdir(prefix)
    
    dict_list = []

    # Every single file in 2019 data folder will result a dataframe,
    # we convert that dataframe to dictionary and use a list to store
    # all those dictionaries
    for file in files:
        if file.startswith(file_prefix):

            # Using methods in the xcel_to_df file to get the original dataframe
            df = pd.read_excel(prefix + file)
            days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
            times= ['8', '10', '12', '2']
            col_names = combine_lists(days, times)
            if needs_formatting(df):
                df = reformat_multiple_columns(df, col_names, start=3, end=7)
                print('Fixed formatting')

            # Modify the original dataframe to format it to the same format as we
            # use in the previous dataframe
            df_19 = df.drop(columns=['Structure', 'Lot'])
            positions = ['8am', '10am', '12pm', '2pm']

            df_19['8am'] = [0 for i in range(0, len(df_19))]
            df_19['9am'] = [0 for i in range(0, len(df_19))]
            df_19['10am'] = [0 for i in range(0, len(df_19))]
            df_19['11am'] = [0 for i in range(0, len(df_19))]
            df_19['12pm'] = [0 for i in range(0, len(df_19))]
            df_19['1pm'] = [0 for i in range(0, len(df_19))]
            df_19['2pm'] = [0 for i in range(0, len(df_19))]
            df_19['3pm'] = [0 for i in range(0, len(df_19))]
            df_19['4pm'] = [0 for i in range(0, len(df_19))]
            df_19['5pm'] = [0 for i in range(0, len(df_19))]

            for time, pos in zip(times, positions):
                for day in days:
                    df_19[pos] += df_19[day + '-' + time].astype(float) / 5.0
                    df_19 = df_19.drop(columns=[day + '-' + time])

            # For the missing hours, we use the average and the ratio to predict it
            df_19['9am'] = (df_19['8am'] + df_19['10am']) / 2.0
            df_19['11am'] = (df_19['10am'] + df_19['12pm']) / 2.0
            df_19['1pm'] = (df_19['12pm'] + df_19['2pm']) / 2.0
            df_19['3pm'] = (df_19['10am']) * 0.9
            df_19['4pm'] = (df_19['9am']) * 0.9
            df_19['5pm'] = (df_19['8am']) * 0.9

            df_19 = df_19.sum()

            df_19['date'] = '2019 ' + quarter
            df_19['year'] = '2019'
            df_new_dict = df_19.to_dict()
            df_new_dict.pop('Total Spaces')

            # We put all A,B,S,V parking data into one the dataframe dictionary
            dict_list.append(df_new_dict)
    return dict_list

def get_df(filename):
    '''

    Use the find_19_dataframe method to get the real corresponding
    dataframe for spring and winter data of 2019

    :param filename: str, the file we want to extract data
    :return: dataframe, list, the useful dataframe and also a list to represent our quarters' order
    '''

    assert isinstance(filename, str)


    file_list = [ 'Win19_wk2','Sp19_wk2']
    quarter_list = ['Winter', 'Spring']

    dict_list = [find_19_dataframe(x, y) for x, y in zip(file_list, quarter_list)]

    # Combine A,B,S,V data of our dictionary into one total dataframe
    data_list = []
    for i in dict_list:
        for j in i[0]:
            if isinstance(i[0][j], str):
                continue
            for idx in range(1, len(i)):
                i[0][j] += i[idx][j]
        data_list.append(i[0])

    # Preprocess the previous years dataframe and choose just 2000,2004,2010,2014 and 2019 data
    prefix = '../csv_data/University-Wide/'
    df_University_Wide = pd.read_csv(prefix + filename)
    df_useful = df_University_Wide
    df_useful['date'] = df_useful['year'] + " " + df_useful['quarter']
    remain = ['8am','9am','10am','11am','12pm','1pm','2pm','3pm','4pm','5pm','date','year']
    df_useful = df_useful[remain]

    for data in data_list:
        df_useful.loc[len(df_useful) + 1] = data
    s = ['8am','9am','10am','11am','12pm','1pm','2pm','3pm','4pm','5pm']
    df_temp = df_useful.drop(columns = s, axis = 1)
    df_temp = df_temp.loc[(df_temp.year == '2000/01') | (df_temp.year == '2004/05') | (df_temp.year == '2010/11') | (df_temp.year == '2014/15') | (df_temp.year == '2019')]
    order = df_temp['date'].to_list()

    # Makes everyday's times as the new columns of our new dataframe
    df_temp = df_temp.join(df_useful[s].stack().reset_index(level = 1, drop = True).rename('empty_spaces'))
    df_temp = df_temp.reset_index(drop = True)

    time_list = [s[i % 10] for i in range(0,len(df_temp))]
    df_temp['time'] = time_list

    return df_temp,order

def get_figure():
    '''

    This method is used to pick up useful data from our dataframe and then
    plot the empty spaces heatmap and save it

    :return: None
    '''

    # Using time, date and empty_spaces as three parameters for our heatmap
    s = ['8am', '9am', '10am', '11am', '12pm', '1pm', '2pm', '3pm', '4pm', '5pm']
    df_temp,order = get_df('University_of_California,_San_Diego__All_Parking_Spaces_Combined.csv')
    spaces_data =  df_temp.pivot('time','date','empty_spaces').reindex(s, columns = order)
    f, ax = plt.subplots(figsize=(40, 10))
    ax =sns.heatmap(spaces_data, cmap='YlGnBu',ax=ax,cbar_kws={'label': 'Empty Parking Spaces'})
    ax.figure.axes[-1].yaxis.label.set_size(40)
    label_y = ax.get_yticklabels()
    plt.setp(label_y, rotation=360, horizontalalignment='right',fontsize = 25)
    label_x = ax.get_xticklabels()
    plt.setp(label_x, rotation=45, horizontalalignment='right',fontsize = 25)
    plt.rcParams['font.size'] = 25
    plt.xlabel('Date', fontsize = 40)
    plt.ylabel('Time', fontsize = 40)
    plt.savefig("../images/empty_spaces_heatmap.jpg", bbox_inches = 'tight')
    plt.show()

if __name__ == '__main__':
    print('Collecting data and plot the empty spaces heatmap')
    get_figure()