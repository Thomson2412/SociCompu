import csv
from collections import defaultdict

cities = defaultdict(list)
cities["India"] = defaultdict(list)
cities["United Kingdom"] = defaultdict(list)
cities["United States"] = defaultdict(list)

files = ["waqi-covid19-airqualitydata-2019Q1.csv","waqi-covid19-airqualitydata-2019Q2.csv",
        "waqi-covid19-airqualitydata-2019Q3.csv","waqi-covid19-airqualitydata-2019Q4.csv",
        "waqi-covid19-airqualitydata-2020.csv"]

required = ["no2","pm25"]

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
                    cities["India"][row[2]].append(row[0:1] + row[3:])
            if row[1] == 'GB':
                if row[3] in required:
                    cities["United Kingdom"][row[2]].append(row[0:1] + row[3:])
            if row[1] == 'US':
                if row[3] in required:
                    cities["United States"][row[2]].append(row[0:1] + row[3:])

for item in cities:
    citylist = []
    for city in cities[item]:
        citylist.append(city)
        for entry in cities[item][city]:
            print(city, " = ", entry)
            break
    print(item, " (", len(citylist), ") : \n", citylist,"\n--------------------------------------------------------------------------------------------------------------------")
    input()
