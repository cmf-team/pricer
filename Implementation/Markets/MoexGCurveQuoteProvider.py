import requests
import pandas
from datetime import date, timedelta
from typing import List

from Products.QuoteProvider import QuoteProvider

class MoexGCurveQuoteProvider(QuoteProvider):
    def __init__(self) -> None:
      pass

    def getQuotes(self, ticker: str, observationDates: List[date]) -> List[float]:
        gcurve=pandas.DataFrame(index=[
           'MOEXGCURVE3M', 
           'MOEXGCURVE6M',
           'MOEXGCURVE9M',
           'MOEXGCURVE1Y',
           'MOEXGCURVE2Y',
           'MOEXGCURVE3Y',
           'MOEXGCURVE5Y',
           'MOEXGCURVE7Y',
           'MOEXGCURVE10Y',
           'MOEXGCURVE15Y',
           'MOEXGCURVE20Y',
           'MOEXGCURVE30Y'
        ])
        
        for observationDate in observationDates:
            data=pandas.DataFrame()
            perviousDate = 0
            while data.empty:
                url = (
                    "https://iss.moex.com/iss/engines/stock/zcyc/"
                    +".json"
                    +"?iss.only=yearyields&iss.meta=off&yearyoelds.columns=period,%20value&date="
                    + str(observationDate)
                )

                data = requests.get(url).json()
                
                data = pandas.DataFrame(
                    data['yearyields']['data'],
                    columns = data['yearyields']['columns']
                )

                if data.empty:
                    perviousDate += 1
                    observationDate = observationDate - timedelta(1)
            
            observationDate = observationDate + timedelta(perviousDate)           
            gcurve[observationDate]=data['value'].values

        quotes = []
        for observationDate in observationDates:
            quotes.append(gcurve.loc[ticker, observationDate])
        
        return quotes
