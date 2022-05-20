import pandas as pd
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
# teste

stocks_list = ["BBAS3.SA", "PETR4.SA", "BBAS3.SA", "MRFG3.SA", "PRIO3.SA",
               "VALE3.SA", "MGLU3.SA", "VIIA3.SA", "WEGE3.SA", "TASA4.SA"]

dict_line_colors = {'mv_7d': 'gray', 'mv_50d': 'green', 'mv_200d': 'blue'}


@st.cache
def load_data(stock_lst=stocks_list):
    start_date = "2016-01-01"
    end_date = pd.to_datetime("today").date().isoformat()
    fields = ["Close", "Open", "High", "Low"]
    data = yf.download(tickers=stock_lst, start=start_date, end=end_date)[fields]
    return data


st.set_page_config(
        "Dashboard by AVR",
        initial_sidebar_state="expanded",
        layout="wide",
    )


# Load the data
df_full = load_data()

# SIDE BAR
st.sidebar.header("Stock to be analysed")
stock_selected = st.sidebar.selectbox('Stock to select', stocks_list)

df = df_full[[('Close', stock_selected), ('Open', stock_selected),
              ('High', stock_selected), ('Low', stock_selected)]]
df = df.droplevel(1, axis=1)


# MAIN
st.title(stock_selected)


def plot_candle_stick(df_, name='ticker', lines=[]):
    trace = {
      'x': df_.index,
      'open': df_.Open,
      'close': df_["Close"],
      'high': df_.High,
      'low': df_.Low,
      'type': 'candlestick',
      'name': name,
      'showlegend': False
    }

    data = [trace]
    layout = go.Layout()
    fig = go.Figure(data=data, layout=layout)
    if len(lines) > 0:
        for c in lines:
            fig.add_trace(
                go.Scatter(x=list(df_.index),
                           y=df_[c],
                           mode='lines',
                           line=dict(color=dict_line_colors[c]),
                           name=c))
    fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])])
    return fig

# mma
# df['mv_7d_1.5_std'] = df.Close.rolling(7).mean() + df.Close.rolling(7).std()*1.5


df['mv_7d'] = df["Close"].rolling(7).mean()
df['mv_50d'] = df["Close"].rolling(50).mean()
df['mv_200d'] = df["Close"].rolling(200).mean()

st.plotly_chart(
    plot_candle_stick(df, name=stock_selected, lines=['mv_7d', 'mv_50d', 'mv_200d']),
    use_container_width=True)



