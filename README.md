# Field Goal Surrender Index (Python, Matplotlib)

This is based on 'The Search For The Saddest Punt in the World', an [SB Nation video](https://www.youtube.com/watch?v=F9H9LwGmc-0) which defined a metric that evaluates punting decisions in the NFL. The higher the 'Surrender Index', the more overly cautious the 
 punt, with the extremely high indexes highlighting overly conservative decisions.
 
 I tried to compute an equivalent metric for decisions to kick field goals. I used dataFrames to handle
 the csv data, and added columns for each of the intermediate multipliers, and then computed the final 
 'Surrender Index' value.
 
 I pulled the field goal data from football reference, and based on the 
 limitations of their webapp, it includes the 500 most recent field goal attempts as of Oct. 10, 2019 
 

 I used matplotlib to plot both the top 100 'worst' decisions and the average by team.
