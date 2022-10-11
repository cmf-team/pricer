from Markets.MoexQuoteProvider import MoexQuoteProvider
from datetime import date

# simple test for getQuotes method
sampleQuoteObj = MoexQuoteProvider('TQBR')
sampleDates = [date(2022, 1, 9), date(2022, 2, 10), date(2022, 10, 3),
    date(2022, 10, 10)]

samplePrices = sampleQuoteObj.getQuotes('GAZP', sampleDates)
for i in range(0, len(sampleDates)):
    print(sampleDates[i], samplePrices[i])

# simple test for getChart method
sampleChartObj=MoexQuoteProvider('TQBR')
sampleQuoteObj.getChart('GAZP',date(2022,1,1),date(2022,10,10))
sampleQuoteObj.getChart('SBER',date(2022,1,1),date(2022,10,10))