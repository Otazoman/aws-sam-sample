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
    Lambda function handler for deleting items from DynamoDB
    """
    try:
        # Get path parameters
        path_parameters = event.get("pathParameters") or {}
        item_id = path_parameters.get("id")

        return delete_item(item_id)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return create_error_response(
            500, "Internal Server Error", "An unexpected error occurred"
        )


def delete_item(item_id):
    """Delete an item by ID"""
    try:
        table = get_table()

        if not item_id:
            return create_error_response(400, "Bad Request", "Item ID is required")

        # Check if item exists before deleting
        existing_response = table.get_item(Key={"id": item_id})
        if "Item" not in existing_response:
            return create_error_response(404, "Not Found", "Item not found")

        # Delete item
        table.delete_item(Key={"id": item_id})

        return create_success_response(
            200, {"message": "Item deleted successfully", "id": item_id}
        )

    except ClientError as e:
        return handle_dynamodb_error(e)
    except Exception as e:
        print(f"Error deleting item: {str(e)}")
        return create_error_response(
            500, "Internal Server Error", "Failed to delete item"
        )
