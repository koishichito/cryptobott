# Crypto Trading Bot

このプロジェクトは、従来のテクニカル指標とグリッド戦略、さらに高速執行および動的リスク管理を組み合わせたルールベースの仮想通貨取引ボットです。  
実際に運用している、botのひな型です。
適宜カスタマイズして応用できるかと。

## ディレクトリ構成


## 主な機能

- **市場データの取得**  
  CCXT を利用して KuCoin 等の取引所から OHLCV や板情報を取得します。

- **テクニカル指標の計算**  
  TA-Lib および scipy を使用し、SMA、RSI、RCI、MACD などを計算。  
  これらをもとに、シンプルなルール（例：SMA クロス＋RSI閾値）でシグナルを生成します。

- **リスク管理**  
  ATR に基づくボラティリティ測定から、口座残高・リスク許容率を用いてロットサイズを動的に計算。  
  エントリー価格からストップロス／テイクプロフィットレベルを設定します。

- **グリッド戦略**  
  指定した価格レンジ内で均等なグリッドレベルを生成し、現在価格を基準として買い／売り注文を生成します。

- **注文執行**  
  Flashbots／プライベートTx を利用し、原子的なバンドル注文を生成および送信。  
  再試行ロジックにより、注文が採用されるまで自動で再送信を試みます。

- **統合メインループ**  
  各モジュールを統合し、データ取得、シグナル生成、リスク管理、グリッド注文、注文執行を連続的に行います。

