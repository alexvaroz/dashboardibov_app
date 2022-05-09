import pandas as pd
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go


@st.cache
def load_data():
    stocks_list = ["PRIO3.SA"]  # , "PETR4.SA", "BBAS3.SA", "MRFG3.SA"]
    start_date = "2017-01-01"
    end_date = pd.to_datetime("today").date().isoformat()
    fields = ["Adj Close", "Open", "High", "Low"]
    data = yf.download(tickers=stocks_list, start=start_date, end=end_date)[fields]
    raw_info = yf.Ticker(stocks_list[0])
    data_info = {"symbol": raw_info.info['symbol'],
                 "sector": raw_info.info['sector'],
                 "summary": raw_info.info['longBusinessSummary']}
    return data, data_info


# Load the data
df, df_info = load_data()

fig = go.Figure()
fig.add_trace(go.Candlestick(x=df.index,
                             open=df["Open"],
                             high=df["High"],
                             low=df["Low"],
                             close=df["Adj Close"],
                             name = "market data"))
fig.update_layout(title = "Stock Prices", yaxis_title = "Stock Price (R$)")
fig.update_xaxes(rangeslider_visible=True)

# hide weekends
fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])])

# SIDE BAR
st.sidebar.header(df_info["symbol"])
st.sidebar.info(df_info["sector"])

# Slider de seleção do ano
st.sidebar.subheader("Ano")
year_to_filter = st.sidebar.slider("Escolha o ano desejado:",
                                   int(df.index.year.min()),
                                   int(df.index.year.max()),
                                   int(df.index.year.min()))
st.sidebar.info(df_info["summary"])

# MAIN
st.title(df_info["symbol"])

st.plotly_chart(fig, use_container_width=True)

