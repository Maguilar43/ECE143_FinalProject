# ECE 143 Final Project --- UCSD Parking

### Members: 
- Matthew Aguilar
- Hao Zhu
- Jiajun Du
- Kasidech Tantipanichaphan

## File Structure: 
- codes/ - all .py files and the Jupyter Notebook
- pdf_data/ - the data we were able to get from UCSD
- excel_data/ - converted data from PDF -> EXCEL using an Adobe converter
- excel_data/2019_data/ - 2019 data seperated by spot type, by quarter, by week
- csv_data/ - correctly formatted data that was converted from excel files using data_extraction script
- images/ - various pictures created throughout code building

## How to Run the Code: 
#### xcel_to_df.py
- < python xcel_to_df.py > 

Running this file turns the specified file in main() into a dataframe and then prints the resulting dataframe

#### historical_peaks.py
- < python historical_peaks.py >

Running this file generates both a pie chart showing the spot distributions through specified years as well as a line chart that shows how different spots utilize their parking through the years for a specified quarter. These are seen in the main() function.

#### find_parking.py
- < python find_parking.py >

Running this file returns the best lot to park in for a specified Spot type and Day of week defined in main()

#### data_extraction.py
- < python data_extraction.py >

Running this file will use all excel files to find useful data and then convert those data into CSV files in the csv_data folder. Meanwhile, it will fix minor mistakes of the conversion as well because the excel files may have some error. It will print a message on the console to let the user know the current program's status.

#### locations_heatmap.py
- < python locations_heatmap.py >

Running this file will generate a location's heatmap which is based on the latitude and longitude of the parking spaces. The heatmap is a Google Map kind figure and should be demonstrated in the Jupyter Notebook. What's more, the main function will also print information messages for users. 

Remember to replace the API_KEY to your Google Maps' api key for this api key that may expire.

#### emptyspaces_heatmap.py
- < python emptyspaces_heatmap.py >

Running this file will show a heatmap of total empty spaces in the University and also an information message will print in the console.

## Third-Party Modules
- Pandas
- Matplotlib
- Seaborn
- Numpy
- Statsmodel
- Scipy
- Xlrd
- Jupyter-gmaps.

