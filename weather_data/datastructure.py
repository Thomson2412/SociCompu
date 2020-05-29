import csv
from collections import defaultdict
import datetime
import matplotlib.pyplot as plt

cities = defaultdict(list)
cities["India"] = defaultdict(list)
cities["United Kingdom"] = defaultdict(list)
cities["United States"] = defaultdict(list)

files = ["waqi-covid19-airqualitydata-2019Q1.csv","waqi-covid19-airqualitydata-2019Q2.csv",
        "waqi-covid19-airqualitydata-2019Q3.csv","waqi-covid19-airqualitydata-2019Q4.csv",
        "waqi-covid19-airqualitydata-2020.csv"]

required = ["no2","pm25","temperature"]
datemin = datetime.datetime(2019, 3, 1)

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


#removing missing data
for item in list(cities):
    for city in list(cities[item]):
        if (set(required) != set(cities[item][city].keys())):
            del cities[item][city]

#removing not enough dates
for item in list(cities):
    for city in list(cities[item]):
        for measure in cities[item][city]:
            if cities[item][city] == []: #error vaag
                del cities[item][city]
                break
            #print(cities[item][city][measure][0][0])
            d = cities[item][city][measure][0][0].split('-')
            date = datetime.datetime(int(d[0]),int(d[1]),int(d[2]))
            if date > datemin:
                del cities[item][city]
            #input()


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
            if cities[item][city][var] == []:
                del cities[item][city]


for item in cities:
    citylist = []
    print("Available data for cities in : ",item)
    for city in cities[item]:
        citylist.append(city)
        for entry in cities[item][city]:
            print(city, " has ", entry, " first data from : ", cities[item][city][entry][0][0], " to ", cities[item][city][entry][-1][0])
    #print(item, " (", len(citylist), ") : \n", citylist,"\n--------------------------------------------------------------------------------------------------------------------")
    #input()

print(cities["United States"]["Manhattan"])
