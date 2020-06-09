import csv
from collections import defaultdict
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

cities = defaultdict(list)
cities["India"] = defaultdict(list)
cities["United Kingdom"] = defaultdict(list)
cities["United States"] = defaultdict(list)

files = ["waqi-covid19-airqualitydata-2019Q1.csv","waqi-covid19-airqualitydata-2019Q2.csv",
        "waqi-covid19-airqualitydata-2019Q3.csv","waqi-covid19-airqualitydata-2019Q4.csv",
        "waqi-covid19-airqualitydata-2020.csv"]

files = files + ["waqi-covid19-airqualitydata-2015H1.csv","waqi-covid19-airqualitydata-2016H1.csv","waqi-covid19-airqualitydata-2017H1.csv", "waqi-covid19-airqualitydata-2018H1.csv"]

extradata = ["delhimanual.csv","londonmanual.csv","newyorkmanual.csv"]

required = ["no2","pm25"]
#datemin = datetime.datetime(2019, 3, 1)
datemin = datetime.datetime(2015, 3, 1)

#Extract all data from the big database
for file in files:
    stream = open(file, 'r', encoding='utf-8')

    print("\n\n--------------------------------------------------------------------------------------------------------------------\n\n".replace('-','_'),"Now analysing: ", file,"\n--------------------------------------------------------------------------------------------------------------------".replace('-','='))

    with stream:
        csvreader = csv.reader(stream, delimiter=",")
        for row in csvreader:
            if len(row) == 1:
                continue

            if row[1] == 'IN':
                if row[3] in required:
                    if row[2] not in cities["India"]:
                        cities["India"][row[2]] = defaultdict(list)
                    cities["India"][row[2]][row[3]].append(row[0:1] + row[4:])
            if row[1] == 'GB':
                if row[3] in required:
                    if row[2] not in cities["United Kingdom"]:
                        cities["United Kingdom"][row[2]] = defaultdict(list)
                    cities["United Kingdom"][row[2]][row[3]].append(row[0:1] + row[4:])
            if row[1] == 'US':
                if row[3] in required:
                    if row[2] not in cities["United States"]:
                        cities["United States"][row[2]] = defaultdict(list)
                    cities["United States"][row[2]][row[3]].append(row[0:1] + row[4:])


#Removing missing measurement group data
for item in list(cities):
    for city in list(cities[item]):
        if (set(required) != set(cities[item][city].keys())):
            del cities[item][city]

#Removing data that started measuring too late                  #TODO problem, deletes all before 2019
for item in list(cities):
    for city in list(cities[item]):
        for measure in cities[item][city]:
            if cities[item][city] == []: #error vaag
                del cities[item][city]
                break
            earliestdate = datetime.datetime(2020,1,1)
            for i in range(0,len(cities[item][city][measure])):
                d = cities[item][city][measure][i][0].split('-')
                currdate = datetime.datetime(int(d[0]),int(d[1]),int(d[2]))
                if currdate < earliestdate:
                    earliestdate = currdate
            if earliestdate > datemin:
                print("removed : ",city,earliestdate)
                del cities[item][city]


#Removing data before datemin
for item in list(cities):
    for city in list(cities[item]):
        for measure in cities[item][city]:
            entries = []
            for entry in cities[item][city][measure]:
                d = entry[0].split('-')
                date = datetime.datetime(int(d[0]),int(d[1]),int(d[2]))
                if not date < datemin:
                    #print(entry)
                    entries.append(entry)
            cities[item][city][measure] = entries

#sanitizing
for item in list(cities):
    for city in list(cities[item]):
        for var in cities[item][city]:
            if not cities[item][city][var]:
                del cities[item][city]
                break


# add manual data
for file in extradata:
    stream = open(file, 'r', encoding='utf-8')
    lines = stream.readlines()
    lines = [line.rstrip() for line in lines]

    print("\n\n--------------------------------------------------------------------------------------------------------------------\n\n".replace('-','_'),"Now analysing: ", file,"\n--------------------------------------------------------------------------------------------------------------------".replace('-','='))

    cities[lines[0]][lines[1]] = defaultdict(list)
    cities[lines[0]][lines[1]]["pm25"] = defaultdict(list)
    entries = []
    for i in range(2,len(lines)):
        entries.append([lines[i].split(',')[0].replace('/','-')] + [lines[i].split(',')[1]] + ["x"])
    cities[lines[0]][lines[1]]["pm25"] = entries

#summarize
for item in cities:
    citylist = []
    print("Available data for cities in : ",item)
    for city in cities[item]:
        citylist.append(city)
        for entry in cities[item][city]:
            print(city, " has ", entry, " first data from : ", cities[item][city][entry][0][0], " to ", cities[item][city][entry][-1][0])
    #print(item, " (", len(citylist), ") : \n", citylist,"\n--------------------------------------------------------------------------------------------------------------------")
    #input()

#Function to plot
def plotCity(country, city, varofinterest, colorr = 'black', llinestyle = 'solid', rolling = True):
    y_axis = [float(cities[country][city][varofinterest][i][-2]) for i in range(len(cities[country][city][varofinterest]))]
    dates = [cities[country][city][varofinterest][i][0] for i in range(len(cities[country][city][varofinterest]))]
    dates = [datetime.datetime.strptime(d,"%Y-%m-%d").date() for d in dates]
    data = sorted(zip(dates,y_axis))
    y_axis_sorted = [x for y, x in data]
    dates_sorted = [y for y, x in data]

    df = pd.DataFrame({'dates': dates_sorted, 'rolling':y_axis_sorted})
    df['pandas_SMA_3'] = df.iloc[:,1].rolling(window=3).mean()
    if rolling:
        plt.plot(dates_sorted, df['pandas_SMA_3'],linestyle=llinestyle, linewidth=0.7, color = colorr)
    else:
        plt.plot(dates_sorted, y_axis_sorted,linestyle=llinestyle, linewidth=0.7, color = colorr)
    plt.title(f"{city} : {varofinterest}")


#Plot NO2
plt.figure(figsize=(20,10))
species = "no2"
plotCity("United States","Staten Island",species,"red","dotted")
plotCity("India","Delhi",species,"green","solid")
plotCity("United Kingdom","London",species,"blue","--")
plt.legend(["New York","Delhi","London"])
plt.title(f"{species} 3 days moving average")

#Plot PM2.5
plt.figure(figsize=(20,10))
species = "pm25"
plotCity("United States","Staten Island(new)",species,"red","dotted")
plotCity("United States","Staten Island",species,"red","solid")
plotCity("India","Delhi(new)",species,"green","dotted")
plotCity("India","Delhi",species,"green","solid")
plotCity("United Kingdom","London(new)",species,"blue","dotted")
plotCity("United Kingdom","London",species,"blue","solid")
plt.legend(["New York (added data)","New York","Delhi (added data)","Delhi","London (added data)","London"])
plt.title(f"{species} 3 days moving average")

''' plot temperature (was for testing purposes)
plt.figure(figsize=(20,10))
species = "temperature"
plotCity("United States","Manhattan",species,"red","dotted",rolling = False)
plotCity("India","Kolkata",species,"green","solid",rolling = False)
plotCity("United Kingdom","London",species,"blue","--",rolling = False)
plt.legend(["New York","Kolkata","London"])
plt.title(f"{species} raw")
'''

plt.show()
