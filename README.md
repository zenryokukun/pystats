# Simple python statistic module

## Available modules
- mva:  simple moving average
- ema:  exponential moving average
- rsi:  relative strength index
- macd: moving average convergence divergence
- bollinger: bollinger band
- extrema: local max/min search

## Basic Usage
"""
from pystats.extrema import search
local_max,local_min = search(some_x,some_y,ratio)
"""
