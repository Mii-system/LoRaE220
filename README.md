# LoRa E220
 LoRa E220 Sample Soft

# Purpose   概要
- +DOC:Manuals
- - +Circuit.pdf
- +SRC:Sample Sorce & Manuals
- - +Python

# Introduction    導入
- LoRa E220 Manual
- RapberryPi や reTerminal に使用できる拡張基板です
- ディップSWとM0/M1 端子をGPIO から操作できるためプログラムから設定変更し運用ができます
- Port割り付けは回路図を参照してください
- ラズベリーパイのサンプルプログラムを用意してあります

## 注意事項
- ボードの取り付け，取り外しは電源オフ状態で行ってください。
- E220は9600bps 8N1 がデフォルトとなります
- ラズベリーパイのUART はttyS0 / ttyAMA0 など実機に合わせてください

## 故障かなと思ったら
### 受信できない
- 送信側と受信側のLoRa 設定を同じにする必要があります
- Sample ソフトのアドレスは0x027F としています
- chおよびLoRa通信ソフトDippSWによります
- 設定が一致していれば受信時にLEDが点滅します
### Python のエラーが出る
- エラーメッセージを確認してください
- ラズベリーパイのUARTはデフォルトでは利用不可のため設定変更が必要です
- ラズベリーパイ3と4でUARTアドレスが変わる場合があります，ttyS0/ttyAMA0など実機に合わせてください

# Samples
## E220_Sample.py
- LoRa E220 の受信サンプル
- 起動時にDipp-SW の設定によりE220 を初期化
- 受信データをコンソールに表示します
## RANDX-DEMO1.py
- RANDX-C-LoRa から受信するサンプルです
- 起動時にDipp-SW の設定によりE220 を初期化
- 受信した電流データをコンソールに表示します
## RANDX-DEMO2.py
- RANDX-DEMO1.py から受信した電流情報をInfluxDB に保存します
- InfluxDB の設定などはプログラムを参考に取り進めください

<br><br>
