import uuid
from datetime import datetime
from botocore.exceptions import ClientError

# Import from Lambda Layer
from utils import (
    get_table,
    create_success_response,
    create_error_response,
    handle_dynamodb_error,
    parse_json_body,
)


def lambda_handler(event, context):
    """
    Lambda function handler for creating items in DynamoDB
    """
    try:
        return create_item(event)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return create_error_response(
            500, "Internal Server Error", "An unexpected error occurred"
        )


def create_item(event):
    """Create a new item"""
    try:
        table = get_table()

        # Parse request body
        body, error_response = parse_json_body(event)
        if error_response:
            return error_response

        # Validate required fields
        if not body.get("name"):
            return create_error_response(400, "Bad Request", "Field 'name' is required")

        # Generate unique ID
        item_id = str(uuid.uuid4())

        # Create item with timestamp
        item = {
            "id": item_id,
            "name": body["name"],
            "description": body.get("description", ""),
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }

        # Add any additional fields from request
        for key, value in body.items():
            if key not in ["id", "created_at", "updated_at"]:
                item[key] = value

        # Put item in DynamoDB
        table.put_item(Item=item)

        return create_success_response(201, item)

    except ClientError as e:
        return handle_dynamodb_error(e)
    except Exception as e:
        print(f"Error creating item: {str(e)}")
        return create_error_response(
            500, "Internal Server Error", "Failed to create item"
        )
