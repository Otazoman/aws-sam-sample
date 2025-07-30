#!/bin/bash

# DynamoDB Local テスト実行スクリプト（仮想環境版）

echo "DynamoDB Local テスト環境セットアップ（仮想環境）"
echo "=============================================="

# 現在のディレクトリを確認
echo "現在のディレクトリ: $(pwd)"

# 仮想環境の存在確認
if [ ! -d "venv" ]; then
    echo "仮想環境が見つかりません。作成中..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ 仮想環境の作成に失敗しました"
        exit 1
    fi
    echo "✅ 仮想環境を作成しました"
fi

# 仮想環境をアクティベート
echo "仮想環境をアクティベート中..."
source venv/bin/activate

# 必要なパッケージがインストールされているかチェック
echo "必要なパッケージをチェック中..."
python -c "import boto3, botocore" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "boto3パッケージをインストール中..."
    pip install boto3 botocore
    if [ $? -ne 0 ]; then
        echo "❌ パッケージのインストールに失敗しました"
        exit 1
    fi
fi
echo "✅ boto3パッケージが利用可能です"

# DynamoDB Localが起動しているかチェック
echo "DynamoDB Local接続テスト..."
if curl -s http://localhost:8000 > /dev/null 2>&1; then
    echo "✅ DynamoDB Local (http://localhost:8000) に接続できました"
else
    echo "❌ DynamoDB Local (http://localhost:8000) に接続できません"
    echo "DynamoDB Localが起動していることを確認してください"
    deactivate
    exit 1
fi

# テーブルセットアップ
echo ""
echo "テーブルセットアップを実行中..."
python setup_local_table.py
if [ $? -ne 0 ]; then
    echo "❌ テーブルセットアップに失敗しました"
    deactivate
    exit 1
fi

# テスト実行
echo ""
echo "Lambda関数のローカルテストを実行中..."
python test_local.py

# 仮想環境を非アクティベート
deactivate

echo ""
echo "テスト完了!"
echo ""
echo "DynamoDB Local管理画面: http://localhost:8001 (利用可能な場合)"
echo "DynamoDB Localエンドポイント: http://localhost:8000"
echo "仮想環境: venv/ (作成済み)"
