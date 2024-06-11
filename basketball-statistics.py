import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.title('NBA Player Stats Hub')

st.markdown("""
This app performs simple webscraping of NBA player stats data!
* **Python libraries:** base64, pandas, streamlit
* **Data source:** [Basketball-reference.com](https://www.basketball-reference.com/).
""")

st.sidebar.header('User Filter Features')
selectedYear = st.sidebar.selectbox('Year', list(reversed(range(1950,2024))))

def load_data(year):
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
    html = pd.read_html(url, header = 0)
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index) 
    raw = raw.fillna(0)
    playerstats = raw.drop(['Rk'], axis=1)
    return playerstats
playerstats = load_data(selectedYear)

# Sidebar - Team selection
sortedUniqueTeam = sorted(playerstats.Tm.unique())
selectedTeam = st.sidebar.multiselect('Team', sortedUniqueTeam, sortedUniqueTeam)

# Sidebar - Position selection
uniquePosition = ['C','PF','SF','PG','SG']
selectedPosition = st.sidebar.multiselect('Position', uniquePosition, uniquePosition)

# Filtering data
dfSelectedTeam = playerstats[(playerstats.Tm.isin(selectedTeam)) & (playerstats.Pos.isin(selectedPosition))]

st.header('Player Stats of Selected Team(s)')
st.write('Data Dimension: ' + str(dfSelectedTeam.shape[0]) + ' rows and ' + str(dfSelectedTeam.shape[1]) + ' columns.')
st.dataframe(dfSelectedTeam)
