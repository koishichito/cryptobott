#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid
import time
import logging
from web3 import Web3
from web3.exceptions import TransactionNotFound
from flashbots import flashbot

logger = logging.getLogger(__name__)

class OrderExecutor:
    """
    基本的な注文生成・送信モジュール（EIP-1559形式）。
    """
    def __init__(self, rpc_url: str, account_address: str, private_key: str):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        if not self.w3.isConnected():
            logger.error("Web3に接続できませんでした")
        self.account = account_address
        self.private_key = private_key

    def generate_order_tx(self, contract, function_name: str, args: list, nonce=None, gas_price=None) -> dict:
        func = getattr(contract.functions, function_name)(*args)
        if nonce is None:
            nonce = self.w3.eth.get_transaction_count(self.account)
        if gas_price is None:
            gas_price = self.w3.toWei('20', 'gwei')
        tx = func.buildTransaction({
            'from': self.account,
            'nonce': nonce,
            'gasPrice': gas_price,
            'gas': 2000000,
        })
        return tx

    def send_transaction(self, tx: dict) -> str:
        signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return tx_hash.hex()

class FlashbotsOrderExecutor(OrderExecutor):
    """
    Flashbots／プライベートTx 経由でバンドル注文を送信するモジュール。
    """
    def __init__(self, rpc_url: str, account_address: str, private_key: str,
                 flashbots_signer_key: str, flashbots_relay: str):
        super().__init__(rpc_url, account_address, private_key)
        self.flashbots_signer = self.w3.eth.account.from_key(flashbots_signer_key)
        flashbot(self.w3, self.flashbots_signer, flashbots_relay)

    def send_order_bundle(self, bundle: list, target_block: int, max_retries: int = 3) -> bool:
        retry = 0
        while retry < max_retries:
            replacement_uuid = str(uuid.uuid4())
            logger.info("Flashbots バンドル送信開始: ターゲットブロック %d, 試行 %d", target_block, retry + 1)
            try:
                result = self.w3.flashbots.send_bundle(
                    bundle,
                    target_block_number=target_block,
                    opts={"replacementUuid": replacement_uuid}
                )
                result.wait()  # ターゲットブロックまで待機
                receipts = result.receipts()
                logger.info("バンドル採用成功: ブロック %s", receipts[0].get('blockNumber', 'N/A'))
                return True
            except TransactionNotFound as e:
                logger.warning("ターゲットブロック %d で未採用: %s", target_block, e)
            except Exception as e:
                logger.error("バンドル送信エラー: %s", e)
            retry += 1
            target_block += 1  # 次ブロックへ再試行
            time.sleep(1)
        logger.error("最大再試行回数に達しました。バンドル送信失敗")
        return False
