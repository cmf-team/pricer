from datetime import date
from typing import List, Optional

from Products.CashFlow import CashFlow
from Products.Derivative import Derivative
from Products.Pricer import Pricer
from Products.QuoteProvider import QuoteProvider


class VanillaStructuredProduct(CashFlow, Derivative):
    def __init__(
        self,
        underlying: str,
        participation: float,
        strike: float,
        maturityDate: date,
        cap: Optional[float] = None
    ):
        self.__underlying = underlying
        self.__participation = participation
        self.__strike = strike
        self.__maturityDate = maturityDate
        self.__cap = cap
        self.__capStrike = None

        if self.__cap is not None:
            self.__capStrike = self.__strike * (
                    1 + self.__cap / self.__participation)

    def getPaymentDates(self) -> List[date]:
        return [self.__maturityDate]

    def getPaymentAmount(
        self,
        paymentDate: date,
        market: QuoteProvider
    ) -> float:
        underlyingQuote = market.getQuotes(self.__underlying, [paymentDate])[0]
        upside = max(underlyingQuote - self.__strike, 0) / self.__strike
        if self.__cap and underlyingQuote >= self.__capStrike:
            return 1 + self.__cap
        else:
            return 1 + self.__participation * upside

    def getBasePrice(self, valuationDate: date, pricer: Pricer) -> float:
        callOptionBasePrice = pricer.getCallOptionBasePrice(
            self.__underlying,
            self.__strike,
            valuationDate
        )
        if self.__cap is not None:
            callCapOptionBasePrice = pricer.getCallOptionBasePrice(
                self.__underlying,
                self.__capStrike,
                valuationDate
            )
            return callOptionBasePrice - callCapOptionBasePrice + 1 * \
                   pricer.getDiscountFactor(self.__maturityDate)
        else:
            return callOptionBasePrice + 1 * pricer.getDiscountFactor(
                self.__maturityDate
            )
