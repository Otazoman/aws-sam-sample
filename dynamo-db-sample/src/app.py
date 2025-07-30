import json
import boto3

client = boto3.client("dynamodb", endpoint_url="http://dynamodb:8000")


def lambda_handler(event, context):
    # リクエストbody取得
    body = json.loads(event["body"])
    name = body["name"]
    # db登録
    result = client.put_item(TableName="members", Item={"name": {"S": name}})
    response = {"statusCode": 200, "body": json.dumps(result)}

    return response
