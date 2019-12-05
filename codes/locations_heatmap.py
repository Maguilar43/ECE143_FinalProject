import gmaps
import gmaps.datasets
import pandas as pd
import os
import math


# Get the latitude and longtitude of the neighbors
# TODO: Use Google Maps API to get the locations' details of those neighbors

location_dict = {}
location_dict['Aquarium'] = (32.873649, -117.250205)
location_dict['Campus_Services_Complex'] = (32.884225, -117.229248)
location_dict['East_Campus_Academic'] = (32.883081, -117.223041)
location_dict['Health_Sciences'] = (32.879871, -117.222291)
location_dict['Marshall_College'] = (32.881570, -117.240855)
location_dict['Medical_Center_Hillcrest'] = (32.757564, -117.165722)
location_dict['Muir_College'] = (32.878590, -117.240475)
location_dict['North_Campus'] = (32.888639, -117.240570)
location_dict['North_Torrey_Pines_and_Glider_Port'] = (32.887263, -117.244244)
location_dict['Revelle_College'] = (32.875369, -117.241927)
location_dict['Roosevelt_College'] = (32.886399, -117.242311)
location_dict['School_of_Medicine'] = (32.874703, -117.236000)
location_dict['Science_Research_Park'] = (32.877269, -117.221253)
location_dict['SIO_Hillside'] = (32.868955, -117.247665)
location_dict['SIO_South'] = (32.866971, -117.250311)
location_dict['SIO_West'] = (32.869017, -117.253386)
location_dict['Sixth_College'] = (32.878434, -117.231914)
location_dict['Theatre_District'] = (32.872228, -117.240450)
location_dict['University_Center'] = (32.877892, -117.235919)
location_dict['Warren_College'] = (32.881349, -117.233666)


def get_aver(filename, year):
    '''

    Using this method to get the average occupancy of different quarters

    :param filename: str, the filename of the csv data
    :param year: str, the year of locations heatmap we want to plot
    :return: float, the average occupancy of different quarters
    '''

    assert isinstance(filename, str)

    df_ori = pd.read_csv(filename)
    s = ['8am','9am','10am','11am','12pm','1pm','2pm','3pm','4pm','5pm']
    df_temp = df_ori.drop(columns = s, axis = 1)
    df_temp['average_empty_spaces'] = df_ori[s].mean(axis=1)
    df_temp = df_temp.loc[(df_temp.year == year)]
    df_final = df_temp[['parking_spaces','average_empty_spaces']].mean()

    # As the occupancies is smaller than 1, if we want to make it as weights, we multiply it with 10
    return 10 * (float(df_final['parking_spaces']) - float(df_final['average_empty_spaces'])) / float(df_final['parking_spaces']) - 5

def get_weights(year):
    '''

    Use the get_aver function, we then get the real weights we want to use
    to get our Google Map based locations heatmap

    :param year: str, the year of locations heatmap we want to plot
    :return: list, the weights list we want to use in for the location heatmap
    '''

    assert isinstance(year, str)

    prefix = '../csv_data/By-Neighborhood/'
    files = os.listdir(prefix)
    # Use weights list to record all the weights we want to use for
    # the heatmap
    weights = []
    for loc in location_dict:
        total_aver = 0
        for file in files:
            if file == loc + '__All_Parking_Spaces_Combined.csv':
                total_aver += get_aver(prefix + file,year)
        weights.append(total_aver)
    return weights

def get_the_dataframe(year):
    '''

    This method is used to get the dataframe we want to use

    :param year: str, the year of locations heatmap we want to plot
    :return: DataFrame, the dataframe we are used for getting the Google Map locations heatmap
    '''

    assert isinstance(year, str)

    # Using latitude, longitude as the locations and average occupancy as the weights
    # to generate a dataframe
    lat_list = [location_dict[loc][0] for loc in location_dict]
    long_list = [location_dict[loc][1] for loc in location_dict]
    weights = get_weights(year)
    df = pd.DataFrame()
    df['latitude'] = lat_list
    df['longitude'] = long_list
    df['average'] = [x if not math.isnan(x) and x > 0 else 1 for x in weights]
    return df

def get_GoogleMap(df):
    '''

    Use the dataframe we get to plot the locations heatmap

    :param df: dataframe, the dataframe we are using to plot the heatmap
    :return: figure, the Google Map heatmap we get
    '''

    assert isinstance(df, pd.DataFrame)

    # Using gmaps package for getting Google Maps really location heatmap
    # This API_KEY may expire, please replace with your api key here
    gmaps.configure(api_key='AIzaSyBijrsbL29gQ7aBIbOt-6Xouz2EFJXIrbw')

    fig = gmaps.figure()
    heatmap_layer = gmaps.heatmap_layer(
        df[['latitude', 'longitude']], weights=df['average'],
        point_radius=25.0
    )

    fig.add_layer(heatmap_layer)
    return fig


if __name__ == '__main__':
    print('Using location data to generate a Google Map heatmap')
    print('Please use jupyter notebook to open this figure')
    get_GoogleMap(get_the_dataframe('2014/15'))
    get_GoogleMap(get_the_dataframe('2000/01'))