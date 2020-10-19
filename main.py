import streamlit as st
import yfinance as yf
import pandas as pd
from functions.get_data import get_data
from functions.get_data import compute_returns

st.title('Market dashboard')
# import tickers
tickers = pd.read_table('data/tickers.txt', header=0)
# convert to string
tickers_str = ' '.join(map(str, tickers['ticker'].values.tolist()))

comput = st.sidebar.selectbox("Choose computation",["Close", "High", "Low", "Open", "Volume"])
tickers_input = st.sidebar.text_area("Input tickers here, split by space", tickers_str)
period1 = st.sidebar.number_input("Period 1", min_value=1, max_value=1000, value=1, step=1)
period2 = st.sidebar.number_input("Period 2", min_value=1, max_value=1000, value=5, step=1)
period3 = st.sidebar.number_input("Period 3", min_value=1, max_value=1000, value=30, step=1)
period4 = st.sidebar.number_input("Period 4", min_value=1, max_value=1000, value=365, step=1)
period5 = st.sidebar.number_input("Period 5", min_value=1, max_value=1000, value=180, step=1)
periods = [period1, period2, period3, period4, period5]
sorts = st.sidebar.selectbox("Sort by", periods)
ascending = st.sidebar.checkbox("Ascending", value=False)
data = get_data(tickers=tickers_input,period="2y")
rets = [compute_returns(data=data, column=comput, period=p) for p in periods]
rets_conc = round(pd.concat(rets, axis=1)*100,2)
rets_conc.columns = periods
st.write(rets_conc.sort_values(sorts, ascending=ascending))





