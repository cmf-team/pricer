import Pricer


class Autocall():

    def __init__(
        self,
        notional,
        percent: int,
        underlyingAssets,
        ab: float,
        cb: float
    ):
        """
        Initialize auto-call pricer


        :param notional: ???
        :param percent: ???
        :param underlyingAssets: underlying assets in current portfolio,\n
        where in underlyingAssets[j][i] j is for underlying, `i` is for time\n
        from t_0, ..., t_i,..., t_n
        :param ab: ???
        :param cb: ???
        """
        self.notional = notional
        self.percent = percent
        self.underlyingAssets = underlyingAssets
        self.ab = ab
        self.cb = cb
        self.normalizedUnderlyingAssets = [
            [0] * len(self.underlyingAssets[0]) for i in range(
                len(self.underlyingAssets)
            )
        ]

        for j in range(0, len(self.underlyingAssets)):
            for i in range(0, len(self.underlyingAssets[j])):
                self.normalizedUnderlyingAssets[j][i] = \
                    self.underlyingAssets[j][i] / self.underlyingAssets[j][0]

    def coupon(self, i: int):
        """
        Returns value of coupon

        :param i: ith time index
        :return: value of coupon at time moment t_i
        """
        tempMin = self.normalizedUnderlyingAssets[0][i]
        tempMax = self.normalizedUnderlyingAssets[0][0]

        for j in range(1, len(self.normalizedUnderlyingAssets)):
            if self.normalizedUnderlyingAssets[j][i] < tempMin:
                tempMin = self.normalizedUnderlyingAssets[j][i]

        for j in range(0, len(self.normalizedUnderlyingAssets)):
            for k in range(0, i):
                if self.normalizedUnderlyingAssets[j][k] > tempMax:
                    tempMax = self.normalizedUnderlyingAssets[j][k]

        print(self.normalizedUnderlyingAssets)
        print(tempMin, tempMax)

        if tempMin >= self.cb and tempMax <= self.ab:
            return self.notional * self.percent / 100
        else:
            return 0

    def redemption(self):
        """
        ???

        :return: ???
        """
        tempMin = self.normalizedUnderlyingAssets[0][-1]
        tempMax = self.normalizedUnderlyingAssets[0][0]

        for j in range(1, len(self.normalizedUnderlyingAssets)):
            if self.normalizedUnderlyingAssets[j][-1] < tempMin:
                tempMin = self.normalizedUnderlyingAssets[j][-1]

        for j in range(0, len(self.normalizedUnderlyingAssets)):
            for k in range(0, len(self.normalizedUnderlyingAssets[0]) - 1):
                if self.normalizedUnderlyingAssets[j][k] > tempMax:
                    tempMax = self.normalizedUnderlyingAssets[j][k]

        print(tempMin, tempMax)

        if tempMin >= self.cb and tempMax <= self.ab:
            return self.notional
        else:
            return 0


if __name__ == '__main__':
    pricer = PricerAutocall(
        1,
        10,
        [[1, 1.1, 0.9, 0.95], [0.5, 0.5, 0.5, 0.5], [1.0, 1.3, 1.5, 1.6],
            [1.0, 0.8, 0.7, 0.8]],
        1.5,
        0.65
    )
    print(pricer.coupon(2))
    print(pricer.redemption())
