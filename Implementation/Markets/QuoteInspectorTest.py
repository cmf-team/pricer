from datetime import date
from unittest import TestCase
from unittest.mock import Mock

from Markets.QuoteInspector import QuoteInspector
from Products.QuoteProvider import QuoteProvider


class QuoteInspectorTest(TestCase):

    def setUp(self) -> None:
        self.__sampleQuoteProvider = Mock(spec=QuoteProvider)
        self.__testedQuoteInspector = QuoteInspector(
            self.__sampleQuoteProvider
        )

    def testWrongExportDirectory(self):
        self.assertRaises(
            ValueError,
            self.__testedQuoteInspector.exportQuotes,
            ["GAZP"],
            date(2022, 1, 1),
            date(2022, 1, 1),
            "NonExistingPath"
        )

    def testWrongExportFileExtension(self):
        self.assertRaises(
            ValueError,
            self.__testedQuoteInspector.exportQuotes,
            ["GAZP"],
            date(2022, 1, 1),
            date(2022, 1, 1),
            __file__
        )
