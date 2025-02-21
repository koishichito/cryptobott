#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd

def aggregate_signals(indicators: dict) -> dict:
    """
    複数のテクニカル指標からシグナルを集約する。
    例：直近2本のSMAの上昇とRSIが30以下なら "BUY"、SMAの下降かつRSIが70以上なら "SELL"、それ以外は "HOLD"
    indicators: {'sma': Series, 'rsi': Series, 'close': Series}
    """
    signal = {}
    sma = indicators.get('sma')
    rsi = indicators.get('rsi')
    close = indicators.get('close')
    if sma is None or rsi is None or close is None:
        signal['action'] = 'HOLD'
        return signal

    if sma.iloc[-2] < sma.iloc[-1] and rsi.iloc[-1] < 30:
        signal['action'] = 'BUY'
        signal['price'] = close.iloc[-1]
    elif sma.iloc[-2] > sma.iloc[-1] and rsi.iloc[-1] > 70:
        signal['action'] = 'SELL'
        signal['price'] = close.iloc[-1]
    else:
        signal['action'] = 'HOLD'
    return signal
