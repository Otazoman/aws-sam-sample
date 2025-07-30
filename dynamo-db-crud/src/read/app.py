import json
from botocore.exceptions import ClientError

# Import from Lambda Layer
from utils import (
    get_table,
    create_success_response,
    create_error_response,
    handle_dynamodb_error,
)


def lambda_handler(event, context):
    """
    Lambda function handler for reading items from DynamoDB
    """
    try:
        # Get path parameters
        path_parameters = event.get("pathParameters") or {}
        item_id = path_parameters.get("id")

        if item_id:
            return get_item(item_id)
        else:
            return get_all_items(event)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return create_error_response(
            500, "Internal Server Error", "An unexpected error occurred"
        )


def get_all_items(event):
    """Get all items with optional pagination"""
    try:
        table = get_table()

        # Get query parameters
        query_params = event.get("queryStringParameters") or {}
        limit = int(query_params.get("limit", 50))

        # Validate limit
        if limit > 100:
            return create_error_response(400, "Bad Request", "Limit cannot exceed 100")

        scan_kwargs = {"Limit": limit}

        # Handle pagination
        if query_params.get("last_key"):
            try:
                last_key = json.loads(query_params["last_key"])
                scan_kwargs["ExclusiveStartKey"] = last_key
            except json.JSONDecodeError:
                return create_error_response(
                    400, "Bad Request", "Invalid last_key format"
                )

        # Scan table
        response = table.scan(**scan_kwargs)

        result = {"items": response["Items"], "count": len(response["Items"])}

        # Add pagination info if there are more items
        if "LastEvaluatedKey" in response:
            result["last_key"] = response["LastEvaluatedKey"]
            result["has_more"] = True
        else:
            result["has_more"] = False

        return create_success_response(200, result)

    except ClientError as e:
        return handle_dynamodb_error(e)
    except Exception as e:
        print(f"Error getting items: {str(e)}")
        return create_error_response(
            500, "Internal Server Error", "Failed to retrieve items"
        )


def get_item(item_id):
    """Get a single item by ID"""
    try:
        table = get_table()

        if not item_id:
            return create_error_response(400, "Bad Request", "Item ID is required")

        # Get item from DynamoDB
        response = table.get_item(Key={"id": item_id})

        if "Item" not in response:
            return create_error_response(404, "Not Found", "Item not found")

        return create_success_response(200, response["Item"])

    except ClientError as e:
        return handle_dynamodb_error(e)
    except Exception as e:
        print(f"Error getting item: {str(e)}")
        return create_error_response(
            500, "Internal Server Error", "Failed to retrieve item"
        )
