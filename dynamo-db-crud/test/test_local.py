#!/usr/bin/env python3
"""
DynamoDB Local用のテストスクリプト（修正版）
Lambda関数をローカルでテストします
"""
import json
import os
import sys
import uuid
from datetime import datetime

# 環境変数を最初に設定
os.environ["AWS_ACCESS_KEY_ID"] = "dummy"
os.environ["AWS_SECRET_ACCESS_KEY"] = "dummy"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
os.environ["TABLE_NAME"] = "local-items-dev"

# boto3をインポートしてDynamoDB Localクライアントを作成
import boto3
from botocore.exceptions import ClientError

# DynamoDB Localリソースを作成
dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url="http://localhost:8000",
    region_name="us-east-1",
    aws_access_key_id="dummy",
    aws_secret_access_key="dummy",
)

table = dynamodb.Table("local-items-dev")


def create_success_response(status_code, data):
    """Create a successful HTTP response"""
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(data, default=str),
    }


def create_error_response(status_code, error_type, message):
    """Create an error HTTP response"""
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(
            {
                "error": error_type,
                "message": message,
                "status_code": status_code,
            }
        ),
    }


def test_create_item():
    """アイテム作成のテスト"""
    print("\n=== CREATE ITEM TEST ===")

    try:
        # Generate unique ID
        item_id = str(uuid.uuid4())

        # Create item with timestamp
        item = {
            "id": item_id,
            "name": "Test Item",
            "description": "This is a test item",
            "category": "test",
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }

        # Put item in DynamoDB
        table.put_item(Item=item)

        response = create_success_response(201, item)
        print(f"Status Code: {response['statusCode']}")
        print(f"Response: {response['body']}")

        return item_id

    except Exception as e:
        print(f"Error: {e}")
        return None


def test_read_items():
    """アイテム一覧取得のテスト"""
    print("\n=== READ ITEMS TEST ===")

    try:
        response_data = table.scan()
        items = response_data.get("Items", [])

        response = create_success_response(200, {"items": items})
        print(f"Status Code: {response['statusCode']}")
        print(f"Response: {response['body']}")

        return True

    except Exception as e:
        print(f"Error: {e}")
        return False


def test_read_item(item_id):
    """特定アイテム取得のテスト"""
    print(f"\n=== READ ITEM TEST (ID: {item_id}) ===")

    try:
        response_data = table.get_item(Key={"id": item_id})

        if "Item" in response_data:
            item = response_data["Item"]
            response = create_success_response(200, item)
        else:
            response = create_error_response(404, "Not Found", "Item not found")

        print(f"Status Code: {response['statusCode']}")
        print(f"Response: {response['body']}")

        return response["statusCode"] == 200

    except Exception as e:
        print(f"Error: {e}")
        return False


def test_update_item(item_id):
    """アイテム更新のテスト"""
    print(f"\n=== UPDATE ITEM TEST (ID: {item_id}) ===")

    try:
        # Update item
        response_data = table.update_item(
            Key={"id": item_id},
            UpdateExpression="SET #name = :name, description = :desc, category = :cat, updated_at = :updated",
            ExpressionAttributeNames={"#name": "name"},
            ExpressionAttributeValues={
                ":name": "Updated Test Item",
                ":desc": "This item has been updated",
                ":cat": "updated",
                ":updated": datetime.utcnow().isoformat(),
            },
            ReturnValues="ALL_NEW",
        )

        updated_item = response_data.get("Attributes", {})
        response = create_success_response(200, updated_item)
        print(f"Status Code: {response['statusCode']}")
        print(f"Response: {response['body']}")

        return True

    except Exception as e:
        print(f"Error: {e}")
        return False


def test_delete_item(item_id):
    """アイテム削除のテスト"""
    print(f"\n=== DELETE ITEM TEST (ID: {item_id}) ===")

    try:
        table.delete_item(Key={"id": item_id})

        response = create_success_response(
            200, {"message": "Item deleted successfully"}
        )
        print(f"Status Code: {response['statusCode']}")
        print(f"Response: {response['body']}")

        return True

    except Exception as e:
        print(f"Error: {e}")
        return False


def main():
    """メインテスト実行"""
    print("DynamoDB Local CRUD テスト開始")
    print("=" * 50)

    # 1. アイテム作成テスト
    item_id = test_create_item()
    if not item_id:
        print("❌ CREATE テスト失敗")
        return
    print("✅ CREATE テスト成功")

    # 2. アイテム一覧取得テスト
    if test_read_items():
        print("✅ READ ALL テスト成功")
    else:
        print("❌ READ ALL テスト失敗")

    # 3. 特定アイテム取得テスト
    if test_read_item(item_id):
        print("✅ READ ONE テスト成功")
    else:
        print("❌ READ ONE テスト失敗")

    # 4. アイテム更新テスト
    if test_update_item(item_id):
        print("✅ UPDATE テスト成功")
    else:
        print("❌ UPDATE テスト失敗")

    # 5. アイテム削除テスト
    if test_delete_item(item_id):
        print("✅ DELETE テスト成功")
    else:
        print("❌ DELETE テスト失敗")

    print("\n" + "=" * 50)
    print("テスト完了")


if __name__ == "__main__":
    main()
