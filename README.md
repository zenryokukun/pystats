# Simple python statistic module

## Available modules
- mva.MVA:  simple moving average
- ema.EMA:  exponential moving average
- rsi.RSI:  relative strength index
- macd.MACD: moving average convergence divergence
- bollinger.Bollinger: bollinger band
- extrema.search: local max/min search

## Basic Usage
- MVA
> from pystats.mva import MVA  
> mva = MVA()  
> for price in range(20):  
>   mva.update(price)  

EMA,RSI,MACD,Bollinger can be used in same manner. 

