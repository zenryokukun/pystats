"""
 extrema API
 search:
    param:[x:list,y:list,df:dataframe,ratio:float]
    ret[(list,list)]
 show:
    TEST function.
    param:[times:list,prices:list,peaks;list,bottoms:list]
    ret:[None]
"""

import matplotlib.pyplot as plt


class Extrema:
    def __init__(self):
        """
        高値と底値情報。val(float | int)は価格、time(int)は配列のindexを想定。
        timeの型は他でも良いが、数字であることを想定。
        """
        self.val = []
        self.time = []

    def add(self, val, utime):
        """
        価格と時間を追加する。
        Args:
            val (float | int):価格
            utime (any): 時間。配列のindexを想定
        """
        self.val.append(val)
        self.time.append(utime)

    def last_inf(self, now_time_index):
        """
        直近のtimeとval、time_indexと直近のtimeの差を返す
        timeには何らかの配列のindexが入っている必要がある。

        Args:
            now_time_index (int): 現在の時間をindex表記したものを想定

        Returns:
            int,Number,int: 直近time、直近val,now_time_indexとの差
        """

        last_t, last_v = self.last

        if last_t is None:
            return last_t, last_v, None

        diff_t = now_time_index - last_t
        return last_t, last_v, diff_t

    @property
    def last(self):
        """
        直近のtime,valを返す。いずれかが空の場合はNoneを返す

        Returns:
            tuple(int|None,Number|None): 直近のtime,val
        """
        if len(self.val) == 0 or len(self.time) == 0:
            return None, None
        return self.time[-1], self.val[-1]


def search(x, y, ratio):
    """
    x,yから全ての極値を探索する処理

    Args:
        x (list(any)): 時間の配列。unix timestampを想定だが、他の型でも動く
        y (list(int | float)): 価格の配列
        ratio (float): 極値を確定させる折り返しの割合

    Returns:
        tuple(Extrema,Extrema): 高値情報,底値情報
    """
    asc = True  # True->高値探索 False->底値探索
    i = 0  # yのindexを入れる変数
    # 制御用。高値で見つからない（1)、底値検索しても見つからない（2)ならbreakするため
    ctrl = 0
    maxima = Extrema()
    minima = Extrema()

    while i < len(y):
        step = search_local(y, i, ratio, asc)
        if step == 0 or step == -1:
            # 見つからない場合、制御用変数を更新
            ctrl += 1
            if ctrl == 2:
                break
        else:
            # 見つかった場合
            i += step  # 極値のindexを設定
            if i < len(y):
                targ = maxima if asc else minima
                targ.add(y[i], x[i])
            ctrl = 0
        asc = not asc

    return maxima, minima


def search_local(y, start, ratio, asc):
    """
    start以降のyから、一案最初の極値を返す処理

    Args:
        y (list(int | float)): 価格の配列
        ratio (float): 極値を確定させる折り返しの割合
        start (int): 開始するindex
        asc (bool): True->高値探索 False->底値探索

    Returns:
        int: 極値のindex（startからのオフセット）。極値が無い場合は-1。
    """
    local = y[start]  # 極値を入れる変数を初期化
    pos = 0  # 極値を示す添え字。startからのオフセット。
    for i, v in enumerate(y[start:]):
        if (asc and v >= local) or ((not asc) and v <= local):
            # 最大値　or 最小値を更新した場合、localとposを更新
            local = v
            pos = i
        else:
            if is_extrema(local, v, ratio, asc):
                return pos
    return -1


def is_extrema(check, current, ratio, asc):
    """
    極値か判定する関数

    Args:
        check (int | float): 極値か判定する値
        current (_type_): 現在価格
        ratio (float): 極値を確定させる折り返しの割合
        asc (bool): True->高値探索 False->底値探索

    Returns:
        bool : 極値ならTrue、極値でないならFalse
    """
    if asc:
        return (check-current)/check >= ratio
    else:
        return (current-check)/check >= ratio


def show(times, prices, peaks, bottoms, save=False):
    """
    価格と高値、底値をグラフ表示する関数

    Args:
        times (list(any)): 時間の配列
        prices (int | float): 価格の配列
        peaks (Extrema): 高値
        bottoms (Extrema): 底値
        save (bool, optional): Falseならグラフ、Trueなら画像として保存
    """
    fig = plt.figure()
    ax = fig.add_subplot(111)

    # 価格と時間
    ax.plot(times, prices)

    # 山と時間
    ptime = peaks.time
    pprice = peaks.val

    # 谷と時間
    btime = bottoms.time
    bprice = bottoms.val

    # test start
    # for val in pprice:
    # ax.plot(times,[val for i in range(len(times))],color="grey")
    # for val in bprice:
    #   ax.plot(times, [val for i in range(len(times))], color="purple")
    # test end

    ax.scatter(ptime, pprice, color="red")
    ax.scatter(btime, bprice, color="green")

    # x軸調整
    fig.autofmt_xdate()
    # グリッド表示
    plt.grid(True)
    if save:
        plt.savefig("extrema")
    else:
        plt.show()


if __name__ == "__main__":
    import json
    with open("4h15000.json") as f:
        data = json.load(f)
        data["index"] = [i for i in range(len(data["time"]))]
    start = 14990
    x = data["index"][start:]
    y = data["c"][start:]
    mx, mn = search(x, y, 0.003)
    t, v, d = mx.last_inf(15000)
    print(t, v, d)
    show(x, y, mx, mn)
