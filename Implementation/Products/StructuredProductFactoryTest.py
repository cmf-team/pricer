from datetime import date
from unittest import TestCase
from unittest.mock import patch

from Products.Autocall import Autocall
from Products.StructuredProductFactory import CouponFrequency, \
    StructuredProductFactory


class StructuredProductFactoryTest(TestCase):
    def setUp(self) -> None:
        self.__factoryInput = {
            'underlyings': ['GAZP', 'YNDX'],
            'couponBarrier': 1,
            'autocallBarrier': 1.1,
            'startDate': date(2022, 9, 1),
            'couponFrequency': CouponFrequency.MONTHLY,
            'couponCount': 3,
            'couponRate': 0.1,
            'memoryFeature': False
        }
        self.__autocallInput = {
            'underlyings': ['GAZP', 'YNDX'],
            'couponBarrier': 1,
            'autocallBarrier': 1.1,
            'startDate': date(2022, 9, 1),
            'couponDates': [
                date(2022, 10, 1), date(2022, 11, 1), date(2022, 12, 1)
            ],
            'couponAmounts': [0.1 * 30 / 365, 0.1 * 31 / 365, 0.1 * 30 / 365],
            'memoryFeature': False
        }

    def testCreateAutocallMonthly(self):
        with patch.object(
            Autocall,
            '__init__',
            return_value=None
        ) as mockAutocall:
            StructuredProductFactory.createAutocall(**self.__factoryInput)
            mockAutocall.assert_called_once_with(**self.__autocallInput)

    def testCreateAutocallQuarterly(self):
        with patch.object(
            Autocall,
            '__init__',
            return_value=None
        ) as mockAutocall:
            factoryInput = self.__factoryInput.copy()
            factoryInput['couponFrequency'] = CouponFrequency.QUARTERLY
            factoryInput['couponCount'] = 1

            autocallInput = self.__autocallInput.copy()
            autocallInput['couponDates'] = [date(2022, 12, 1)]
            autocallInput['couponAmounts'] = [0.1 * 91 / 365]

            StructuredProductFactory.createAutocall(**factoryInput)
            mockAutocall.assert_called_once_with(**autocallInput)

    def testExceptions(self):
        with self.assertRaisesRegex(ValueError, 'barrier'):
            barrierCheck = self.__factoryInput.copy()
            barrierCheck['couponBarrier'] = 1.2
            StructuredProductFactory.createAutocall(**barrierCheck)
