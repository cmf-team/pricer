import Pricer


class PricerAutocall(Pricer):

    def __init__(
        self,
        notional,
        percent: int,
        underlying_assets,
        ab: float,
        cb: float
    ):
        """
        Initialize auto-call pricer


        :param notional: ???
        :param percent: ???
        :param underlying_assets: underlying assets in current portfolio,\n
        where in underlying_assets[j][i] j is for underlying, `i` is for time\n
        from t_0, ..., t_i,..., t_n
        :param ab: ???
        :param cb: ???
        """
        self.notional = notional
        self.percent = percent
        self.underlying_assets = underlying_assets
        self.ab = ab
        self.cb = cb
        self.normalized_underlying_assets = [
            [0] * len(self.underlying_assets[0]) for i in range(
                len(self.underlying_assets)
            )
        ]

        for j in range(0, len(self.underlying_assets)):
            for i in range(0, len(self.underlying_assets[j])):
                self.normalized_underlying_assets[j][i] = \
                    self.underlying_assets[j][i] / self.underlying_assets[j][0]

    def coupon(self, i: int):
        """
        Returns value of coupon

        :param i: ith time index
        :return: value of coupon at time moment t_i
        """
        temp_min = self.normalized_underlying_assets[0][i]
        temp_max = self.normalized_underlying_assets[0][0]

        for j in range(1, len(self.normalized_underlying_assets)):
            if self.normalized_underlying_assets[j][i] < temp_min:
                temp_min = self.normalized_underlying_assets[j][i]

        for j in range(0, len(self.normalized_underlying_assets)):
            for k in range(0, i):
                if self.normalized_underlying_assets[j][k] > temp_max:
                    temp_max = self.normalized_underlying_assets[j][k]

        print(self.normalized_underlying_assets)
        print(temp_min, temp_max)

        if temp_min >= self.cb and temp_max <= self.ab:
            return self.notional * self.percent / 100
        else:
            return 0

    def redemption(self):
        """
        ???

        :return: ???
        """
        temp_min = self.normalized_underlying_assets[0][-1]
        temp_max = self.normalized_underlying_assets[0][0]

        for j in range(1, len(self.normalized_underlying_assets)):
            if self.normalized_underlying_assets[j][-1] < temp_min:
                temp_min = self.normalized_underlying_assets[j][-1]

        for j in range(0, len(self.normalized_underlying_assets)):
            for k in range(0, len(self.normalized_underlying_assets[0]) - 1):
                if self.normalized_underlying_assets[j][k] > temp_max:
                    temp_max = self.normalized_underlying_assets[j][k]

        print(temp_min, temp_max)

        if temp_min >= self.cb and temp_max <= self.ab:
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
