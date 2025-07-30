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
    Lambda function handler for updating items in DynamoDB
    """
    try:
        # Get path parameters
        path_parameters = event.get("pathParameters") or {}
        item_id = path_parameters.get("id")

        return update_item(event, item_id)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return create_error_response(
            500, "Internal Server Error", "An unexpected error occurred"
        )


def update_item(event, item_id):
    """Update an existing item"""
    try:
        table = get_table()

        if not item_id:
            return create_error_response(400, "Bad Request", "Item ID is required")

        # Parse request body
        body, error_response = parse_json_body(event)
        if error_response:
            return error_response

        # Check if item exists
        existing_response = table.get_item(Key={"id": item_id})
        if "Item" not in existing_response:
            return create_error_response(404, "Not Found", "Item not found")

        # Build update expression
        update_expression = "SET #updated_at = :updated_at"
        expression_values = {":updated_at": datetime.utcnow().isoformat()}
        expression_names = {"#updated_at": "updated_at"}

        # Add fields to update (excluding id, created_at)
        for key, value in body.items():
            if key not in ["id", "created_at"]:
                expression_key = f"#{key}"
                expression_value_key = f":{key}"
                update_expression += f", {expression_key} = {expression_value_key}"
                expression_values[expression_value_key] = value
                expression_names[expression_key] = key

        # Update item
        response = table.update_item(
            Key={"id": item_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_values,
            ExpressionAttributeNames=expression_names,
            ReturnValues="ALL_NEW",
        )

        return create_success_response(200, response["Attributes"])

    except ClientError as e:
        return handle_dynamodb_error(e)
    except Exception as e:
        print(f"Error updating item: {str(e)}")
        return create_error_response(
            500, "Internal Server Error", "Failed to update item"
        )
