# Simple python statistic module

## Available modules
- ***MVA***      :  simple moving average
- ***EMA***      :  exponential moving average
- ***RSI***      :  relative strength index
- ***MACD***     : moving average convergence divergence
- ***Bollinger***: bollinger band
- ***search***   : local max/min search

## Basic Usage
- MVA,EMA,RSI,MACD,Bollinger
```python
import random
from pystats import MVA,EMA,RSI,MACD,Bollinger

mva = MVA()
ema = EMA()
rsi = RSI()
macd = MACD()
bol = Bollinger()

test_prices = [random.randint(100,120) for i in range(50)]

for price in test_prices:
    mva.update(price)
    ema.update(price)
    rsi.update(price)
    macd.update(price)
    bol.update(price)
    
# calculated results.
print(mva.avg)
print(ema.avg)
print(rsi.rsi)
print(macd.macd,macd.signal)
print(bol.std)
```

- search
```python
import random
from pystats import search

# x and y must be same length.
x = [i for i in range(50)]
y = [random.randint(100,120) for i in range(50)]

# search local maxs and local mins
local_max,local_min = search(x,y,0.007)

#local_max and local_min has 'val' and 'time' attributes.
print(local_max.val)
print(local_max.time)
print(local_min.val)
print(local_min.time)
```


