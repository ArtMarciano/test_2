import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

@st.cache_data
def load_data():
    return pd.read_csv(
        'brooklyn_bridge_pedestrians.csv',
        parse_dates=True,
        index_col='hour_beginning'
    )

bridge = load_data()

st.title('Brooklyn Bridge Crossings')
st.subheader('Pedestrian traffic Oct 2017 – Jun 2018')
st.markdown('---')

volume = st.radio('Traffic volume', ('Hourly', 'Daily', 'Weekly'))

if volume == 'Hourly':
    df = bridge
elif volume == 'Daily':
    df = bridge[['pedestrians','to_manhattan','to_brooklyn']].resample('D').sum()
else:
    df = bridge[['pedestrians','to_manhattan','to_brooklyn']].resample('W').sum()

col1, col2 = st.columns(2)
col1.metric('Total pedestrians', f"{int(df['pedestrians'].sum()):,}")
col2.metric('Avg per period', f"{int(df['pedestrians'].mean()):,}")

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(df.index, df['pedestrians'])
ax.set_xlabel('Date')
ax.set_ylabel(f'Pedestrians ({volume.lower()})')
ax.xaxis.set_major_formatter(DateFormatter('%m-%y'))
st.pyplot(fig)