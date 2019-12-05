import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import patsy
import statsmodels.api as sm
import scipy.stats as stats
from scipy.stats import ttest_ind, chisquare, normaltest

# Load csv file.

df_La_Jolla_S = pd.read_csv("/home/ktantipa/ECE143_FinalProject/csv_data/By-Location/La_Jolla_Campus__S_Parking_Spaces.csv")
df_La_Jolla_A = pd.read_csv("/home/ktantipa/ECE143_FinalProject/csv_data/By-Location/La_Jolla_Campus__A_Parking_Spaces.csv")
df_La_Jolla_B = pd.read_csv("/home/ktantipa/ECE143_FinalProject/csv_data/By-Location/La_Jolla_Campus__B_Parking_Spaces.csv") 
df_La_Jolla_V = pd.read_csv("/home/ktantipa/ECE143_FinalProject/csv_data/By-Location/La_Jolla_Campus__Visitor_Parking_Spaces.csv") 

# Assertion
# Check if the files is dataframe.


assert isinstance(df_La_Jolla_S, pd.DataFrame)
assert isinstance(df_La_Jolla_A, pd.DataFrame)
assert isinstance(df_La_Jolla_B, pd.DataFrame)
assert isinstance(df_La_Jolla_V, pd.DataFrame)

# Change column as Empty Spots relative to time.


df_La_Jolla_S_new = df_La_Jolla_S.melt(id_vars=["year", "quarter", "parking_spaces", "peak_empty_spaces", "peak_occupied_spaces", "%_occupied"], 
        var_name="Time of the day", 
        value_name="Empty Spots")

df_La_Jolla_A_new = df_La_Jolla_A.melt(id_vars=["year", "quarter", "parking_spaces", "peak_empty_spaces", "peak_occupied_spaces", "%_occupied"], 
        var_name="Time of the day", 
        value_name="Empty Spots")

df_La_Jolla_B_new = df_La_Jolla_B.melt(id_vars=["year", "quarter", "parking_spaces", "peak_empty_spaces", "peak_occupied_spaces", "%_occupied"], 
        var_name="Time of the day", 
        value_name="Empty Spots")


df_La_Jolla_V_new = df_La_Jolla_V.melt(id_vars=["year", "quarter", "parking_spaces", "peak_empty_spaces", "peak_occupied_spaces", "%_occupied"], 
        var_name="Time of the day", 
        value_name="Empty Spots")

# The average empty spots (year 2000)




df_La_Jolla_S_new_2000 = df_La_Jolla_S_new[df_La_Jolla_S_new.year == '2000/01']
df_La_Jolla_S_new_2000["Empty Spots"].mean()


# The average empty spots (year 2005)



df_La_Jolla_S_new_2005 = df_La_Jolla_S_new[df_La_Jolla_S_new.year == '2005/06']
df_La_Jolla_S_new_2005["Empty Spots"].mean()


# The average empty spots (year 2010)


df_La_Jolla_S_new_2010 = df_La_Jolla_S_new[df_La_Jolla_S_new.year == '2010/11']
df_La_Jolla_S_new_2010["Empty Spots"].mean()


# The average empty spots (year 2014)


df_La_Jolla_S_new_2014 = df_La_Jolla_S_new[df_La_Jolla_S_new.year == '2014/15']
df_La_Jolla_S_new_2014["Empty Spots"].mean()


# Average Empty Spots based on time of the day (8am to 5pm)(S-spot)


df_La_Jolla_S_new = df_La_Jolla_S_new.rename(columns={"Time of the day": "Time"})

df_La_Jolla_S_new_8am = df_La_Jolla_S_new[df_La_Jolla_S_new.Time == '8am']
x1 = df_La_Jolla_S_new_8am["Empty Spots"].mean()
df_La_Jolla_S_new_9am = df_La_Jolla_S_new[df_La_Jolla_S_new.Time == '9am']
x2 = df_La_Jolla_S_new_9am["Empty Spots"].mean()
df_La_Jolla_S_new_10am = df_La_Jolla_S_new[df_La_Jolla_S_new.Time == '10am']
x3 = df_La_Jolla_S_new_10am["Empty Spots"].mean()
df_La_Jolla_S_new_11am = df_La_Jolla_S_new[df_La_Jolla_S_new.Time == '11am']
x4 = df_La_Jolla_S_new_11am["Empty Spots"].mean()
df_La_Jolla_S_new_12am = df_La_Jolla_S_new[df_La_Jolla_S_new.Time == '12pm']
x5 = df_La_Jolla_S_new_12am["Empty Spots"].mean()
df_La_Jolla_S_new_1pm = df_La_Jolla_S_new[df_La_Jolla_S_new.Time == '1pm']
x6 = df_La_Jolla_S_new_1pm["Empty Spots"].mean()
df_La_Jolla_S_new_2pm = df_La_Jolla_S_new[df_La_Jolla_S_new.Time == '2pm']
x7 = df_La_Jolla_S_new_2pm["Empty Spots"].mean()
df_La_Jolla_S_new_3pm = df_La_Jolla_S_new[df_La_Jolla_S_new.Time == '3pm']
x8 = df_La_Jolla_S_new_3pm["Empty Spots"].mean()
df_La_Jolla_S_new_4pm = df_La_Jolla_S_new[df_La_Jolla_S_new.Time == '4pm']
x9 = df_La_Jolla_S_new_4pm["Empty Spots"].mean()
df_La_Jolla_S_new_5pm = df_La_Jolla_S_new[df_La_Jolla_S_new.Time == '5pm']
x10 = df_La_Jolla_S_new_5pm["Empty Spots"].mean()

#Times = ('8am', '9am', '10am', '11am', '12pm', '1pm', '2pm', '3pm', '4pm', '5pm')
#y_pos = np.arange(len(Times))
#performance = [x1,x2,x3,x4,x5,x6,x7,x8,x9,x10]

#plt.bar(y_pos, performance, align='center', alpha=0.5)
#plt.xticks(y_pos, Times)
#plt.ylabel('Empty Spots')
#plt.title('Empty Spots of the Day on Average S Permit')

#plt.show()


# Detail for the Max and Min Empty Spots (S parking permit)


df_La_Jolla_S_new.loc[df_La_Jolla_S_new['Empty Spots'].idxmax()]
df_La_Jolla_S_new.loc[df_La_Jolla_S_new['Empty Spots'].idxmin()]



# ### Detail for the Max and Min Empty Spots (A parking permit)


df_La_Jolla_A_new.loc[df_La_Jolla_A_new['Empty Spots'].idxmax()]



df_La_Jolla_A_new.loc[df_La_Jolla_A_new['Empty Spots'].idxmin()]


# The average empty spots (year 2000)


df_La_Jolla_A_2000 = df_La_Jolla_A_new[df_La_Jolla_A_new.year == '2000/01']
#df_La_Jolla_A_2000
df_La_Jolla_A_2000["Empty Spots"].mean()


# The average empty spots (year 2009)

df_La_Jolla_A_2009 = df_La_Jolla_A_new[df_La_Jolla_A_new.year == '2009/10']
df_La_Jolla_A_2009["Empty Spots"].mean()


# The average empty spots (year 2014)

df_La_Jolla_A_2015 = df_La_Jolla_A_new[df_La_Jolla_A_new.year == '2014/15']
df_La_Jolla_A_2015["Empty Spots"].mean()


# ### Average Empty Spots based on time of the day (A-spot)


df_La_Jolla_A_new = df_La_Jolla_A.melt(id_vars=["year", "quarter", "parking_spaces", "peak_empty_spaces", "peak_occupied_spaces", "%_occupied"], 
        var_name="Time of the day", 
        value_name="Empty Spots")

df_La_Jolla_A_new = df_La_Jolla_A_new.rename(columns={"Time of the day": "Time"})


df_La_Jolla_A_new_8am = df_La_Jolla_A_new[df_La_Jolla_A_new.Time == '8am']
y1 = df_La_Jolla_S_new_8am["Empty Spots"].mean()
df_La_Jolla_A_new_9am = df_La_Jolla_A_new[df_La_Jolla_A_new.Time == '9am']
y2 = df_La_Jolla_A_new_9am["Empty Spots"].mean()
df_La_Jolla_A_new_10am = df_La_Jolla_A_new[df_La_Jolla_A_new.Time == '10am']
y3 = df_La_Jolla_A_new_10am["Empty Spots"].mean()
df_La_Jolla_A_new_11am = df_La_Jolla_A_new[df_La_Jolla_A_new.Time == '11am']
y4 = df_La_Jolla_A_new_11am["Empty Spots"].mean()
df_La_Jolla_A_new_12am = df_La_Jolla_A_new[df_La_Jolla_A_new.Time == '12pm']
y5 = df_La_Jolla_A_new_12am["Empty Spots"].mean()
df_La_Jolla_A_new_1pm = df_La_Jolla_A_new[df_La_Jolla_A_new.Time == '1pm']
y6 = df_La_Jolla_A_new_1pm["Empty Spots"].mean()
df_La_Jolla_A_new_2pm = df_La_Jolla_A_new[df_La_Jolla_A_new.Time == '2pm']
y7 = df_La_Jolla_A_new_2pm["Empty Spots"].mean()
df_La_Jolla_A_new_3pm = df_La_Jolla_A_new[df_La_Jolla_A_new.Time == '3pm']
y8 = df_La_Jolla_A_new_3pm["Empty Spots"].mean()
df_La_Jolla_A_new_4pm = df_La_Jolla_A_new[df_La_Jolla_A_new.Time == '4pm']
y9 = df_La_Jolla_A_new_4pm["Empty Spots"].mean()
df_La_Jolla_A_new_5pm = df_La_Jolla_A_new[df_La_Jolla_A_new.Time == '5pm']
y10 = df_La_Jolla_A_new_5pm["Empty Spots"].mean()

#Times = ('8am', '9am', '10am', '11am', '12pm', '1pm', '2pm', '3pm', '4pm', '5pm')
#y_pos = np.arange(len(Times))
#performance = [y1,y2,y3,y4,y5,y6,y7,y8,y9,y10]

#plt.bar(y_pos, performance, align='center', alpha=0.5)
#plt.xticks(y_pos, Times)
#plt.ylabel('Empty Spots')
#plt.title('Empty Spots of the Day on Average (A permit)')

#plt.show()

# Detail for the Max and Min Empty Spots (B parking permit)



df_La_Jolla_B_new.loc[df_La_Jolla_B_new['Empty Spots'].idxmax()]
df_La_Jolla_B_new.loc[df_La_Jolla_B_new['Empty Spots'].idxmin()]


# The average empty spots (year 2000)


df_La_Jolla_B_2000 = df_La_Jolla_B_new[df_La_Jolla_B_new.year == '2000/01']
df_La_Jolla_B_2000["Empty Spots"].mean()


# The average empty spots (year 2009)

df_La_Jolla_B_2009 = df_La_Jolla_B_new[df_La_Jolla_B_new.year == '2009/10']
df_La_Jolla_B_2009["Empty Spots"].mean()


# The average empty spots (year 2014)

df_La_Jolla_B_2014 = df_La_Jolla_B_new[df_La_Jolla_B_new.year == '2014/15']
df_La_Jolla_B_2014["Empty Spots"].mean()


# ### Average Empty Spots based on time of the day (B-spot)

df_La_Jolla_B_new = df_La_Jolla_B_new.rename(columns={"Time of the day": "Time"})

df_La_Jolla_B_new_8am = df_La_Jolla_B_new[df_La_Jolla_B_new.Time == '8am']
z1 = df_La_Jolla_B_new_8am["Empty Spots"].mean()
df_La_Jolla_B_new_9am = df_La_Jolla_B_new[df_La_Jolla_B_new.Time == '9am']
z2 = df_La_Jolla_B_new_9am["Empty Spots"].mean()
df_La_Jolla_B_new_10am = df_La_Jolla_B_new[df_La_Jolla_B_new.Time == '10am']
z3 = df_La_Jolla_B_new_10am["Empty Spots"].mean()
df_La_Jolla_B_new_11am = df_La_Jolla_B_new[df_La_Jolla_B_new.Time == '11am']
z4 = df_La_Jolla_B_new_11am["Empty Spots"].mean()
df_La_Jolla_B_new_12am = df_La_Jolla_B_new[df_La_Jolla_B_new.Time == '12pm']
z5 = df_La_Jolla_B_new_12am["Empty Spots"].mean()
df_La_Jolla_B_new_1pm = df_La_Jolla_B_new[df_La_Jolla_B_new.Time == '1pm']
z6 = df_La_Jolla_B_new_1pm["Empty Spots"].mean()
df_La_Jolla_B_new_2pm = df_La_Jolla_B_new[df_La_Jolla_B_new.Time == '2pm']
z7 = df_La_Jolla_B_new_2pm["Empty Spots"].mean()
df_La_Jolla_B_new_3pm = df_La_Jolla_B_new[df_La_Jolla_B_new.Time == '3pm']
z8 = df_La_Jolla_B_new_3pm["Empty Spots"].mean()
df_La_Jolla_B_new_4pm = df_La_Jolla_B_new[df_La_Jolla_B_new.Time == '4pm']
z9 = df_La_Jolla_B_new_4pm["Empty Spots"].mean()
df_La_Jolla_B_new_5pm = df_La_Jolla_B_new[df_La_Jolla_B_new.Time == '5pm']
z10 = df_La_Jolla_B_new_5pm["Empty Spots"].mean()

#Times = ('8am', '9am', '10am', '11am', '12pm', '1pm', '2pm', '3pm', '4pm', '5pm')
#y_pos = np.arange(len(Times))
#performance = [z1,z2,z3,z4,z5,z6,z7,z8,z9,z10]

#plt.bar(y_pos, performance, align='center', alpha=0.5)
#plt.xticks(y_pos, Times)
#plt.ylabel('Empty Spots')
#plt.title('Empty Spots of the Day on Average (B permit)')

#plt.show()



df_La_Jolla_V_new = df_La_Jolla_V.melt(id_vars=["year", "quarter", "parking_spaces", "peak_empty_spaces", "peak_occupied_spaces", "%_occupied"], 
        var_name="Time of the day", 
        value_name="Empty Spots")


# ### Detail for the Max and Min Empty Spots (V parking)



df_La_Jolla_V_new.loc[df_La_Jolla_V_new['Empty Spots'].idxmax()]


df_La_Jolla_V_new.loc[df_La_Jolla_V_new['Empty Spots'].idxmin()]


# Average empty spots in year 2000


df_La_Jolla_V_2000 = df_La_Jolla_V_new[df_La_Jolla_V_new.year == '2000/01']
df_La_Jolla_V_2000["Empty Spots"].mean()


# Average empty spots in year 2009


df_La_Jolla_V_2000 = df_La_Jolla_V_new[df_La_Jolla_V_new.year == '2009/10']
df_La_Jolla_V_2000["Empty Spots"].mean()


# Average empty spots in year 2014


df_La_Jolla_V_2000 = df_La_Jolla_V_new[df_La_Jolla_V_new.year == '2014/15']
df_La_Jolla_V_2000["Empty Spots"].mean()


df_La_Jolla_V_new = df_La_Jolla_V_new.rename(columns={"Time of the day": "Time"})

df_La_Jolla_V_new_8am = df_La_Jolla_V_new[df_La_Jolla_V_new.Time == '8am']
a1 = df_La_Jolla_V_new_8am["Empty Spots"].mean()
df_La_Jolla_V_new_9am = df_La_Jolla_V_new[df_La_Jolla_V_new.Time == '9am']
a2 = df_La_Jolla_V_new_9am["Empty Spots"].mean()
df_La_Jolla_V_new_10am = df_La_Jolla_V_new[df_La_Jolla_V_new.Time == '10am']
a3 = df_La_Jolla_V_new_10am["Empty Spots"].mean()
df_La_Jolla_V_new_11am = df_La_Jolla_V_new[df_La_Jolla_V_new.Time == '11am']
a4 = df_La_Jolla_V_new_11am["Empty Spots"].mean()
df_La_Jolla_V_new_12am = df_La_Jolla_V_new[df_La_Jolla_V_new.Time == '12pm']
a5 = df_La_Jolla_V_new_12am["Empty Spots"].mean()
df_La_Jolla_V_new_1pm = df_La_Jolla_V_new[df_La_Jolla_V_new.Time == '1pm']
a6 = df_La_Jolla_V_new_1pm["Empty Spots"].mean()
df_La_Jolla_V_new_2pm = df_La_Jolla_V_new[df_La_Jolla_V_new.Time == '2pm']
a7 = df_La_Jolla_V_new_2pm["Empty Spots"].mean()
df_La_Jolla_V_new_3pm = df_La_Jolla_V_new[df_La_Jolla_V_new.Time == '3pm']
a8 = df_La_Jolla_V_new_3pm["Empty Spots"].mean()
df_La_Jolla_V_new_4pm = df_La_Jolla_V_new[df_La_Jolla_V_new.Time == '4pm']
a9 = df_La_Jolla_V_new_4pm["Empty Spots"].mean()
df_La_Jolla_V_new_5pm = df_La_Jolla_V_new[df_La_Jolla_V_new.Time == '5pm']
a10 = df_La_Jolla_V_new_5pm["Empty Spots"].mean()

#Times = ('8am', '9am', '10am', '11am', '12pm', '1pm', '2pm', '3pm', '4pm', '5pm')
#y_pos = np.arange(len(Times))
#performance = [a1,a2,a3,a4,a5,a6,a7,a8,a9,a10]

#plt.bar(y_pos, performance, align='center', alpha=0.5)
#plt.xticks(y_pos, Times)
#plt.ylabel('Empty Spots')
#plt.title('Empty Spots of the Day on Average (V permit)')


# Combine Charts

S_spot = [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10]
A_spot = [y1, y2, y3, y4, y5, y6, y7, x8, x9, x10]
B_spot = [z1, z2, z3, z4, z5, z6, z7, z8, z9, z10]
V_spot = [a1, a2, a3, a4, a5, a6, a7, a8, a9, a10]

index = ['8am','9am','10am','11am','12pm','1pm','2pm','3pm','4pm', '5pm']
df = pd.DataFrame({'S spot': S_spot,
                   'A spot': A_spot,
                   'B spot': B_spot,
                   'V spot': V_spot}, index=index)
ax = df.plot.bar(title='What are the average empty Spots on Average for each permits? (La Jolla Campus)', rot=0)


