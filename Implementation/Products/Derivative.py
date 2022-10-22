from abc import ABC, abstractmethod
from datetime import date

from Products.PriceableElement import PriceableElement
from Products.Pricer import Pricer
from Products.PricerFactory import PricerFactory
from Products.QuoteProvider import QuoteProvider


class Derivative(PriceableElement, ABC):
    pricerCreator = None

    def getPrice(self, valuationDate: date, market: QuoteProvider) -> float:
        pass

    @abstractmethod
    def getBasePrice(self, valuationDate: date, pricer: Pricer) -> float:
        pass

    @staticmethod
    def setPricerCreator(newPricerCreator: PricerFactory):
        Derivative.pricerCreator = newPricerCreator
