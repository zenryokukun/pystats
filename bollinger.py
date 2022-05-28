"""
Bollinger
20～25が一般的とのこと
"""
import math
from .mva import MVA


class Bollinger:
    def __init__(self, interval=20, max_length=20):
        """
        コンストラクタ
        Args:
            interval (int, optional): 何足分か. Defaults to 20.
            max_length (int, optional): stdを最大何個保持するか. Defaults to 20.
        """
        self.mva = MVA(interval, max_length)
        self.std = []  # std(標準偏差)を格納

    def update(self, current):
        """
        更新関数
        Args:
            current (Number): 現在価格
        """
        self.mva.update(current)
        if len(self.mva.avg) > 0:
            self.update_std(current)
            self.shift()

    def update_std(self, current):
        """
        標準偏差計算関数

        Args:
            current (Number): 現在価格
        """
        itv = self.mva.interval
        prices = self.mva.prices[-itv:]
        mva = self.mva.avg[-1]
        diffsum = 0
        for p in prices:
            sdiff = (p-mva)**2
            diffsum += sdiff

        variance = diffsum / itv
        std = math.sqrt(variance)
        self.std.append(std)

    def shift(self):
        """
        stdの長さがmax_lengthを超えたら余分を切り捨てる
        """
        i = len(self.std) - self.mva.max_length
        if i > 0:
            self.std = self.std[i:]

    @property
    def last(self):
        """
        直近のstdを返す

        Returns:
            Number: std
        """
        if len(self.std) == 0:
            return None
        return self.std[-1]


if __name__ == "__main__":
    test = [5, 9, 1, 1, 4, 5, 8, 11, 70, 5, 3, 16, 7, 3,
            6, 4, 2, 22, 3, 66, 45, 4, 600, 55, 10, -1000,
            9, 100, 20, 25, 40, 25, 6, 50, 53, 40, 66, 90, 49, 10, 66
            ]
    b = Bollinger()
    for i, v in enumerate(test):
        b.update(v)
        print(
            f"i:{i} v:{v} std:{b.last} ml:{len(b.std)}"
        )
    """
    ol = _Bollinger()
    ne = Bollinger()
    # test = [i for i in range(25)]
    test = [5,9,1,1,4,5,8,11,70,5,3,16,7,3,6,4,2,22,3,66,45,4,600,55,10,-1000]
    for v in test:
            ol.update(v)
            ne.update(v)
            # print(f"old {ol.sigmas}")
            # print(f"new {ne.sigmas}")

    print(ol.standardize())
    print(ne.standardize())
    print(ol.standardize(pos=1))
    print(ne.standardize(ilast=2))
    print(ol.standardize(pos=6))
    print(ne.standardize(ilast=7))

    # for i in range(len(ol.sigmas)):
    #    oi = i
    #    ni = i + 1
    #    print("--------------------------------")
    #    print(f"old:{ol.is_over_ndist(pos=oi)}")
    #    print(f"old:{ol.is_over_ndist(pos=oi,under=True)}")
    #    print(f"new:{ne.is_over_ndist(ilast=ni)}")
    #    print(f"new:{ne.is_over_ndist(ilast=ni,under=True)}")


"""
