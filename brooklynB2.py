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

print(bridge)

# ── Sidebar filters ───────────────────────────
st.sidebar.header('Filters')

# Stretch goal B: radio moved to sidebar
volume = st.sidebar.radio('Traffic volume', ('Hourly', 'Daily', 'Weekly'))

# Stretch goal C: weather filter
weathers = ['All'] + sorted(bridge['weather_summary'].dropna().unique().tolist())
weather = st.sidebar.selectbox('Weather', weathers)

# ── Apply filters ─────────────────────────────
df = bridge.copy()

if weather != 'All':
    df = df[df['weather_summary'] == weather]

if volume == 'Hourly':
    pass  # no resampling needed
elif volume == 'Daily':
    df = df[['pedestrians', 'to_manhattan', 'to_brooklyn']].resample('D').sum()
else:
    df = df[['pedestrians', 'to_manhattan', 'to_brooklyn']].resample('W').sum()

# ── Page header ───────────────────────────────
st.title('Brooklyn Bridge Crossings')
st.subheader('Pedestrian traffic Oct 2017 – Jun 2018')
st.markdown('---')

# ── Metric cards ──────────────────────────────
col1, col2 = st.columns(2)
col1.metric('Total pedestrians', f"{int(df['pedestrians'].sum()):,}")
col2.metric(f'Avg per {volume.lower()}', f"{int(df['pedestrians'].mean()):,}")

st.markdown('---')

# ── Line chart ────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 4))

# Stretch goal A: two lines instead of one
ax.plot(df.index, df['to_manhattan'], label='To Manhattan', color='steelblue', linewidth=1.5)
ax.plot(df.index, df['to_brooklyn'], label='To Brooklyn', color='tomato', linewidth=1.5)

ax.set_xlabel('Date')
ax.set_ylabel(f'Pedestrians ({volume.lower()})')
ax.set_title(f'{volume} pedestrian traffic across Brooklyn Bridge')
ax.xaxis.set_major_formatter(DateFormatter('%m-%y'))
ax.legend()

st.pyplot(fig)