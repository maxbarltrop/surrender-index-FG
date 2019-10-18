import pandas as pd 
import numpy as np
import os 
import math
import matplotlib
from matplotlib import pyplot as plt

data = pd.read_csv("fieldGoalData.csv")

teams =  { 
"CRD": "Cardinals",
"ATL": "Falcons",
"RAV": "Ravens",
"BUF": "Bills",
"CAR": "Panthers",
"CHI": "Bears",
"CIN": "Bengals",
"CLE": "Browns",
"DAL": "Cowboys",
"DEN": "Broncos",
"DET": "Lions",
"GNB": "Packers",
"HTX": "Texans",
"CLT": "Colts",
"JAX": "Jaguars",
"KAN": "Chiefs",
"MIA": "Dolphins",
"MIN": "Vikings",
"NWE": "Patriots",
"NOR": "Saints",
"NYG": "Giants",
"NYJ": "Jets",
"RAI": "Raiders",
"PHI": "Eagles",
"PIT": "Steelers",
"SDG": "Chargers",
"SEA": "Seahawks",
"SFO": "49ers",
"RAM": "Rams",
"TAM": "Buccaneers",
"OTI": "Titans",
"WAS": "Redskins"
}

data = data.drop('Yds',axis=1)
data = data.drop('EPA',axis=1)

dates = data['Date']
data = data.drop('Date',axis=1)

detail = data['Detail']
data = data.drop('Detail',axis=1)

locations = (data['Location'])
locationMultiplier = []
deficitMultiplier = []
timeMultiplier = []
distanceMultiplier = []
scores = (data['Score'])

for i in range (len(locations)):
    if data['Opp'][i] == teams[(locations[i])[0:3]] : 
        locationMultiplier.append(int(locations[i].split(' ')[1]))
    else: 
        locationMultiplier.append(100 - int(locations[i].split(' ')[1]))
    if locationMultiplier[i] >= 40:
        locationMultiplier[i] = 1
    else: 
        locationMultiplier[i] = 1.04 ** (40 - locationMultiplier[i])

    score = scores[i].split('-')
    scoreDifference = int(score[0]) - int(score[1])
    scoreMultiplier = 0
    if scoreDifference > 7: 
        scoreMultiplier = 1.5
    elif scoreDifference >= 5:
        scoreMultiplier = 1 
    elif scoreDifference >= 1:
        scoreMultiplier = 2 
    elif scoreDifference == 0: 
        scoreMultiplier = 1.5
    elif scoreDifference >= -3:
        scoreMultiplier = 0.5 
    elif scoreDifference >= -7: 
        scoreMultiplier = 3 
    elif scoreDifference >= -10:
        scoreMultiplier = 1 
    else: 
        scoreMultiplier = 2.5
    deficitMultiplier.append(scoreMultiplier)

    secondsSinceHalf = 900 - ((int((data['Time'][i]).split(':')[0]) * 60) + int(((data['Time'][i]).split(':'))[1]))
    if data['Quarter'][i] == 1 or data['Quarter'][i] == 2 : 
        timeMultiplier.append(1)
    else:
        if data['Quarter'][i] == 4: 
            secondsSinceHalf += 900 
        if secondsSinceHalf < 1680: 
            timeMultiplier.append((1 + math.log(secondsSinceHalf,5)**2))
        else: 
            timeMultiplier.append(2)

    distance = int(data['Yards'][i])
    if distance >= 10: 
        distanceMultiplier.append(0.2)
    elif distance >= 7: 
        distanceMultiplier.append(0.4)
    elif distance >= 4: 
        distanceMultiplier.append(0.6)
    elif distance >= 2: 
        distanceMultiplier.append(0.8)
    else:
        distanceMultiplier.append(1)
 
      
data['Time Multiplier'] = timeMultiplier
data['Deficit Multiplier'] = deficitMultiplier
data['Location Multiplier'] = locationMultiplier
data['Distance Multiplier'] = distanceMultiplier

sIndex = [] 
for i in range (len(data.iloc[:,0])): 
    sIndex.append(data['Time Multiplier'][i] * data['Deficit Multiplier'][i] * data['Location Multiplier'][i] * data['Distance Multiplier'][i])
data['Index'] = sIndex 

col = []
for key in teams:
    col.append(teams[key])

zeros = np.zeros((2,32),dtype=int)

teamKicks = {}
teamSum = {}
teamAvg = {} 
for team in teams:
    teamKicks[teams[team]] = 0 
    teamSum[teams[team]] = 0.0 

for i in range (len(data.iloc[:,0])): 
    teamKicks[data['Tm'][i]] = teamKicks[data['Tm'][i]] + 1 
    teamSum[data['Tm'][i]] = teamSum[data['Tm'][i]] + data['Index'][i] 

for team in teamKicks: 
    teamAvg[team] = teamSum[team] / teamKicks[team]

teamNames = [] 
teamIndex = [] 
for team in teams: 
    teamNames.append(team)
    teamIndex.append(teamAvg[teams[team]])

sIndex.sort(reverse=True)


plt.subplot()
x = np.arange(100)
plt.bar(x, sIndex[0:100], align='center', alpha=0.6)
plt.xticks(None)
plt.ylabel('Surrender Index')
plt.title('Field Goal Surrender Index - Top 100')
plt.subplot()
plt.figure(figsize=(12,6))
y = np.arange(0,320,10) 
plt.bar(y, teamIndex, align='center', alpha=0.6, width = 5)
plt.xticks(y, labels = teamNames, fontsize = 7)
plt.ylabel('Average SI')
plt.title('Average Field Goal Index by NFL Team - Last 500 League Attempts')
plt.show()

