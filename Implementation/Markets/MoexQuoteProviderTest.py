from Markets.MoexQuoteProvider import MoexQuoteProvider
from datetime import date

# simple test for getQuotes method
sampleQuoteObject = MoexQuoteProvider('TQBR')
sampleDates = [date(2022, 1, 9), date(2022, 2, 10), date(2022, 10, 3),
    date(2022, 10, 10)]

samplePrices = sampleQuoteObject.getQuotes('GAZP', sampleDates)
for i in range(len(sampleDates)):
    print(sampleDates[i], samplePrices[i], type(samplePrices[i]))
