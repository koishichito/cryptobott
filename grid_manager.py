#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)

class GridManager:
    """
    指定された価格レンジとグリッド数に基づきグリッド注文を生成するモジュール。
    """
    def __init__(self, lower_bound: float, upper_bound: float, grid_count: int):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.grid_count = grid_count

    def generate_grid_levels(self) -> list:
        if self.grid_count <= 1:
            return [self.lower_bound, self.upper_bound]
        interval = (self.upper_bound - self.lower_bound) / (self.grid_count - 1)
        levels = [self.lower_bound + i * interval for i in range(self.grid_count)]
        logger.info("生成されたグリッドレベル: %s", levels)
        return levels

    def generate_grid_orders(self, current_price: float, base_lot: float) -> list:
        levels = self.generate_grid_levels()
        orders = []
        for level in levels:
            if level < current_price:
                orders.append({'side': 'BUY', 'price': level, 'lot': base_lot})
            elif level > current_price:
                orders.append({'side': 'SELL', 'price': level, 'lot': base_lot})
        logger.info("生成されたグリッド注文: %s", orders)
        return orders
