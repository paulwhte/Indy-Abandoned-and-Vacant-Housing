"""
from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

#Marion count is located at index 911

print(counties["features"][911])
"""

f = open("data/Abandoned_And_Vacant_Zip_Address_Status.csv", "r")

"""
Calculations to do:
1. Total abandoned/vacant
2. Total abandoned
3. Total vacant
4. Number per zip code

"""
dataList = []
abandonedCount = 0
vacantCount = 0
zipDict = {}

for line in f:
    #indexes: 0=zip, 1=address, 2=status
    line = line.split(",")

    #Calc abandoned/vacant
    dataList.append(line)
    if line[2] == "Abandoned\n":
        abandonedCount += 1
    elif line[2] == "Vacant\n":
        vacantCount += 1

    #Zip code count
    if line[0] != "ZIPCODE" and line[0] != "": #Ignore header
        #Check if zip is already in dict
        zip = (line[0])
        if zip in zipDict.keys():
            zipDict[zip] += 1
        else:
            zipDict[zip] = 1

print(f"Abandoned housing: {abandonedCount}")
print(f"Vacant housing: {vacantCount}")
print(f"Total: {abandonedCount+vacantCount}")
print(zipDict)
zipDict = dict(sorted(zipDict.items(), key=lambda item: item[1]))
#zipDict = dict(sorted(zipDict.items())) #Sorts dict by zip code
print(zipDict)

import plotly.express as px

#Build parallel lists of zip codes and total
zipList = []
totalsList = []
for key in zipDict:
    zipList.append(key)
    totalsList.append(zipDict[key])


fig = px.bar(x=zipList, y=totalsList, title="Number of abandoned and vacant homes in Indianapolis by ZIP code")
fig.show()