#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import pandas as pd
import talib
import logging

logger = logging.getLogger(__name__)

class RiskManager:
    """
    ATR計算、ロットサイズ計算、ストップロス／テイクプロフィット設定のモジュール。
    DataFrameは 'high', 'low', 'close' カラムを持つことを前提とする。
    """
    def __init__(self, data: pd.DataFrame, atr_period: int = 14):
        self.data = data
        self.atr_series = talib.ATR(self.data['high'], self.data['low'], self.data['close'], timeperiod=atr_period)
        self.atr_series = self.atr_series.fillna(method='bfill')

    def get_latest_atr(self) -> float:
        atr_value = self.atr_series.iloc[-1]
        logger.info("最新ATR: %.4f", atr_value)
        return atr_value

    def calculate_lot_size(self, account_balance: float, risk_ratio: float, stop_distance: float) -> float:
        if stop_distance <= 0:
            logger.error("stop_distance が0以下です")
            return 0.0
        lot = math.floor((account_balance * risk_ratio) / stop_distance * 100) / 100
        logger.info("計算されたロットサイズ: %.2f", lot)
        return lot

    def set_stop_levels(self, entry_price: float, atr_value: float, stop_multiplier: float, tp_multiplier: float) -> (float, float):
        stop_loss = entry_price - (atr_value * stop_multiplier)
        take_profit = entry_price + (atr_value * tp_multiplier)
        logger.info("エントリー: %.2f, ストップロス: %.2f, テイクプロフィット: %.2f", entry_price, stop_loss, take_profit)
        return stop_loss, take_profit
