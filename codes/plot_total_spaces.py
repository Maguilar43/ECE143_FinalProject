import matplotlib.pyplot as plt
import pandas as pd
import pylab as pl
import numpy as np
from numpy import *
Roosevelt_College = pd.read_csv("Roosevelt_College__All_Parking_Spaces_Combined.txt")
North_Campus = pd.read_csv("North_Campus__All_Parking_Spaces_Combined.txt")
School_of_Medicine = pd.read_csv("School_of_Medicine__All_Parking_Spaces_Combined.txt")
University_Center = pd.read_csv("University_Center__All_Parking_Spaces_Combined.txt")
East_Campus_Academic = pd.read_csv("East_Campus_Academic__All_Parking_Spaces_Combined.txt")
Health_Sciences = pd.read_csv("Health_Sciences__All_Parking_Spaces_Combined.txt")
data = [Roosevelt_College, North_Campus, School_of_Medicine, University_Center,
        East_Campus_Academic, Health_Sciences]
name = ["Roosevelt_College", "North_Campus", "School_of_Medicine", "University_Center",
        "East_Campus_Academic", "Health_Sciences"]
color = ["blue", "brown", "lime", "olive", "navy", "maroon",]

def totalSpacesByNeighbor():
    rate = []
    equation = []
    deriv = []
    line_list = ['--','--','-.','-','-','-']
    fig = plt.figure()
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


        plt.scatter(x, y, c=color[index], marker="o", s=20)
        plt.plot(x, y, linestyle=line_list[index], linewidth=3, markevery=1, color=color[index], label=name[index])
        plt.xlabel('years',fontsize=15)
        plt.ylabel('spaces',fontsize=15)
        plt.title("Total Spaces Number by Area", fontsize=30)
        pl.xticks(x, rotation=0, fontsize=15)

    plt.legend(bbox_to_anchor=(1.1,1.1), framealpha=1, fontsize=12)
    return fig


