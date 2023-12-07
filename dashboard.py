import streamlit as st 
import pandas as pd
import plotly.express as px 

df = pd.read_csv('supermarket_sales.csv', sep=';', decimal=',')