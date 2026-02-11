#import pandas as pd
import streamlit as st
import yfinance as yf
import numpy as np
from datetime import date

def main():
    company_ticker = st.text_input("Ingrese el ticker de la empresa")

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

    st.write(company_ticker)

    if st.sidebar.button("Predict", key="predict"):
        #define the ticker symbol
        tickerSymbol = company_ticker
        st.write("Wait 1 minute for the Results")
        st.write("Making predictions...")

        #get data on this ticker
        tickerData = yf.Ticker(tickerSymbol)

        #get the historical prices for this ticker
        tickerDf = tickerData.history(start=fecha_usuario_str, end=fecha_actual_str)
        
        st.dataframe(tickerDf)
        info = tickerData.info
        # Dividend Yield
        dividend_yield = info.get("dividendYield", np.nan)

        st.write(dividend_yield)

if __name__ == '__main__':
    main()