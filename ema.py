"""
EMA管理計算クラス:
    EMA = 現在価格*α + 前EMA*(1-α)
    α = weight/(interval+1)

forで価格を一つずつupdateする時に使う。
"""


class EMA:
    def __init__(self, interval=7, max_length=7, weight=2):
        """
        emaを計算して保持するクラス。

        Args:
            interval (int, optional): 分母。何足分。 Defaults to 7.
            max_length (int, optional): 保持数. Defaults to 7.
            weight (int, optional): ウェイト. Defaults to 2.

        Raises:
            ValueError: intervalがmax_lengthより大きい場合エラー
        """
        if interval > max_length:
            raise ValueError("interval must be shorter than max_length")

        self.prices = []                  # 初回計算用に価格を保持
        self.avg = []                     # ここにemaが入る
        self.interval = interval
        self.max_length = max_length
        self.alpha = weight / (interval + 1)

    def update(self, current):
        """
        更新関数

        Args:
            current (Number): 現在価格
        """
        if len(self.avg) > 0:
            # 初回以降
            self.updateEma(current)
            self.shift()

        else:
            # 初回計算。価格をセットし、所定の長さになったら単純平均をセット。
            # 以降はpricesは使わないので空に。
            self.prices.append(current)
            if len(self.prices) == self.interval:
                mva = sum(self.prices)/self.interval
                self.avg.append(mva)
                self.prices = []

    def updateEma(self, v):
        """
        ema計算

        Args:
            v (Number): 現在価格
        """
        last = self.last
        if last is None:
            return
        ema = v * self.alpha + last * (1-self.alpha)
        self.avg.append(ema)

    def shift(self):
        """
        avgがmax_lengthを超えたら余分を落とす
        """
        i = len(self.avg) - self.max_length
        if i > 0:
            self.avg = self.avg[i:]

    @property
    def last(self):
        """
        直近価格を取得
        Returns:
            Number: 直近価格
        """
        if len(self.avg) == 0:
            return None
        return self.avg[-1]


if __name__ == "__main__":
    test = [
        5,
        7,
        4,
        10,
        5,
        8,
        5,
        12,
        15,
        3,
        6,
        8,
        9,
        14,
        9,
        11
    ]
    ema = EMA(interval=5, max_length=5)
    for i, v in enumerate(test):
        ema.update(v)
        print(
            f"i:{i} v:{v} ema:{ema.last} l:{len(ema.avg)}"
        )
