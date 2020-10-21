import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from functions.get_data import get_data
from functions.get_data import compute_returns
import plotly.express as px

DIR_TICKERS = 'data/tickers.txt'
MAX_PERIOD = 5*365

@st.cache(allow_output_mutation=True, show_spinner=False)
def get_tickers(dir=DIR_TICKERS):
    df = pd.read_excel('data/tickers.xlsx')
    # df.to_excel('data/tickers.xlsx', sheet_name='sheet1', index=False)
    return df

@st.cache(allow_output_mutation=True, show_spinner=False)
def make_figure(data, periods, fig_width=1000, fig_height=1000, font_size=10, 
                sorting=1, asc_desc="total ascending", within_group=False):
  

    fig = px.bar(data, x="Return (%)", y="Ticker", facet_col="Period", color="Group", 
                 facet_col_spacing=.025, width=fig_width, height=fig_height, 
                 hover_data=["Ticker","Name","Return (%)","Group", "Period"], 
                 color_discrete_sequence=px.colors.qualitative.Prism)
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', font=dict(
            size=font_size
        ))
    
    fig.layout.xaxis.update(matches=None)

    fig.layout.xaxis2.update(matches=None)

    fig.layout.xaxis3.update(matches=None)

    fig.layout.xaxis4.update(matches=None)

    fig.layout.xaxis5.update(matches=None)

    #return fig
    if not within_group:
        if sorting == periods[0]:
            fig.layout.yaxis.update(categoryorder=asc_desc)
        elif sorting == periods[1]:
            fig.layout.yaxis2.update(categoryorder=asc_desc)
        elif sorting == periods[2]:
            fig.layout.yaxis3.update(categoryorder=asc_desc)
        elif sorting == periods[3]:
            fig.layout.yaxis4.update(categoryorder=asc_desc)
        elif sorting == periods[4]:
            fig.layout.yaxis5.update(categoryorder=asc_desc)


    return fig

st.beta_set_page_config(layout="wide")

st.title('Market dashboard')
# import tickers
with st.spinner("Updating tickers..."):
    tickers = get_tickers(dir=DIR_TICKERS)


st.sidebar.title("User settings")
if st.sidebar.button("Update tickers"):
    tickers = pd.read_excel('data/tickers.xlsx')

comput = st.sidebar.selectbox("Choose computation",["Close", "High", "Low", "Open", "Volume"])

# convert to string
tickers_input = ' '.join(map(str, tickers['Ticker'].values.tolist()))

tickers_list = tickers['Ticker'].values.tolist()
tickers_list.sort()
# choose benchmark
benchmark = st.sidebar.selectbox("Select benchmark",  [1] + tickers_list)


# periods
expander_periods = st.sidebar.beta_expander("Define periods")
with expander_periods:

    # periods input
    period1 = expander_periods.number_input("Period 1", min_value=1, max_value=MAX_PERIOD, value=1, step=1)
    period2 = expander_periods.number_input("Period 2", min_value=1, max_value=MAX_PERIOD, value=5, step=1)
    period3 = expander_periods.number_input("Period 3", min_value=1, max_value=MAX_PERIOD, value=30, step=1)
    period4 = expander_periods.number_input("Period 4", min_value=1, max_value=MAX_PERIOD, value=180, step=1)
    period5 = expander_periods.number_input("Period 5", min_value=1, max_value=MAX_PERIOD, value=365, step=1)
    
    # add periods in list
    periods = [period1, period2, period3, period4, period5]
    sorts = expander_periods.selectbox("Sort by period", periods)
    within_group = expander_periods.checkbox("Sort within group", value=False)


expander_figureOpt = st.sidebar.beta_expander("Figure options")

# figure options
with expander_figureOpt:
    ascending = expander_figureOpt.checkbox("Descending", value=False)
    fig_width = expander_figureOpt.slider("Figure width", min_value=100, max_value=2000, value=1000, step=1)
    fig_height = expander_figureOpt.slider("Figure height", min_value=100, max_value=2000, value=1000, step=1)
    font_size = expander_figureOpt.number_input("Font size", min_value=4, max_value=30, value=10, step=1)

if ascending:
    asc_desc = "total ascending"
else:
    asc_desc = "total descending"

# compute returns
data = get_data(tickers=tickers_input, period="10y")

rets = [compute_returns(data=data, column=comput, period=p, benchmark=benchmark) for p in periods]
rets_conc = round(pd.concat(rets, axis=1)*100, ndigits=2)
rets_conc.columns = periods
rets_conc['Ticker'] = rets_conc.index


# expander tickers
expander_ticker = st.beta_expander("Show tickers")
with expander_ticker:
    t = expander_ticker.multiselect("Select tickers", options=tickers_list, default=tickers_list)

select_tick = rets_conc[rets_conc['Ticker'].isin(t)]
select_tick = pd.concat([select_tick.set_index('Ticker'), tickers.set_index('Ticker')], axis=1, join='inner').reset_index()
select_tick = select_tick.sort_values(['Group',sorts], ascending=ascending)
select_tick.dropna(inplace=True)
df_plot_long = pd.melt(select_tick, id_vars=['Ticker','Name', 'Group'], var_name='Period', value_name='Return (%)')

# make figure
with st.spinner("Updating figure..."):
    fig = make_figure(data=df_plot_long, fig_width=fig_width, fig_height=fig_height, 
                      font_size=font_size, sorting = sorts, periods=periods,
                      asc_desc=asc_desc, within_group=within_group)
    st.plotly_chart(fig, use_container_width=False)




