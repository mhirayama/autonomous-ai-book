# Pythonではじめる自律型AIシステム開発入門

本リポジトリは、Python、YOLO、OpenCV、MariaDB、Flask、Raspberry Piを組み合わせて、自律型AIシステムを構築するためのサンプルコードを公開しています。

カメラから取得した映像をAIで解析し、人物の状態を判断します。その結果をデータベースへ保存するとともに、ネットワーク経由でRaspberry Piへ送信し、GPIOを利用してLEDを制御します。

システムは、単純な画像認識だけではなく、

```text
観測
 ↓
認識
 ↓
判断
 ↓
制御
 ↓
環境の変化
 ↓
再び観測
```

というフィードバックループを形成します。

---

## システム構成

システムは、主にUbuntu PCとRaspberry Pi Zero WHから構成されます。

```

【現実環境】
    │
    ↓
【カメラ】
    │
    ↓
【Ubuntu PC】
    │
    ├─ OpenCV
    │
    ├─ YOLO
    │
    ├─ 人物数・座標の取得
    │
    ├─ 状態判断
    │
    ├─ MariaDB
    │
    ├─ Raspberry Piとの通信
    │
    └─ Flask
          │
          ↓
     【Webブラウザ】

【Ubuntu PC】
    │
    │ HTTP通信
    ↓
【Raspberry Pi Zero WH】
    │
    ↓
【GPIO17】
    │
    ↓
【LED】
    │
    ↓
【現実環境】
```
### Ubuntu PC

Ubuntu PCでは、AI処理とシステム全体の管理を行います。

- カメラ映像の取得
    
- OpenCVによる画像処理
    
- YOLOによる人物認識
    
- 人物数の取得
    
- 状態判断
    
- MariaDBへのデータ保存
    
- Raspberry PiとのHTTP通信
    
- FlaskによるWebインターフェース
    

### Raspberry Pi Zero WH

Raspberry Pi Zero WHでは、Ubuntu PCから受信した状態に応じてGPIOを制御します。

今回のシステムでは、GPIO17を利用してLEDを制御します。

```text
empty
 ↓
LED OFF

single
 ↓
LED ON

multiple
 ↓
LED BLINK
```

GPIO17は、Raspberry Pi Zero WHの物理ピン11に対応します。

---

## 使用技術

|技術|用途|
|---|---|
|Python|システム全体の開発|
|OpenCV|カメラ映像の取得・画像処理|
|YOLO|人物認識|
|MariaDB|状態データの保存|
|Flask|Webインターフェース・通信API|
|Raspberry Pi Zero WH|GPIOによる物理制御|
|gpiozero|Raspberry PiのGPIO制御|
|Git|ソースコード管理|

---

## 開発環境

主な開発環境は以下を想定しています。

- Ubuntu
    
- Python 3
    
- Raspberry Pi Zero WH
    
- USBカメラ
    
- MariaDB
    

Pythonの依存パッケージについては、プロジェクトの仮想環境を利用してインストールしてください。

---

## ディレクトリ構成

プロジェクトは基本的に次のような構成になっています。

```text
python-autonomous-ai-book/
│
├── chapter01
│   ├── environment_check.py
│   └── hello.py
├── chapter02
│   ├── chapter02-3-1.py
│   ├── chapter02-3-2.py
│   ├── chapter02-4.py
│   ├── chapter02-5.py
│   ├── chapter02-6.py
│   └── chapter02-7.py
├── chapter03
│   ├── chapter03-2-1.py
│   ├── chapter03-2-2.py
│   ├── chapter03-3.py
│   ├── chapter03-4.py
│   ├── chapter03-5.py
│   ├── chapter03-6.py
│   └── yolo11n.pt
├── chapter04
│   ├── chapter04-1-1.py
│   ├── chapter04-1-2.py
│   ├── chapter04-14.py
│   ├── chapter04-15.py
│   ├── chapter04-16.py
│   ├── chapter04-2-1.py
│   ├── chapter04-2-2.py
│   ├── chapter04-5.py
│   └── yolo11n.pt
├── chapter05
│   ├── chapter05-2-1.py
│   ├── chapter05-2-2.py
│   ├── chapter05-3-1.py
│   ├── chapter05-3-2.py
│   ├── chapter05-4-1.py
│   ├── chapter05-4-2.py
│   ├── chapter05-5-1.py
│   ├── chapter05-5-2.py
│   ├── chapter05-5-3.py
│   ├── chapter05-5-4.py
│   ├── chapter05-6-1.py
│   ├── chapter05-6-2.py
│   ├── chapter05-6-3.py
│   ├── chapter05-6-4.py
│   └── yolo11n.pt
├── chapter06
│   ├── chapter06-1-1.py
│   ├── chapter06-1-2.py
│   ├── chapter06-2-1.py
│   ├── chapter06-2-2.py
│   ├── chapter06-3-1.py
│   ├── chapter06-3-2.py
│   ├── chapter06-4-1.py
│   ├── chapter06-4-2.py
│   ├── chapter06-6.py
│   └── yolo11n.pt
├── chapter07
│   ├── chapter07-8-1.py
│   ├── chapter07-8-2.py
│   ├── chapter07-8-3.py
│   ├── chapter07-9-1.py
│   └── chapter07-9-2.py
├── chapter08
│   ├── chapter08-4-1.py
│   ├── chapter08-4-2.py
│   ├── chapter08-5.py
│   ├── chapter08-6.py
│   ├── chapter08-7-1.py
│   └── chapter08-7-2.py
├── chapter09
│   ├── chapter09-1.py
│   ├── chapter09-8-1.py
│   ├── chapter09-8-2.py
│   └── yolo11n.pt
├── chapter10
│   ├── chapter10-1.py
│   ├── chapter10-2.py
│   ├── chapter10-9.py
│   └── templates
│       └── index.html
├── chapter11
│   ├── chapter11-3.py
│   ├── chapter11-6.py
│   ├── chapter11-8.py
│   └── yolo11n.pt
└── chapter12
    ├── chapter12-10.py
    ├── chapter12-11.py
    ├── static
    │   └── style.css
    ├── system.log
    ├── templates
    │   └── index.html
    └── yolo11n.pt

```

実際の構成は、各章で追加されるプログラムに応じて変化します。

---

## Python仮想環境

プロジェクトではPythonの仮想環境を利用します。

```bash
python3 -m venv .venv
```

仮想環境を有効にします。

```bash
source .venv/bin/activate
```

仮想環境を終了するときは、

```bash
deactivate
```

を実行します。

---

## MariaDB

MariaDBには、カメラとYOLOによって取得した人物情報を保存します。

第4章で使用するテーブルの基本構造は以下のとおりです。

```sql
CREATE TABLE person_states (
    id INT AUTO_INCREMENT PRIMARY KEY,
    recorded_at DATETIME(6) NOT NULL,
    person_id INT NOT NULL,
    x INT NOT NULL,
    y INT NOT NULL,
    person_count INT NOT NULL
);
```

このテーブルには、人物の位置や検出された人物数などを保存します。

章が進むにつれて、システムの機能に合わせてデータベース構成も発展させていきます。

---

## Raspberry Piの接続

Raspberry Pi Zero WHは、Ubuntu PCとネットワーク経由で通信します。

Ubuntu PCからRaspberry PiへHTTPリクエストを送信し、人物の状態を伝えます。

```text
Ubuntu PC
    │
    │ HTTP
    ↓
Raspberry Pi
    │
    ↓
GPIO17
    │
    ↓
LED
```

Raspberry Pi側ではFlaskを利用して制御用APIを提供します。

---

## システムの起動

### 1. Raspberry Pi側

Raspberry Pi上で制御プログラムを起動します。

```bash
python3 raspi_controller.py
```

Flaskサーバーが起動すると、Ubuntu PCからHTTP通信を受け付けられるようになります。

### 2. Ubuntu PC側

Ubuntu PCでAIシステムを起動します。

```bash
python3 main.py
```

システムが起動すると、カメラ映像の取得、YOLOによる人物認識、状態判断、MariaDBへの保存、Raspberry Piへの制御命令送信などが開始されます。

---

## Webインターフェース

FlaskによるWebインターフェースから、システムの状態を確認できます。

表示する情報の例：

```text
人物数
状態
FPS
CPU使用率
メモリ使用率
Raspberry Piの状態
```

Ubuntu PCのIPアドレスが`192.168.1.100`の場合、

```text
http://192.168.1.100:5000
```

からアクセスします。

---

## 状態判断

人物数に応じて、システムの状態を3種類に分類します。

```text
0人
 ↓
empty

1人
 ↓
single

2人以上
 ↓
multiple
```

この状態をRaspberry Piへ送信し、LEDを制御します。

```text
empty
 → LED消灯

single
 → LED点灯

multiple
 → LED点滅
```

---

## FPS

AI処理は、目標FPSを設定して実行します。

本システムでは、基本的な目標値として5FPSを使用します。

```text
5FPS
↓
1フレームあたり約0.2秒
```

実際のFPSは、使用するコンピュータ、カメラ、YOLOモデルなどによって変化します。

---

## ログ

長時間動作するシステムでは、システムの状態やエラーを記録します。

例えば、

```text
AI system started
Database connected
State changed
Raspberry Pi connection error
```

などの情報をログとして記録します。

ログを利用することで、システムに問題が発生した場合に、いつ、どのような問題が発生したのかを確認できます。

---

## エラー処理

自律型AIシステムでは、一部の機能でエラーが発生しても、可能な限りシステム全体の処理を継続できるようにします。

例えば、Raspberry Piとの通信に失敗した場合でも、カメラによる観測やYOLOによる認識処理を継続できるようにします。

また、システム終了時にはカメラやデータベースなどのリソースを解放し、Raspberry PiのLEDを消灯します。

---

## フィードバックループ

本システムの特徴は、AIによる認識結果を単に表示するだけではなく、その結果を利用して現実世界を制御することです。

基本的な流れは、

```text
カメラ
 ↓
YOLO
 ↓
人物認識
 ↓
状態判断
 ↓
Raspberry Pi
 ↓
GPIO
 ↓
LED
 ↓
環境
 ↓
カメラ
```

となります。

この循環によって、システムは環境を観測し、その状態を判断し、物理的な制御を行い、変化した環境を再び観測します。

---

## 本リポジトリについて

本リポジトリでは、自律型AIシステムを段階的に構築するためのコードを公開しています。

最初からすべての機能を実装するのではなく、

```text
開発環境
 ↓
カメラ
 ↓
YOLO
 ↓
データベース
 ↓
Webインターフェース
 ↓
Raspberry Pi
 ↓
フィードバック
 ↓
システム統合
```

という順番で、システムを少しずつ発展させていきます。

各章のコードを実際に動かしながら、AIによる認識だけではなく、データベース、ネットワーク、物理デバイス、Webインターフェースを組み合わせたシステム開発を学ぶことを目的としています。

---

## License

本リポジトリのライセンスについては、リポジトリ内の`LICENSE`ファイルを確認してください。