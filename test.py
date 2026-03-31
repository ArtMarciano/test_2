import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


st.title("hello world")
st.header('this is steamlit')
st.subheader("you will be able to start creating things")
st.text("you will be able to start creating your project")
st.code("a = 123\n" \
"import matplotlib as plt\n" \
"plt.show()")

st.markdown('----')
st.header("lets display some data")

df = pd.read_csv('https://raw.githubusercontent.com/ArtMarciano/datasets/refs/heads/main/tips.csv')
st.dataframe(df)

# Slider widget — returns the selected value
tip_range = st.slider(
    'Filter by Tip amount',
    min_value=0.0,
    max_value=10.0,
    value=5.0
)

# Use the slider value to filter rows
filtered_df = df[df['tip'] <= tip_range]
st.write(f'Showing {len(filtered_df)} rows')
st.dataframe(filtered_df)



st.markdown('---')
st.subheader('Tip distribution')

# Create matplotlib figure and display it
fig, ax = plt.subplots()
ax.hist(filtered_df['tip'], bins=15, color='steelblue', alpha=0.7)
ax.set_xlabel('Tip amount ($)')
ax.set_ylabel('Count')
ax.set_title('Distribution of tips')
st.pyplot(fig)



# Add this after the slider line:

meal = st.radio(
    'Select meal time',
    ('All', 'Lunch', 'Dinner')
)

# Update the filter to use both widgets:
filtered_df = df[df['tip'] <= tip_range]
if meal != 'All':
    filtered_df = filtered_df[filtered_df['time'] == meal]

# Add this right after filtered_df is created:

st.markdown('---')
st.subheader('Summary')

col1, col2, col3 = st.columns(3)

col1.metric(
    label='Total rows',
    value=len(filtered_df)
)
col2.metric(
    label='Avg tip',
    value=f"${filtered_df['tip'].mean():.2f}"
)
col3.metric(
    label='Avg bill',
    value=f"${filtered_df['total_bill'].mean():.2f}"
)

# Replace the single chart section with this:

st.markdown('---')
st.subheader('Charts')

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.write('Tip distribution')
    fig1, ax1 = plt.subplots()
    ax1.hist(filtered_df['tip'], bins=15,
             color='steelblue', alpha=0.7)
    ax1.set_xlabel('Tip ($)')
    st.pyplot(fig1)

with chart_col2:
    st.write('Bill distribution')
    fig2, ax2 = plt.subplots()
    ax2.hist(filtered_df['total_bill'], bins=15,
             color='tomato', alpha=0.7)
    ax2.set_xlabel('Bill ($)')
    st.pyplot(fig2)

# Replace the charts + dataframe sections with tabs:

tab1, tab2, tab3 = st.tabs(['Data', 'Charts', 'Scatter'])

with tab1:
    st.write(f'{len(filtered_df)} rows')
    st.dataframe(filtered_df)

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        fig1, ax1 = plt.subplots()
        ax1.hist(filtered_df['tip'], bins=15,
                 color='steelblue', alpha=0.7)
        ax1.set_xlabel('Tip ($)')
        st.pyplot(fig1)
    with col2:
        fig2, ax2 = plt.subplots()
        ax2.hist(filtered_df['total_bill'], bins=15,
                 color='tomato', alpha=0.7)
        ax2.set_xlabel('Bill ($)')
        st.pyplot(fig2)

with tab3:
    fig3, ax3 = plt.subplots()
    ax3.scatter(filtered_df['total_bill'],
                filtered_df['tip'], alpha=0.6)
    ax3.set_xlabel('Total bill ($)')
    ax3.set_ylabel('Tip ($)')
    st.pyplot(fig3)



