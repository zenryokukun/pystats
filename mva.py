"""
MVA:移動平均線修正版　listの後ろに挿入するようにした
"""


class MVA:
    def __init__(self, interval=7, max_length=7):
        """初期化
        Args:
                interval (int, optional):何足分の平均にするか. Defaults to 7.
                max_length (int, optional):最大何個分のデータを保持するか. Defaults to 7.
        Raises:
                ValueError:interval > max_lengthでエラー
        """
        # param check
        if interval > max_length:
            raise ValueError("interval must be shorter than max_length")

        self.prices = []
        self.avg = []
        self.interval = interval
        self.max_length = max_length

    def update(self, current):
        """移動平均線更新処理
                新しい価格をpricesに挿入し過去interval分の移動平均を計算、mvaに挿入。
                prices,mvaの長さがmax_lengthを超えたら、古いデータを超えた分削除
        Args:
                current(Number): 新しい価格
        """
        self.prices.append(current)
        itv = self.interval

        if len(self.prices) >= itv:
            mva = sum(self.prices[-itv:]) / itv
            self.avg.append(mva)
            self.shift_prices()
            self.shift_avg()

    def shift_prices(self):
        """
        pricesがmax_lengthを超えたら余分を削除
        """
        i = len(self.prices) - self.max_length
        if i > 0:
            self.prices = self.prices[i:]

    def shift_avg(self):
        """
        avgがmax_lengthを超えたら余分を削除
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
    test = [i for i in range(100)]
    # mva_old = _MVA()
    mva_new = MVA(14, 14)
    for i, v in enumerate(test):
        # mva_old.update(v)
        mva_new.update(v)
        # print(f"old mva:{mva_old.mva}")
        print(
            f"i: {i} mva: {mva_new.last} lenP: {len(mva_new.prices)} \
            lenA: {len(mva_new.avg)}"
        )

    print(mva_new.last)
