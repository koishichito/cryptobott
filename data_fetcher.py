#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ccxt
import pandas as pd
import numpy as np
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class DataFetcher:
    """
    KuCoin などの取引所 API を利用して、市場データ（OHLCV）および板情報を取得するモジュール。
    CCXT を利用して実際のデータ取得を行います。
    """
    def __init__(self, exchange_id='kucoin', api_key=None, secret=None, password=None):
        self.exchange = getattr(ccxt, exchange_id)({
            'apiKey': api_key,      # YOUR_KUCOIN_API_KEY
            'secret': secret,       # YOUR_KUCOIN_SECRET
            'password': password,   # YOUR_KUCOIN_PASSWORD (必要な場合)
            'enableRateLimit': True,
        })

    def get_ohlcv(self, symbol='BTC/USDT', timeframe='1h', limit=200) -> pd.DataFrame:
        """
        指定シンボルの OHLCV データを取得し、DataFrame 形式で返す。
        """
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
            logger.info("OHLCV データ取得成功")
            return df
        except Exception as e:
            logger.error("OHLCV データ取得エラー: %s", e)
            return pd.DataFrame()

    def get_order_book(self, symbol='BTC/USDT') -> dict:
        """
        指定シンボルの注文板情報を取得する。
        """
        try:
            order_book = self.exchange.fetch_order_book(symbol)
            logger.info("注文板情報取得成功")
            return order_book
        except Exception as e:
            logger.error("注文板情報取得エラー: %s", e)
            return {}
