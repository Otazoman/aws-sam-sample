# DynamoDB Local テスト環境セットアップ

このドキュメントでは、DynamoDB Localを使用してローカル環境でCRUD APIをテストする方法を説明します。

## 前提条件

- DynamoDB Localが起動済み（ポート8000）
- Python 3.x がインストール済み

## セットアップとテスト実行手順

### 1. 必要なパッケージのインストールとテストの実行

`test` ディレクトリに移動し、以下のスクリプトを実行するだけです。
必要なパッケージのインストール（初回のみ）、テーブルのセットアップ、テストの実行がすべて自動で行われます。

```bash
cd sam_apps/dynamo-db-crud/test
./run_local_test_venv.sh
```

このスクリプトは以下を実行します：
- Python仮想環境 `venv` を作成（存在しない場合）
- 必要なパッケージ（boto3, botocore）をインストール
- DynamoDB Localに接続
- `local-items-dev` テーブルを作成
- CRUD操作のテストを実行

## テスト内容

テストスクリプトは以下のCRUD操作をテストします：

1. **CREATE**: 新しいアイテムの作成
2. **READ ALL**: 全アイテムの取得
3. **READ ONE**: 特定アイテムの取得
4. **UPDATE**: アイテムの更新
5. **DELETE**: アイテムの削除

## ファイル構成

```
sam_apps/dynamo-db-crud/
├── test/                     # テスト関連ファイル
│   ├── setup_local_table.py      # テーブル作成スクリプト
│   ├── test_local.py       # Lambda関数テストスクリプト
│   ├── utils_local.py            # ローカル用ユーティリティ
│   └── run_local_test_venv.sh    # 一括実行スクリプト（仮想環境）
├── venv/                     # Python仮想環境
├── src/                      # Lambda関数ソースコード
├── layers/                   # Lambda Layer
├── events/                   # テストイベント
├── template.yaml             # SAMテンプレート
└── README_LOCAL_TEST.md      # このファイル
```

## 設定

### DynamoDB Local設定

- **エンドポイント**: http://localhost:8000
- **リージョン**: us-east-1
- **アクセスキー**: dummy
- **シークレットキー**: dummy
- **テーブル名**: local-items-dev

## トラブルシューティング

### DynamoDB Localに接続できない

```bash
# DynamoDB Localの起動状態を確認
curl http://localhost:8000

# プロセス確認
ps aux | grep dynamodb
```

### テーブルが作成されない

1. DynamoDB Localが正常に起動していることを確認
2. ポート8000が他のプロセスで使用されていないか確認
3. `run_local_test_venv.sh` を再実行

## DynamoDB Local管理画面

DynamoDB Localの管理画面が利用可能な場合：
- URL: http://localhost:8001
- テーブルの内容を視覚的に確認可能

## 本番環境との違い

ローカルテスト環境では以下の点が本番環境と異なります：

1. **エンドポイント**: localhost:8000 vs AWS DynamoDB
2. **認証**: ダミー認証 vs IAM認証
3. **テーブル名**: local-items-dev vs 実際のテーブル名
4. **リージョン**: us-east-1固定 vs 設定可能

## 次のステップ

ローカルテストが成功したら：

1. SAM CLIを使用したローカル実行
2. AWS環境へのデプロイ
3. API Gatewayを通じたテスト

```bash
# SAM ローカル実行例
sam local start-api --docker-network dynamodb_sam-test-network --env-vars test/env.json
