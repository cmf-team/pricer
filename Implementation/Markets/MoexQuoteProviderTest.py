from Markets.MoexQuoteProvider import MoexQuoteProvider
from typing import List
import requests
import apimoex
import pandas as pd
from datetime import date
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# simple test for getQuotes method
sampleQuoteObj = MoexQuoteProvider('TQBR')
sampleDates = [date(2022, 1, 9), date(2022, 2, 10), date(2022, 10, 3),
    date(2022, 10, 10)]

samplePrices = sampleQuoteObj.getQuotes('GAZP', sampleDates)
for i in range(0, len(sampleDates)):
    print(sampleDates[i], samplePrices[i])

# simple test for getQuotes method
sampleChartObj=MoexQuoteProvider('TQBR')
sampleQuoteObj.getChart('OZON',date(2022,1,1),date(2022,10,10))
sampleQuoteObj.getChart('MOEX',date(2022,1,1),date(2022,10,10))