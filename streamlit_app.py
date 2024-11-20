import streamlit as st
import pandas as pd
from pathlib import Path
import numpy as np
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title='Superman Demand Estimation')

@st.cache_data
def get_data():
    DATA_FILENAME = Path(__file__).parent/'data/AMR_Data.csv'
    df_amr = pd.read_csv(DATA_FILENAME)
    DATA_FILENAME = Path(__file__).parent/'data/EU_Data.csv'
    df_eu = pd.read_csv(DATA_FILENAME)
    DATA_FILENAME = Path(__file__).parent/'data/PAC_Data.csv'
    df_pac = pd.read_csv(DATA_FILENAME)
    
    return df_amr, df_eu, df_pac

def clear_input():
    st.session_state.actual = ''

df_amr, df_eu, df_pac = get_data()

amr = st.checkbox('AMR', on_change=clear_input)
eu = st.checkbox('Europe', on_change=clear_input)
pac = st.checkbox('PAC', on_change=clear_input)

df = pd.DataFrame(columns=['week', 'year_2', 'year_1'])
df['week'] = [0] * 20
df['year_2'][:15] = 0.
df['year_2'][15:] = np.nan
df['year_1'][:5] = np.nan
df['year_1'][5:] = 0.

if amr:
    df += df_amr
if eu:
    df += df_eu
if pac:
    df += df_pac
df['week'] = np.arange(1, 21, 1)

if amr or eu or pac:
    # Calculate price factor
    year_2_normalized = np.mean(df['year_2'][2:15])
    year_1_normalized = np.mean(df['year_1'][7:20])
    price_factor = (year_2_normalized - year_1_normalized) / (120 - 200)

    # Display slider for year_1 weight
    year_1_weight = st.slider(label='Last year seasonality weight', min_value=0., max_value=1., value=0.7)

    # Make estimate
    df['year_0_estimate'] = np.nan
    df['year_0_estimate'][:7] = df['year_2'][:7] + price_factor * (205 - 120)
    estimate_2 = df['year_2'][7:15] + price_factor * (205 - 120)
    estimate_1 = df['year_1'][7:15] + price_factor * (205 - 200)
    df['year_0_estimate'][7:15] = estimate_1 * year_1_weight + estimate_2 * (1 - year_1_weight)

    # Display input field for actual data
    st.text_input(label='Please input actual demand for Superman, starting from week 1, separated by comma, 15 inputs max', placeholder='240,200,150', key='actual', on_change=None)

    # Update estimate
    try:
        # Validate input
        actual_year_0 = [float(s.strip()) for s in st.session_state.actual.split(',')]
        assert(len(actual_year_0) <= 15)
        for value in actual_year_0:
            assert(value >= 0.)

        # Fit new price factor
        actual_mean = np.mean(actual_year_0)
        model = LinearRegression()
        model.fit(X=[[120.], [200.], [205.]], y=[[year_2_normalized], [year_1_normalized], [actual_mean]])
        price_factor_new = model.coef_[0]

        # Make new estimates
        df['year_0_estimate'][:len(actual_year_0)] = actual_year_0
        if len(actual_year_0) < 7:
            # Use year_2 for first portion and both for second portion
            df['year_0_estimate'][len(actual_year_0):7] = df['year_2'][len(actual_year_0):7] + price_factor_new * (205 - 120)
            estimate_2 = df['year_2'][7:15] + price_factor_new * (205 - 120)
            estimate_1 = df['year_1'][7:15] + price_factor_new * (205 - 200)
            df['year_0_estimate'][7:15] = estimate_1 * year_1_weight + estimate_2 * (1 - year_1_weight)
        else:
            # Use both for the second portion
            estimate_2 = df['year_2'][len(actual_year_0):15] + price_factor_new * (205 - 120)
            estimate_1 = df['year_1'][len(actual_year_0):15] + price_factor_new * (205 - 200)
            df['year_0_estimate'][len(actual_year_0):15] = estimate_1 * year_1_weight + estimate_2 * (1 - year_1_weight)
    except:
        pass

    # Draw the graph
    df.rename({'year_2':'Dwarf', 'year_1':'Princess', 'year_0_estimate':'Superman_Estimate'}, axis=1, inplace=True)
    st.line_chart(data=df, x='week', y=['Dwarf', 'Princess', 'Superman_Estimate'], color=('#2222ff', '#7777ff', '#ff0000'))

    # Display estimate
    if st.checkbox('Display all estimates'):
        st.dataframe(data=df[['week', 'Superman_Estimate']][:15], hide_index=True)
