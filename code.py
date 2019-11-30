import matplotlib.pyplot as plt
import pandas as pd
import pylab as pl
import numpy as np
from numpy import *
from pyecharts.charts import Geo, Map
from pyecharts import options as opts
import pyecharts
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import style
import seaborn as sns

SIO_South = pd.read_csv("SIO_South__All_Parking_Spaces_Combined.txt")
SIO_West = pd.read_csv("SIO_West__All_Parking_Spaces_Combined.txt")
SIO_Hillside = pd.read_csv("SIO_Hillside__All_Parking_Spaces_Combined.txt")
Aquarium = pd.read_csv("Aquarium__All_Parking_Spaces_Combined.txt")
Theatre_District = pd.read_csv("Theatre_District__All_Parking_Spaces_Combined.txt")
Revelle_College = pd.read_csv("Revelle_College__All_Parking_Spaces_Combined.txt")
Muir_College = pd.read_csv("Muir_College__All_Parking_Spaces_Combined.txt")
Marshall_College = pd.read_csv("Marshall_College__All_Parking_Spaces_Combined.txt")
Roosevelt_College = pd.read_csv("Roosevelt_College__All_Parking_Spaces_Combined.txt")
North_Campus = pd.read_csv("North_Campus__All_Parking_Spaces_Combined.txt")
Warren_College = pd.read_csv("Warren_College__All_Parking_Spaces_Combined.txt")
Campus_Services_Complex = pd.read_csv("Campus_Services_Complex__All_Parking_Spaces_Combined.txt")
School_of_Medicine = pd.read_csv("School_of_Medicine__All_Parking_Spaces_Combined.txt")
University_Center = pd.read_csv("University_Center__All_Parking_Spaces_Combined.txt")
East_Campus_Academic = pd.read_csv("East_Campus_Academic__All_Parking_Spaces_Combined.txt")
Health_Sciences = pd.read_csv("Health_Sciences__All_Parking_Spaces_Combined.txt")
Medical_Center_Hillcrest = pd.read_csv("Medical_Center_Hillcrest__All_Parking_Spaces_Combined.txt")

# Science_Research_Park = pd.read_csv("Science_Research_Park__All_Parking_Spaces_Combined.txt")
# Sixth_College = pd.read_csv("Sixth_College__All_Parking_Spaces_Combined.txt")
# North_Torrey_Pines_and_Glider_Port = pd.read_csv("North_Torrey_Pines_and_Glider_Port__All_Parking_Spaces_Combined.txt")

data = [SIO_South, SIO_West, SIO_Hillside, Aquarium, Theatre_District, Revelle_College, Muir_College, Marshall_College,
        Roosevelt_College, North_Campus, Warren_College, Campus_Services_Complex, School_of_Medicine, University_Center,
        East_Campus_Academic, Health_Sciences, Medical_Center_Hillcrest]
name = ["SIO_South", "SIO_West", "SIO_Hillside", "Aquarium", "Theatre_District", "Revelle_College", "Muir_College", "Marshall_College",
        "Roosevelt_College", "North_Campus", "Warren_College", "Campus_Services_Complex", "School_of_Medicine", "University_Center",
        "East_Campus_Academic", "Health_Sciences", "Medical_Center_Hillcrest"]
color = ["blue", "brown", "lime", "olive", "navy", "maroon", "olive", "magenta", "pink", "peru", "tan", "sienna", "steelblue",
         "silver", "saddlebrown", "yellow", "purple"]



'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'               Plot 1:  Spaces number statistic by "year" and "neighborhood" in 3D face                  '      
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

years = ["2000", "20001", "2002", "2003", "2004", "2005", "2006", "2007",
     "2008", "2009", "2010", "2011", "2012", "2013", "2014"]
x = np.array(range(len(name)))
y = np.array(range(len(["2000", "20001", "2002", "2003", "2004", "2005", "2006", "2007",
     "2008", "2009", "2010", "2011", "2012", "2013", "2014"])))

z = np.ones((15,17))
for i in range(17):
    for j in range(15):
        z[j, i] = data[i]["parking_spaces"].values[j*4]
X, Y = meshgrid(x, y)

fig1 = plt.figure(1)
ax = Axes3D(fig1)
ax.plot_surface(X,Y,z,rstride=1, cstride=1, cmap="rainbow")
pl.xticks([index for index in x],name, rotation=315, fontsize=5)
pl.yticks([index for index in x],years, rotation=315, fontsize=5)
ax.set_xlabel('years')
ax.set_ylabel('neighbor')
ax.set_zlabel('spaces')
plt.title("Spaces Number 3D")

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'           Plot 2:    Spaces number statistic by "year" and "neighborhood" in 2D line Spots            '
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
rate = []
equation = []
deriv = []

fig2 = plt.figure(2)
plt.style.use('Solarize_Light2')
for index, e in enumerate(data):

    spaces_list = e["parking_spaces"].values
    tmp = []
    for i in range(len(spaces_list)//4):
        tmp.append(spaces_list[i*4])

    x = list(range(2000, 2015))
    y = tmp

    f1 = np.polyfit(x, y, 3)
    p1 = np.poly1d(f1)
    d_p1 = p1.deriv()
    equation.append(p1)
    deriv.append(d_p1)
    rate.append(d_p1(2014))

    yvals = p1(x)

    plt.scatter(x, y, c='r', marker="*", s=20)
    plt.plot(x, y, linestyle='-', linewidth=1, markevery=1, color=color[index], label=name[index])
    plt.xlabel('years')
    plt.ylabel('spaces')
    plt.title("Space Number Plot")
    pl.xticks(x, rotation=315, fontsize=5)

plt.legend()

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'         Plot 3:     Spaces number statistic by "year" and "neighborhood"  in 2D Regression Curve        '
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
rate = []
equation = []
deriv = []

fig3 = plt.figure(3)
plt.style.use('seaborn-darkgrid')
for index, e in enumerate(data):

    spaces_list = e["parking_spaces"].values
    tmp = []
    for i in range(len(spaces_list)//4):
        tmp.append(spaces_list[i*4])

    x = list(range(2000, 2015))
    y = tmp

    f1 = np.polyfit(x, y, 3)
    p1 = np.poly1d(f1)
    d_p1 = p1.deriv()
    equation.append(p1)
    deriv.append(d_p1)
    rate.append(d_p1(2014))

    yvals = p1(x)

    plt.plot(x, yvals, linestyle='-', linewidth=1, markevery=1,color=color[index], label=name[index])
    plt.xlabel('years')
    plt.ylabel('spaces')
    plt.title("Regression Plot")
    pl.xticks(x, rotation=315, fontsize=5)

plt.legend()

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'          Plot 4:   Rate of Spaces number statistic by "year" and "neighborhood"  in 2D HeatMap          '     
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

pos_val = []
neg_val = []
pos_name = []
neg_name = []
for i,e in enumerate(rate):
    if e > 0:
        pos_val.append(e)
        pos_name.append(name[i])
    else:
        neg_val.append(e)
        neg_name.append(name[i])

fig4, (ax1,ax2) = plt.subplots(ncols=2)
fig4.subplots_adjust(wspace=0.01)
sns.heatmap([pos_val], cmap="rocket_r", ax=ax1, cbar=False, fmt=".3g", annot=True, annot_kws={'size':9, 'color':'lightgreen'})
fig4.colorbar(ax1.collections[0], ax=ax1,location="left", use_gridspec=False, pad=0.2)
ax1.set_title('Increasing')
ax1.set_xlabel("")
ax1.set_ylabel("")
ax1.set_xticklabels(pos_name,rotation=315, fontsize=5)
ax1.set_yticklabels("")

sns.heatmap([neg_val], cmap="YlGnBu_r", ax=ax2, cbar=False, fmt=".3g", annot=True, annot_kws={'size':9, 'color':'lightgreen'})
fig4.colorbar(ax2.collections[0], ax=ax2,location="right", use_gridspec=False, pad=0.2)
ax2.yaxis.tick_right()
ax2.tick_params(rotation=1)

ax2.set_title('Decreasing')
ax2.set_xlabel("")
ax2.set_ylabel("")
ax2.set_xticklabels(neg_name,rotation=315, fontsize=5)
ax2.set_yticklabels("")

plt.show()


