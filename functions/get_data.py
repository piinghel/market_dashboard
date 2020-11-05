import yfinance as yf
import streamlit as st



#@st.cache(show_spinner=False)
def get_data(tickers=None, 
             period="1y", 
             interval="1d",
             group_by="column",
             auto_adjust=True,
             prepost=True,
             threads=True,
             proxy=None):
        
    data = yf.download(
    # tickers list or string as well
    tickers = tickers,

    # use "period" instead of start/end
    # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
    # (optional, default is '1mo')
    period = period,

    # fetch data by interval (including intraday if period < 60 days)
    # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
    # (optional, default is '1d')
    interval = interval,

    # group by ticker (to access via data['SPY'])
    # (optional, default is 'column')
    group_by = group_by,

    # adjust all OHLC automatically
    # (optional, default is False)
    auto_adjust = auto_adjust,

    # download pre/post regular market hours data
    # (optional, default is False)
    prepost = prepost,

    # use threads for mass downloading? (True/False/Integer)
    # (optional, default is True)
    threads = threads,

    # proxy URL scheme use use when downloading?
    # (optional, default is None)
    proxy = proxy)
    
    return data


def compute_returns(data, column="Close", period=1, benchmark=1):

    
    data = data[column]
    # check if benchmark is not 1
    if  benchmark !=1:   
        data = data.div(data[benchmark], axis=0)
    
    # compute return
    ret = data.iloc[-1]/data.iloc[-(period+1)] - 1 
    ret.fillna(method='ffill', inplace=True)   
    ret.columns = period

    return ret






