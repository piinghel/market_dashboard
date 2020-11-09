import streamlit as st
import pandas as pd
import plotly.express as px
from numpy.lib.stride_tricks import as_strided
from numpy.lib import pad
import numpy as np
from functions.get_data import get_data


def rolling_spearman(seqa, seqb, window):
    """
    computes rolling spearman correlation
    """
    
    stridea = seqa.strides[0]
    ssa = as_strided(seqa, shape=[len(seqa) - window + 1, window], strides=[stridea, stridea])
    strideb = seqa.strides[0]
    ssb = as_strided(seqb, shape=[len(seqb) - window + 1, window], strides =[strideb, strideb])
    ar = pd.DataFrame(ssa)
    br = pd.DataFrame(ssb)
    ar = ar.rank(1)
    br = br.rank(1)
    corrs = ar.corrwith(br, 1)
    return pad(corrs, (window - 1, 0), 'constant', constant_values=np.nan)

def run_page2():
    
    st.sidebar.title("User settings")
    st.header("Correlation overview")
    ex_tickers = "CL=F, DX=F, GC=F, ES=F, NQ=F"
    tickers = st.text_input("Provide ticker symbols, split by comma", ex_tickers)
    df = get_data(tickers=tickers, period="20y")
    df_perc = df["Close"].pct_change(periods=1).dropna()
    ticker = st.sidebar.selectbox("Select ticker", list(df_perc.columns))

    ex_periods = "10, 20, 30, 60, 90, 120, 150, 180, 210"
    periods = st.text_input("Choose correlation periods, split by comma", ex_periods)
    periods = periods.split(",")
    # convert to integer
    periods = [int(p) for p in periods]
    
    # correlation for table
    store_corelations = {}
    for c in df_perc.columns:
        corr_tick = {}
        if c !=ticker:
            for p in periods:
                df_perc_period = df_perc.tail(p)
                corr_tick[p] = pd.DataFrame(df_perc_period[ticker]).corrwith(df_perc_period[c], axis=0, drop=False, method='spearman').values.tolist()[0]
            store_corelations[c] = corr_tick
    
    # precision
    precision = st.sidebar.number_input("Number of digits for precision", min_value=1, max_value=10, value=3)
    st.dataframe(pd.DataFrame(store_corelations).T.style.set_precision(precision))

    
    # correlation for figure
    corr_period = st.sidebar.slider("Choose correlation period figure", min_value=5, max_value=200, value=30)
    period_figure = st.sidebar.slider("Choose maximum period figure", min_value=100, max_value=2000, value=1000)
    corr_tick_rolling = {}
    for c in df_perc.columns:
        if c !=ticker:
                df_perc_period = df_perc.tail(period_figure)
                corr_tick_rolling[c] = rolling_spearman(df_perc_period[ticker].values, df_perc_period[c].values, corr_period)
    
    # plot fiure
    out = pd.DataFrame(corr_tick_rolling, index=df_perc_period.index).dropna().reset_index()
    out_long = pd.melt(out, id_vars='Date', value_vars=out.columns[1:])
    out_long = out_long.rename(columns={"variable": "Ticker", "value": "Correlation"})
    fig = px.line(out_long, x="Date", y="Correlation", title=f'Rolling correlations with {ticker}', color="Ticker")
    st.plotly_chart(fig, use_container_width=True)