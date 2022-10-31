from unittest import TestCase

import requests

sampleQuoteData = pandas.DataFrame(
    data = {
        date(2022,10,18): 7.6924, 
        date(2022,10,16): None, #weekend
        date(2022,10,14): 7.6367, 
        date(2022,10,12): 7.7208
    },
    index=[
            0.25 #tenor = 'MOEXGCURVE3M'
            ]
)

class ApiMoexGCurveTest(TestCase):

    def testRatesFeed(self, tenor=sampleQuoteData.index.values, observationDates=sampleQuoteData.columns.tolist()):
        
        expectedResponse = sampleQuoteData.values.tolist()[0]
        serviceResponse = []
        
        for observationDate in observationDates:
            data = requests.get(
                        "https://iss.moex.com/iss/engines/stock/zcyc/"
                        +".json"
                        +"?iss.only=yearyields&iss.meta=off&yearyoelds.columns=period,%20value&date="
                        + str(observationDate)
                ).json()
            data = pandas.DataFrame(
                        data['yearyields']['data'],
                        columns = data['yearyields']['columns'])

            if not data.empty:
                serviceResponse.append(data.loc[data['period'] == 0.25]['value'].values[0])
            else:
                serviceResponse.append(None)

        with self.subTest(tenor=sampleQuoteData.index.values, observationDates=sampleQuoteData.columns.tolist()):
            self.assertEqual(expectedResponse, serviceResponse)
