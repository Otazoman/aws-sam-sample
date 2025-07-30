import json
import boto3
import os

# DynamoDB Localの設定
DYNAMODB_LOCAL_ENDPOINT = "http://localhost:8000"

# DynamoDB Localリソースを初期化
dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url=DYNAMODB_LOCAL_ENDPOINT,
    region_name="us-east-1",
    aws_access_key_id="dummy",
    aws_secret_access_key="dummy",
)

table_name = os.environ.get("TABLE_NAME", "local-items-dev")
table = dynamodb.Table(table_name)


def get_table():
    """Get DynamoDB table instance"""
    return table


def create_success_response(status_code, data):
    """Create a successful HTTP response"""
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS",
            "Access-Control-Allow-Headers": (
                "Content-Type,X-Amz-Date,Authorization,X-Api-Key,"
                "X-Amz-Security-Token"
            ),
        },
        "body": json.dumps(data, default=str),
    }


def create_error_response(status_code, error_type, message):
    """Create an error HTTP response"""
    error_response = {
        "error": error_type,
        "message": message,
        "status_code": status_code,
    }

    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS",
            "Access-Control-Allow-Headers": (
                "Content-Type,X-Amz-Date,Authorization,X-Api-Key,"
                "X-Amz-Security-Token"
            ),
        },
        "body": json.dumps(error_response),
    }


def handle_dynamodb_error(e):
    """Handle common DynamoDB errors"""
    error_code = e.response["Error"]["Code"]
    if error_code == "ProvisionedThroughputExceededException":
        return create_error_response(
            429, "Too Many Requests", "Request rate limit exceeded"
        )
    elif error_code == "ServiceUnavailable":
        return create_error_response(
            503, "Service Unavailable", "Service temporarily unavailable"
        )
    else:
        return create_error_response(
            500, "Internal Server Error", f"Database error: {error_code}"
        )


def parse_json_body(event):
    """Parse and validate JSON body from event"""
    if not event.get("body"):
        return None, create_error_response(
            400, "Bad Request", "Request body is required"
        )

    try:
        body = json.loads(event["body"])
        return body, None
    except json.JSONDecodeError:
        return None, create_error_response(
            400, "Bad Request", "Invalid JSON in request body"
        )
