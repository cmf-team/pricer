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
        print(expectedResponse)
        serviceResponse = []
        for observationDate in observationDates:
            print(observationDate)
            data = requests.get(
                        "https://iss.moex.com/iss/engines/stock/zcyc/"
                        +".json"
                        +"?iss.only=yearyields&iss.meta=off&yearyoelds.columns=period,%20value&date="
                        + str(observationDate)
                ).json()
            print(data)
            data = pandas.DataFrame(
                        data['yearyields']['data'],
                        columns = data['yearyields']['columns'])
            print(data)
            print(tenor)
            if not data.empty:
                print(data.loc[data['period'] == 0.25]['value'].values[0])
                serviceResponse.append(data.loc[data['period'] == 0.25]['value'].values[0])
            else:
                serviceResponse.append(None)
            print(serviceResponse)
        print(sampleQuoteData.values.tolist(), serviceResponse)
        with self.subTest(tenor=sampleQuoteData.index.values, observationDates=sampleQuoteData.columns.tolist()):
            self.assertEqual(expectedResponse, serviceResponse)