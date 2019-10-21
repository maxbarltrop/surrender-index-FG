This is based on 'The Search For The Saddest Punt in the World', an SB Nation video which defined a metric that evaluates the 
 quality of punting decisions in the NFL. The higher the 'Surrender Index', the more overly cautious the 
 punt, with the extremely high indexes highlighting poor coaching decisions.
 I attempted to replicate this rating for field goal decisions. I used dataFrames to handle
 the csv data, and added columns for each of the intermediate multipliers, and then the final 
 Surrender Index value.
 SB Nation's Surrender Index from 'The Search for the Saddest Punt in the World' uses the following formula: 
 (Field Position Multiplier) * (Yards-to-go Multiplier) * (Score Multiplier) * (Time Multiplier)
 My multipliers are calculated differently and are defined below, and skew the index more towards score differential vs. field position
 I pulled the field goal data from football reference, and based on the 
 limitations of their webapp, it includes the 500 most recent field goal attempts as of Oct. 10, 2019 
 I used matplotlib to plot both the top 100 'worst' field goal decisions, and the average by team.

It plots a lot more smoothly than the original surrender index with punts, yielding no big outliers since 
  it does not use any expoinential multipliers, but it does highlighting some very overly cautious kicking decisions 

I did not come up with the original idea, just thought it would be interesting to translate the surrender index to field goals
