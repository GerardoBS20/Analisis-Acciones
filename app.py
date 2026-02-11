#import pandas as pd
import streamlit as st
import yfinance as yf
import numpy as np
from datetime import date

@st.cache_data(ttl=3600)
def obtener_datos_ticker(ticker_symbol, start_date, end_date):
    ticker = yf.Ticker(ticker_symbol)
    
    # Histórico
    df = ticker.history(start=start_date, end=end_date)
    
    # Info (puede fallar por rate limit)
    try:
        info = ticker.fast_info  # mucho más ligero que .info
        #dividend_yield = info.get("dividendYield", np.nan)
        dividend_yield = ticker.dividends

        # Payout Ratio (EPS-based)
        payout_ratio = info.get("payoutRatio", np.nan)
        # Debt to Equity
        debt_to_equity = info.get("debtToEquity", np.nan) / 100 if info.get("debtToEquity") else np.nan
    except Exception:
        dividend_yield = np.nan,
        payout_ratio = np.nan
        debt_to_equity = np.nan

    return df, dividend_yield,payout_ratio,debt_to_equity


def main():
    ticker_symbol = st.text_input("Ingrese el ticker de la empresa")

    fecha_usuario = st.date_input(
    label="Selecciona una fecha",
    value=date.today(),        # valor por defecto
    format="YYYY-MM-DD"         # formato visible
    )

    # 2. Convertir a string en formato YYYY-MM-DD
    fecha_usuario_str = fecha_usuario.strftime("%Y-%m-%d")

    # 3. Fecha actual
    fecha_actual = date.today()
    fecha_actual_str = fecha_actual.strftime("%Y-%m-%d")

    st.write(ticker_symbol)

    if st.sidebar.button("Predict", key="predict"):
        #define the ticker symbol
        tickerDf, dividend_yield ,payout_ratio,debt_to_equity = obtener_datos_ticker(
        ticker_symbol,
        fecha_usuario_str,
        fecha_actual_str
        )

        st.dataframe(tickerDf)
        st.write("Dividend Yield:", dividend_yield)
        st.write("payout_ratio:", payout_ratio)
        st.write("debt_to_equity :", debt_to_equity)
        

if __name__ == '__main__':
    main()