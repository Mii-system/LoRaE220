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
- - ラズパイの場合アンテナがLAN/USB と同じ向きになります
- - reTerminal の場合，アンテナが上向きになります
- E220は9600bps 8N1 がデフォルトとなります
- ラズベリーパイのUART はttyS0 / ttyAMA0 など実機に合わせてください

!<img src="https://github.com/Mii-system/LoRaE220/assets/69335570/a51b8dbf-641a-4a19-b0ad-3cff682e09f0" width="320p">

## 故障かなと思ったら
### 受信できない
- 送信側と受信側のLoRa 設定を同じにする必要があります
- Sample ソフトのアドレスは0x027F としています
- ch / Adr / LoRa PowはDippSWにより設定していますので親機子機の設定を同じにしてください
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

# Dipp-SW Exsample
!<img src="https://github.com/Mii-system/LoRaE220/assets/69335570/3efbd05f-0b5c-4cc4-96c8-cd955a760529" width="320p">

- Sample プログラムのDipp-SW 設定例です
- POW : LoRa 通信速度です，High/Middle/Low/Extra Low Speed.の略で速いほど応答が良いが距離は短くなります
- ADR : LoRa アドレスです，アプリ固有の使い方を推奨，サンプルは0x02xx (00/01/7F) を使用
- TIME: 子機の送信周期です，(1/5/10/60 [min]) としています，バッテリー寿命に影響します
- CH  : LoRa 通信チャンネルです，0-7を使用し他機器と重ならない事を推奨
