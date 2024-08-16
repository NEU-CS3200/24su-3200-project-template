import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from pmdarima import auto_arima


def load_data():
    print("Loading data...")
    data = pd.read_csv('../../app/src/Metro_mlp_uc_sfrcondo_sm_month-v1.csv')
    data['Date'] = pd.to_datetime(data['Date'])
    return data


def predict_future_prices(data, state, months_ahead):
    # Filter and prepare data
    state_data = data[data['StateName'] == state]
    state_data.sort_values('Date', inplace=True)
    prices = state_data['Price'].values

    model = auto_arima(prices, seasonal=True, m=12, suppress_warnings=True)
    
    # Predict future prices
    future_prices = model.predict(n_periods=months_ahead)
    future_dates = pd.date_range(state_data['Date'].max(), periods=months_ahead, freq='M')

    return future_dates, future_prices


def main():
    st.title('Real Estate Price Prediction')
    data = load_data()

    states = data['StateName'].unique()
    selected_state = st.selectbox('Select State', states)

    # Allow users to choose months ahead and show more data options
    months_ahead = st.number_input('How many months ahead would you like to predict?', min_value=1, max_value=36, value=12)
    years_of_data = st.slider('How many years of past data to use?', 1, 5, 3)

    if st.button('Predict Future Prices'):
        # Filter data to include only the selected range of years
        start_date = pd.to_datetime('today') - pd.DateOffset(years=years_of_data)
        filtered_data = data[(data['Date'] >= start_date) & (data['StateName'] == selected_state)]

        if filtered_data['Date'].nunique() > 1:
            future_dates, predicted_prices = predict_future_prices(filtered_data, selected_state, months_ahead)
            st.write(f"Future prices for {selected_state}:")
            results = pd.DataFrame({'Date': future_dates, 'Predicted Price': predicted_prices})
            st.line_chart(results.set_index('Date'))
        else:
            st.error("Not enough data points with unique dates to perform prediction.")

if __name__ == "__main__":
    main()
