import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import numpy
import plotly.io as pio
import textwrap

#Open the file, but only the columns we're interested in to avoid dropping many columns
surveillancedata = pd.read_csv('AtlasofSurveillance-20230405.csv', usecols= ["City", "State", "Technology", "Type of Juris", "Summary"])

#Make names more uniform
surveillancedata = surveillancedata.replace("New York", "New York City")
surveillancedata = surveillancedata[surveillancedata["City"].isin(['New York City', 'Houston', 'Los Angeles', 'Chicago'])]

#insert a linebreak instead of spaces in the technology column to make the sunburst look nicer. It looks bad in the dataset but I don't care enough to fix it
surveillancedata['Technology'] = surveillancedata['Technology'].str.replace(' ', '<br>')

#Create individual data sets for each of the cities
dataLA = surveillancedata[surveillancedata["City"].isin(['Los Angeles'])]
dataNY = surveillancedata[surveillancedata["City"].isin(['New York City'])]
dataCHI = surveillancedata[surveillancedata["City"].isin(['Chicago'])]
dataHTX = surveillancedata[surveillancedata["City"].isin(['Houston'])]

#Making a function that converts the dataset of each city to a figure

def fig(city):
    #Group all mentions of technologies into one to display better summaries
    city = city.groupby(['City', 'Type of Juris','Technology'], as_index=False).agg({'Technology': 'first', 'Summary': '<br>'.join})

    #Creates the figure using three layers(paths). I want the hovering text to be explanation of the surveillance used
    fig = px.sunburst(city, path=["City", "Type of Juris", "Technology"], hover_data=["Summary"])
    fig.update_traces(
        #label text orientation set for better viewing experience
        insidetextorientation='radial',
        #shows the summary, but hides all the dumb extra details for clarity
        hovertemplate='%{customdata[0]}<extra></extra>'
        )
    fig.show()
    return fig

dataNY = fig(dataNY)
graphLA = fig(dataLA)
graphCHI = fig(dataCHI)
graphHTX = fig(dataHTX)
#pio.write_html(graphNY, file="index1.html", auto_open=True)
#pio.write_html(graphLA, file="index2.html", auto_open=True)
#pio.write_html(graphCHI, file="index3.html", auto_open=True)