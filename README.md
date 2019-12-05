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
- csv_data/ - correctly formatted data that was converted form Adobe to excel
- images/ - various pictures created throughout code building

## How to Run the Code: 
#### xcel_to_df.py
- < python xcel_to_df.py > 

Running this file turns the specified file in main() into a dataframe and then prints the resulting dataframe

#### 
- < python historical_peaks.py >

Running this file generates both a pie chart showing the spot distributions through specified years as well as a line chart that shows how different spots utilize their parking through the years for a specified quarter. These are seen in the main() function.

#### find_parking.py
- < python find_parking.py >

Running this file returns the best lot to park in for a specified Spot type and Day of week defined in main()




## Third-Party Modules
- Pandas
- Matplotlib
- Seaborn
- Numpy
- Statsmodel
- Scipy
- Xlrd
- Jupyter-gmaps.

