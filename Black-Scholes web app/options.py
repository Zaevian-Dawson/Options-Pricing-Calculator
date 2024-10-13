import streamlit as st 
import math 
import numpy as np
from scipy.stats import norm 

st.set_page_config(page_title = "Options Pricing Calculator") 
st.title("Options Pricing Calculator")
st.header("Black-Scholes and Bachelier Options Pricing Models") 

#setting the background colour to light blue using CSS 
st.markdown(
    """
    <style>
    .main {
        background-color: #ADD8E6;  /*light blue colour*/ 
    }
    /*style for input fields */
    .stTextInput div[data-baseweb="input"] {
        width: 65px !important; /*adjusting the width*/ 
    } 
    </style>
    """,
    unsafe_allow_html=True
)

#getting user input 
st.write("Enter the values of the following parameters:")
stock_price = st.number_input("stock price ($): ", min_value=0.0, value=0.0) 
exercise_price = st.number_input("exercise price ($): ", min_value=0.0, value=0.0) 
time = st.number_input("time to expiration (days): ", min_value=0.0, value=0.0) 
time_val = time/365 
volatility = st.number_input("volatility (%): ", min_value=0.0, value=0.0)
volatility_val = volatility/100 
interest_rate = st.number_input("interest rate (%): ", min_value=0.0, value=0.0) 
interest_rate_val = interest_rate/100 

#Black-Scholes model implementation 
#calculating d1 and d2 
def d1_bs(): 
    if stock_price > 0 and exercise_price > 0:
        numerator = math.log((stock_price/exercise_price)) + ((interest_rate_val + 0.5*(volatility_val**2))*time_val)
        denominator = volatility_val*(math.sqrt(time_val))
        if denominator != 0:
            d1_val = numerator/denominator 
            return d1_val
        return None 

def d2_bs(d1): 
    d2_val = d1 - volatility_val*(math.sqrt(time_val)) 
    return d2_val 

#Black-Scholes call option 
def calculate_call_BS(): 
    d1 = d1_bs()
    d2 = d2_bs(d1) 
    call_price = stock_price*(norm.cdf(d1)) - ((exercise_price)/(math.exp(interest_rate_val*time_val)))*(norm.cdf(d2))
    return call_price 

#Black-Scholes put option 
def calculate_put_BS(): 
    #find the call option price 
    call_option = calculate_call_BS() 
    put_option_price = call_option + ((exercise_price)/(math.exp(interest_rate_val*time_val))) - stock_price 
    return put_option_price 


#Bachelier model implementation 
#Bachelier call option 
def calculate_call_BA(volatility_val, stock_price, exercise_price, interest_rate_val, time_val): 
    #calulating dN 
    dN = ((stock_price*np.exp(interest_rate_val*time_val) - exercise_price)/
    np.sqrt(volatility_val**2/(2*interest_rate_val)*(np.exp(2*interest_rate_val*time_val)-1)))
    
    bach_call = np.exp(-interest_rate_val*time_val)*(stock_price*np.exp(interest_rate_val*time_val) - exercise_price)*(norm.cdf(dN))  + \
    np.exp(-interest_rate_val*time_val)*np.sqrt(volatility_val**2/(2*interest_rate_val)*(np.exp(2*interest_rate_val*time_val)-1))*norm.pdf(dN)
    
    return bach_call 

#Bachelier put option 
def calculate_put_BA(stock_price, exercise_price, interest_rate_val, time_val): 
    call_price = calculate_call_BA(volatility_val*stock_price, stock_price, exercise_price, interest_rate_val, time_val) 
    bach_put = call_price - stock_price + (math.exp(-interest_rate_val*time_val))*exercise_price 
    return bach_put 

#display the buttons for user selection 
st.write("Do you want to calculate the price of a Call or Put option?") 
call_button = st.button("Call Option") 
put_button = st.button("Put Option") 

if call_button: 
    call_price_val = calculate_call_BS() 
    bach_call = calculate_call_BA(volatility_val*stock_price, stock_price, exercise_price, interest_rate_val, time_val) 
    st.write(f"<h3><b>Black-Scholes Call option price is: ${call_price_val:.2f}</b></h3>", unsafe_allow_html=True) 
    st.write(f"<h3><b>Bachelier Call option price is: ${bach_call:.2f}</b></h3>", unsafe_allow_html=True) 

elif put_button: 
    put_price = calculate_put_BS() 
    bach_put = calculate_put_BA(stock_price, exercise_price, interest_rate_val, time_val) 
    st.write(f"<h3><b>Black-Scholes Put option price is: ${put_price:.2f}</b></h3>", unsafe_allow_html=True) 
    st.write(f"<h3><b>Bachelier Put option price is: ${bach_put:.2f}</b></h3>", unsafe_allow_html=True) 

