
# google-calendar-notifier
Google Calendar のイベント通知をデスクトップに表示するアプリです。Linux向けの通知アプリが見当たらなかったので自分用に作ったものですが、一応公開しておきます。多分Windowsでも動くと思います。

イベントの通知時刻がくると、タイトルを表示するウィンドウがデスクトップの右下から右上に向かって1秒程でスライドします( __マルチモニタ環境では、通知時点でマウスカーソルが存在するモニタのデスクトップに通知が現れます__ ので見逃す心配はありません)。確認したら「完了」ボタンを押せばウィンドウが消えます。再通知機能も用意しており、最大で5分後に再び通知させることもできます。

5分おきにサーバーに接続して新しいイベントを確認しています。よって __登録から5分以内に発動するように作られた病的なイベントは取りこぼす可能性が大__ ですのでご注意ください。

![通知画面のスクリーンショット](https://github.com/motchy869/Google-Calendar-notifier/blob/master/ss_notif.png "通知画面のスクリーンショット")

# 使い方
## Python環境の準備
Python3以上を用意してください。Anacondaがおすすめです。

## Qtの準備
GUIライブラリにQtを用いています。下のページからQtをダウンロードしてインストールしてください。
https://www.qt.io/download
オープンソース版で十分です。

## Python用ライブラリの準備
次のライブラリが必要です。`pip` でインストールしてください。
* setproctitle
* pyQt5
* google-api-python-client (参考: https://developers.google.com/google-apps/calendar/quickstart/python)

## Google Calendar API の有効化
下のページを参考にしてGoogle Calendar APIを有効化し、
https://developers.google.com/google-apps/calendar/quickstart/python
クライアント情報ファイル`client_secret.json` をダウンロードして本プログラムのメインスクリプト`google-calendar-notifier.py` と同じフォルダに置いてください。

## 起動
`google-calendar-notifier.py` に実行権限を付与してターミナルから呼び出します。
システム起動時に自動起動するように設定しておくと便利です。

## 終了方法
次のようにしてPIDを見つけてkillします。
``kill `pidof google-calendar-notifier`　``

# ライセンス
このプログラムをMITライセンスで公開します。  
(c) 2018 Motoki Kamimura  
Released under the MIT license  
http://opensource.org/licenses/mit-license.php
