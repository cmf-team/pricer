import requests
import pandas
from datetime import date, timedelta
from typing import List

from Products.QuoteProvider import QuoteProvider

class MoexGCurveQuoteProvider(QuoteProvider):
    def __init__(self) -> None:
        self.gcurve=pandas.DataFrame(index=[
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
        pass

    def getQuotes(self, ticker: str, observationDates: List[date]) -> List[float]:

        quotes=[]
        
        for observationDate in observationDates:
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

            if not data.empty:
                self.gcurve[observationDate]=data['value'].values
            else:
                self.gcurve[observationDate]=None

            quotes.append(self.gcurve.loc[ticker, observationDate])
        
        return quotes
