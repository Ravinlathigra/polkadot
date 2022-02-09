import streamlit as st
import plotly
from tool_staking import * 

st.title("Visualizing the Relationship Between Inflation and Annaul Yield")

st.markdown("---")


st.sidebar.image("data:image/png;base64,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", width = 50)

st.sidebar.header("Calculation Parameters")

baseline_inflation = st.sidebar.slider('What is the Base Inflation Rate (%)', 0.0, 100.0, 2.5,.5)/100
ideal_staking = st.sidebar.slider('What is the ideal percent of Staked DOT (%)', 0, 100,50,1)/100
ideal_inflation = st.sidebar.slider('What is the ideal Inflation Rate (%)', 0, 100,10,1)/100
distance_metric = st.sidebar.slider('During Exponential Decay, what distance should there be no more than a 50%% decrease in Yield', 0.0,1.0,0.05)

inf = inflation(baseline_inflation,ideal_inflation,ideal_staking,distance_metric)

df = inf.create_df(.1,1,100)
yield_curves = inf.plot_staking_rewards("Polkadot Staking Rewards")
yield_curves.update_layout(width=1100,height=900) 

st.plotly_chart(yield_curves, use_container_width=False,height=600,width = 1000)
