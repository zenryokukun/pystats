"""
MACD
short 短期ema 12が一般的
long 長期ema 26が一般的
signal macdの移動平均。nを9にするのが一般的
"""
from .ema import EMA


class MACD:
    def __init__(self,
                 short_itv=12, short_ml=20, short_w=2,
                 long_itv=26, long_ml=30, long_w=2,
                 signal_itv=9):
        self.short = EMA(short_itv, short_ml, short_w)
        self.long = EMA(long_itv, long_ml, long_w)
        self.macd = []
        self.signal = []
        self.interval = signal_itv

    def update(self, current):
        self.short.update(current)
        self.long.update(current)
        self.update_macd()
        self.update_signal()
        self.shift()

    def update_macd(self):
        if self.short.last is None or self.long.last is None:
            return
        macd = self.short.last - self.long.last
        self.macd.append(macd)

    def update_signal(self):
        i = len(self.macd) - self.interval
        if i < 0:
            return
        targ = self.macd[i:]
        sig = sum(targ)/self.interval
        self.signal.append(sig)

    def shift(self):
        i = len(self.macd) - self.long.max_length
        if i > 0:
            self.macd = self.macd[i:]

        j = len(self.signal) - self.long.max_length
        if j > 0:
            self.signal = self.signal[j:]

    @property
    def last(self):
        if len(self.macd) == 0:
            return None
        return self.macd[-1]

    @property
    def last_signal(self):
        if len(self.signal) == 0:
            return None
        return self.signal[-1]


if __name__ == "__main__":

    test = [
        101,
        109,
        102,
        118,
        120,
        105,
        104,
        115,
        104,
        115,
        115,
        112,
        114,
        100,
        103,
        116,
        117,
        103,
        120,
        104,
        110,
        109,
        116,
        104,
        103,
        119,
        111,
        102,
        105,
        118,
        113,
        115,
        118,
        116,
        110,
        116,
        118,
        108,
        105,
        104,
        113,
        105,
        118,
        112,
        114,
        107,
        115,
        101,
        112,
        113,
        115,
        120,
        110,
        102,
        105,
        106,
        113,
        116,
        105,
        102,
        108,
        107
    ]

    macd = MACD()
    for i, v in enumerate(test):
        macd.update(v)
        print(
            f"i: {i}, v: {v}: macd: {macd.last},\
            sig: {macd.last_signal},\
            lmacd: {len(macd.macd)},\
            lsig: {len(macd.signal)}"
        )
