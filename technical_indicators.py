#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import talib
from scipy.stats import spearmanr

class TechnicalIndicators:
    """
    DataFrame に対して各種テクニカル指標（SMA, RSI, RCI, MACD）を計算するクラス。
    """
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def calculate_SMA(self, period: int) -> pd.Series:
        sma = talib.SMA(self.data['close'], timeperiod=period)
        return sma

    def calculate_RSI(self, period: int) -> pd.Series:
        rsi = talib.RSI(self.data['close'], timeperiod=period)
        return rsi

    def calculate_RCI(self, period: int) -> pd.Series:
        """
        RCI (Rank Correlation Index) の計算。
        ※ RCI = Spearman順位相関係数 * 100
        """
        rci_values = [np.nan] * (period - 1)
        time_ranks = np.arange(period, 0, -1)
        closes = self.data['close'].values
        for i in range(period - 1, len(closes)):
            window = closes[i - period + 1: i + 1]
            correlation, _ = spearmanr(window, time_ranks)
            rci_values.append(correlation * 100)
        return pd.Series(rci_values, index=self.data.index)

    def calculate_MACD(self, fast_period: int = 12, slow_period: int = 26, signal_period: int = 9) -> (pd.Series, pd.Series):
        macd, macd_signal, _ = talib.MACD(self.data['close'], fastperiod=fast_period,
                                            slowperiod=slow_period, signalperiod=signal_period)
        return pd.Series(macd, index=self.data.index), pd.Series(macd_signal, index=self.data.index)
