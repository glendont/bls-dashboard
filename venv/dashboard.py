import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import panel as pn
import datetime
from matplotlib.legend_handler import HandlerBase
from matplotlib.text import Text
import matplotlib.patches as mpatches
import plotly.graph_objects as go

pn.extension()

IndivPerfData = pd.read_csv('IndivPerfExcel.csv')
SamplingData = pd.read_csv('Sampling.csv')


#Progress Meter
SamplingData['Legitimacy']=1

#Progress Calculation
completed = SamplingData[SamplingData.Progress==1]
notcompleted =  SamplingData[SamplingData.Progress==0]
progresscalculation = round((len(completed) / (len(completed)+len(notcompleted)) )*100,2)


#Data Collection Countplot Graph
progressgraph, axes = plt.subplots(1, 1, figsize=(20, 11))
ax= sb.countplot(y='Progress',palette="ch:.25",data=SamplingData)
currentdatetime = datetime.datetime.now()
ax.set_xlabel('Sample Size')
ax.set_ylabel('Status')
ax.set_title('Data Collection Progress\n Updated as of : '+ str(currentdatetime.strftime("%x")) + '\nCompletion: ' + str(progresscalculation) + '%')

#Legend
tobecollected = mpatches.Patch(color='#ded3c4')
collected = mpatches.Patch(color='black')
plt.legend([tobecollected, (tobecollected, collected)],["Samples to be Collected", "Samples Collected"])

#Progress Chart / Meter
date = str(currentdatetime.strftime("%x"))
progressmeter = go.Figure(go.Indicator(
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = len(completed),
    mode = "gauge+number+delta",
    title = {"text": "Data Collection<br><span style='font-size:0.8em;color:gray'>Progress Meter</span><br><span style='font-size:0.8em;color:gray'>Updated as of: </span>"+date},
#     delta = {'reference': 500},
    gauge = {'axis': {'range': [None, 500]},
             'steps' : [
                 {'range': [0, 250], 'color': "lightgray"},
                 {'range': [250, 750], 'color': "gray"}],
             'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 990}}))

progressmeter.update_layout(
    autosize=False,
    width=1300,
    height=500,
    margin=dict(l=10, r=200, t=100, b=50),
    paper_bgcolor="white",
)

#Creation of Tabs
tabs = pn.Tabs()
tabs.append(('Progress Chart', progressgraph))
tabs.append(('Progress Meter', progressmeter))
tabs.show()