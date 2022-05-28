"""
Simple python statistic package.
Python version of https://github.com/zenryokukun/dataprocess

###################################
APIs
###################################
mva.MVA
ema.EMA
bollinger.Bollinger
rsi.RSI
macd.MACD
extrema.search
"""
from .mva import MVA
from .ema import EMA
from .rsi import RSI
from .macd import MACD
from .bollinger import Bollinger
from .extrema import search

__all__ = ["MVA", "EMA", "RSI", "MACD", "Bollinger", "search"]
