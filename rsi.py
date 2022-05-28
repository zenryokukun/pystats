"""
RSI 計算
初回はcutler式
A/(A+B)が基本
n -> 日数.基本は14
A -> 上昇分の合計/n
B -> 下落分の合計/n
差分が14個必要となるため、配列の長さとしては15必要。
=>nが14ならば、価格は15必要となる。
"""


class RSI:
    @classmethod
    def cutler(cls, prices, n):
        """
        初回rsi計算用。Cutler式
        Args:
            prices (Number): 価格。n + 1の長さである必要がある。
            n (int): 何足分か

        Returns:
            (Number,Number,Number): rsi,A,B
        """
        plus, minus = 0, 0
        prev = prices[0]
        for v in prices:
            diff = v - prev
            if diff > 0:
                plus += diff
            else:
                minus += diff
            prev = v
        A = plus/n
        B = abs(minus)/n
        rsi = A/(A+B)
        return rsi, A, B

    def __init__(self, n=14, max_length=14):
        """
        初期化

        Args:
            n (int, optional): 何足分. Defaults to 14.
            max_length (int, optional): rsiの保持数. Defaults to 14.
        """
        self.prices = []  # 初回計算用として必要
        self.rsi = []
        self.max_length = max_length
        self.n = n
        self.A = 0
        self.B = 0
        self.last_val = 0

    def update(self, current):
        """
        rsi更新

        Args:
            current (Number): 現在価格
        """
        if len(self.rsi) > 0:
            # 初回以降
            self.updateRsi(current)
            self.shift()
        else:
            # 初回
            self.prices.append(current)
            if len(self.prices) == self.n+1:
                rsi, A, B = self.cutler(self.prices, self.n)
                self.rsi.append(rsi)
                self.A = A
                self.B = B
                self.last_val = current
                self.prices = []  # 初回計算後は使わないので空にする

    def updateRsi(self, current):
        """
        rsi計算

        Args:
            current (Number): 現在価格
        """
        diff = current - self.last_val
        pA = self.A * (self.n - 1)
        pB = self.B * (self.n - 1)

        nA, nB = 0, 0

        if diff > 0:
            nA = (pA + diff) / self.n
            nB = (pB) / self.n
        else:
            nB = (pB + abs(diff)) / self.n
            nA = pA / self.n

        rsi = nA / (nA + nB)
        self.rsi.append(rsi)
        self.A = nA
        self.B = nB
        self.last_val = current

    def shift(self):
        """
        rsiがmax_lengthを超えたら余分を削除
        """
        i = len(self.rsi) - self.max_length
        if i > 0:
            self.rsi = self.rsi[i:]

    @property
    def last(self):
        """
        直近rsiを返す
        Returns:
            Number | None: rsi
        """
        if len(self.rsi) == 0:
            return None
        return self.rsi[-1]


if __name__ == "__main__":
    test = [1000, 1020, 1010, 1030, 1040, 1050, 1080, 1070,
            1050, 1090, 1100, 1120, 1110, 1120, 1100, 1080,
            1080, 1100, 1050, 1060, 1070, 1040, 1100, 1090
            ]
    rsi = RSI(5, 7)

    for i, v in enumerate(test):
        rsi.update(v)
        print(
            f"i:{i},v:{v},rsi:{rsi.last},ml:{len(rsi.rsi)}"
        )
    '''
    test = [1,4,7,6,3,9]
    rsi = RSI(interval=5)
    old = oRSI(interval=5)
    rsi.update(test)
    old.update(test)
    print(rsi.rsi)
    print(old.rsi)
    test = [10,1,4,7,6,3,9]
    ntest = [9,1,3,6,7,4,1,10]
    print(ntest)
    rsi.update(ntest)
    old.update(test)
    print(rsi.rsi)
    print(old.rsi)
    # ret = RSI(test)
    # print(ret)

    test = [
        3692935,
        3696440,
        3696152,
        3705146,
        3701355,
        3705763,
        3702662,
        3704381,
        3713402,
        3710447,
        3713756,
        3703027,
        3702189,
        3712001,
        3692116
    ]

    rsi = RSI(interval=14)
    old = oRSI(interval=14)
    rsi.update(test)
    old.update(test)
    print(rsi.rsi)
    print(old.rsi)
    '''
