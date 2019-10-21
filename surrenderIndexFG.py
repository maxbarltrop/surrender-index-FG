# This is based on 'The Search For The Saddest Punt in the World', which defined a metric that evaluates the 
# quality of punting decisions in the NFL. The higher the 'Surrender Index', the more overly cautious the 
# punt, with the extremely high indexes highlighting poor coaching decisions.
# I attempted to replicate this rating for field goal decisions. I used dataFrames to handle
# the csv data, and added columns for each of the intermediate multipliers, and then the final 
# Surrender Index value.
# SB Nation's Surrender Index from 'The Search for the Saddest Punt in the World' uses the following formula: 
# (Field Position Multiplier) * (Yards-to-go Multiplier) * (Score Multiplier) * (Time Multiplier)
# My multipliers are calculated differently and are defined below, and skew the index more towards score differential vs. field position
# I pulled the field goal data from football reference, and based on the 
# limitations of their webapp, it includes the 500 most recent field goal attempts as of Oct. 10, 2019 
# I used matplotlib to plot both the top 100 'worst' field goal decisions, and the average by team.

import pandas as pd 
import numpy as np
import os 
import math
import matplotlib
from matplotlib import pyplot as plt

data = pd.read_csv("fieldGoalData.csv") #Put the data from football-reference into a dataframe.

teams =  {  #Map the three-letter codes used by football-reference to team names
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

data = data.drop('Yds',axis=1) #Unnecessary data 
data = data.drop('EPA',axis=1)

dates = data['Date']  #Store the info that might be useful for different insights in a separate list 
data = data.drop('Date',axis=1)

detail = data['Detail']
data = data.drop('Detail',axis=1)

locations = (data['Location']) #Store the field positions in a separate list
locationMultiplier = []
deficitMultiplier = []
timeMultiplier = []
distanceMultiplier = []
scores = (data['Score'])

for i in range (len(data.iloc[:,0])):  #For every field goal in the data set
    if data['Opp'][i] == teams[(locations[i])[0:3]] : #If on the opponents side of the field (almost all values)
        locationMultiplier.append(int(locations[i].split(' ')[1]))
    else: 
        locationMultiplier.append(100 - int(locations[i].split(' ')[1])) #If not, subtract the yard number from 100
    if locationMultiplier[i] >= 40: #If farther than the other team's 40, no penalty, as the endzone is far and kicks from this distance are rare 
        locationMultiplier[i] = 1
    else: 
        locationMultiplier[i] = 1.04 ** (40 - locationMultiplier[i]) #Use an exponential scale, the closer to the endzone, the worse the kick

    score = scores[i].split('-')
    scoreDifference = int(score[0]) - int(score[1]) #Calculate the teams deficit, and apply a multiplier 
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
    elif scoreDifference >= -7: #Losing by more than three, but less than 7 is the worst field goal situation -> highest multiplier
        scoreMultiplier = 3 
    elif scoreDifference >= -10:
        scoreMultiplier = 1 
    else: 
        scoreMultiplier = 2.5
    deficitMultiplier.append(scoreMultiplier)

    secondsSinceHalf = 900 - ((int((data['Time'][i]).split(':')[0]) * 60) + int(((data['Time'][i]).split(':'))[1])) #parse the time to figure out how long until the end of the game
    if data['Quarter'][i] == 1 or data['Quarter'][i] == 2 : #No penalty in the first or second quarter
        timeMultiplier.append(1)
    else:
        if data['Quarter'][i] == 4: 
            secondsSinceHalf += 900 
        if secondsSinceHalf < 1680: 
            timeMultiplier.append((1 + math.log(secondsSinceHalf,5)**2)) #Use a logarithmic scale instead of the exponential scale used in the surrender index for punts
        else:                                                               #Since sometimes late-game field goals make sense 
            timeMultiplier.append(2) #Lesser penaly for a last-two-minute field goal, since presumably this is a necessary kick vs. an overly cautious decision 

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

sIndex = []  #sInde for 'Surrender Index'
for i in range (len(data.iloc[:,0])): #Aggregate the multipliers for each kick, store in a new list 
    sIndex.append(data['Time Multiplier'][i] * data['Deficit Multiplier'][i] * data['Location Multiplier'][i] * data['Distance Multiplier'][i]) 
data['Index'] = sIndex  #Add the list to the dataframe

col = []
for key in teams:
    col.append(teams[key]) #Create a list of the team names 

teamKicks = {} #Store the number of kicks and sum in a dictionary to compute team averages 
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

print (sum(sIndex)/len(sIndex))

#Plot the two graphs
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

