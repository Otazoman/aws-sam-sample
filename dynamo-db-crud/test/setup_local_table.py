#!/usr/bin/env python3
"""
DynamoDB Local用のテーブル作成スクリプト
"""
import boto3
from botocore.exceptions import ClientError

# DynamoDB Localの設定
DYNAMODB_LOCAL_ENDPOINT = "http://localhost:8000"
TABLE_NAME = "local-items-dev"
REGION = "us-east-1"


def create_dynamodb_client():
    """DynamoDB Localクライアントを作成"""
    return boto3.client(
        "dynamodb",
        endpoint_url=DYNAMODB_LOCAL_ENDPOINT,
        region_name=REGION,
        aws_access_key_id="dummy",
        aws_secret_access_key="dummy",
    )


def create_table():
    """テーブルを作成"""
    dynamodb = create_dynamodb_client()

    try:
        # 既存のテーブルをチェック
        try:
            dynamodb.describe_table(TableName=TABLE_NAME)
            print(f"テーブル '{TABLE_NAME}' は既に存在します")
            return True
        except ClientError as e:
            if e.response["Error"]["Code"] != "ResourceNotFoundException":
                raise

        # テーブル作成
        table_definition = {
            "TableName": TABLE_NAME,
            "KeySchema": [{"AttributeName": "id", "KeyType": "HASH"}],
            "AttributeDefinitions": [{"AttributeName": "id", "AttributeType": "S"}],
            "BillingMode": "PAY_PER_REQUEST",
        }

        dynamodb.create_table(**table_definition)
        print(f"テーブル '{TABLE_NAME}' を作成しました")

        # テーブルがアクティブになるまで待機
        waiter = dynamodb.get_waiter("table_exists")
        waiter.wait(TableName=TABLE_NAME)
        print(f"テーブル '{TABLE_NAME}' がアクティブになりました")

        return True

    except ClientError as e:
        print(f"テーブル作成エラー: {e}")
        return False


def list_tables():
    """テーブル一覧を表示"""
    dynamodb = create_dynamodb_client()

    try:
        response = dynamodb.list_tables()
        tables = response.get("TableNames", [])
        print(f"DynamoDB Localのテーブル一覧: {tables}")
        return tables
    except ClientError as e:
        print(f"テーブル一覧取得エラー: {e}")
        return []


if __name__ == "__main__":
    print("DynamoDB Local テーブルセットアップ")
    print(f"エンドポイント: {DYNAMODB_LOCAL_ENDPOINT}")
    print(f"テーブル名: {TABLE_NAME}")
    print("-" * 50)

    # 現在のテーブル一覧を表示
    list_tables()

    # テーブル作成
    if create_table():
        print("セットアップ完了!")
        list_tables()
    else:
        print("セットアップに失敗しました")
