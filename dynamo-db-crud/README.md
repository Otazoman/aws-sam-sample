# DynamoDB CRUD API

AWS SAM application that provides a RESTful API for CRUD operations on DynamoDB using Lambda and API Gateway.

## Architecture

- **API Gateway**: RESTful API endpoints
- **Lambda Function**: Business logic for CRUD operations
- **DynamoDB**: NoSQL database for data storage

## API Endpoints

### Base URL
After deployment: `https://{api-id}.execute-api.{region}.amazonaws.com/{stage}/`

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/items` | Create a new item |
| GET | `/items` | Get all items (with pagination) |
| GET | `/items/{id}` | Get a specific item by ID |
| PUT | `/items/{id}` | Update an existing item |
| DELETE | `/items/{id}` | Delete an item |

### Request/Response Examples

#### Create Item (POST /items)
```bash
curl -X POST https://your-api-url/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Sample Item", "description": "This is a sample item"}'
```

Response:
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "Sample Item",
  "description": "This is a sample item",
  "created_at": "2024-01-01T12:00:00.000000",
  "updated_at": "2024-01-01T12:00:00.000000"
}
```

#### Get All Items (GET /items)
```bash
curl https://your-api-url/items?limit=10
```

Response:
```json
{
  "items": [...],
  "count": 10,
  "has_more": true,
  "last_key": {...}
}
```

#### Get Item (GET /items/{id})
```bash
curl https://your-api-url/items/123e4567-e89b-12d3-a456-426614174000
```

#### Update Item (PUT /items/{id})
```bash
curl -X PUT https://your-api-url/items/123e4567-e89b-12d3-a456-426614174000 \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Item", "description": "Updated description"}'
```

#### Delete Item (DELETE /items/{id})
```bash
curl -X DELETE https://your-api-url/items/123e4567-e89b-12d3-a456-426614174000
```

## Error Handling

The API implements comprehensive error handling with the following HTTP status codes:

- **400 Bad Request**: Invalid request parameters or body
- **403 Forbidden**: Access denied
- **404 Not Found**: Resource not found
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: Unexpected server error
- **502 Bad Gateway**: Invalid response from upstream server
- **503 Service Unavailable**: Service temporarily unavailable
- **504 Gateway Timeout**: Request timeout

Error Response Format:
```json
{
  "error": "Error Type",
  "message": "Detailed error message",
  "status_code": 400
}
```

## Deployment

### Prerequisites
- AWS CLI configured
- AWS SAM CLI installed
- Python 3.9+

### Deploy the application

1. Build the application:
```bash
cd sam_apps/dynamo-db-crud
sam build
```

2. Deploy the application:
```bash
sam deploy --guided
```

Follow the prompts to configure:
- Stack name (e.g., `dynamo-db-crud-stack`)
- AWS Region
- Parameter overrides (Stage: dev/prod)
- Confirm changes before deploy: Y
- Allow SAM CLI IAM role creation: Y
- Save parameters to samconfig.toml: Y

### Local Development

Run the API locally:
```bash
# From the `sam_apps/dynamo-db-crud` directory
sam local start-api --docker-network dynamodb_sam-test-network --env-vars test/env.json
```

The API will be available at `http://127.0.0.1:3000`.

You can use `curl` to test the local API endpoints.

#### Create Item (POST /items)
```bash
curl -X POST http://127.0.0.1:3000/items \
-H "Content-Type: application/json" \
-d '{"name": "My Test Item", "description": "A new item from curl"}'
```

#### Get All Items (GET /items)
```bash
curl http://127.0.0.1:3000/items
```

#### Get Item (GET /items/{id})
Replace `{item-id}` with an actual item ID.
```bash
curl http://127.0.0.1:3000/items/{item-id}
```

#### Update Item (PUT /items/{id})
Replace `{item-id}` with an actual item ID.
```bash
curl -X PUT http://127.0.0.1:3000/items/{item-id} \
-H "Content-Type: application/json" \
-d '{"name": "My Updated Item", "description": "This item has been updated"}'
```

#### Delete Item (DELETE /items/{id})
Replace `{item-id}` with an actual item ID.
```bash
curl -X DELETE http://127.0.0.1:3000/items/{item-id}
```

### Testing

Test the deployed API:
```bash
# Get the API URL from stack outputs
aws cloudformation describe-stacks --stack-name your-stack-name --query 'Stacks[0].Outputs'

# Test endpoints
curl https://your-api-url/items
```

## Configuration

### Environment Variables
- `TABLE_NAME`: DynamoDB table name (automatically set)
- `STAGE`: Deployment stage (dev/prod)

### DynamoDB Table
- Table name: `{StackName}-items-{Stage}`
- Partition key: `id` (String)
- Billing mode: Pay-per-request

## Security

- CORS enabled for all origins (configure as needed for production)
- IAM roles with least privilege access
- API Gateway error responses configured to prevent information leakage

## Monitoring

- CloudWatch logs for Lambda function
- API Gateway access logs
- DynamoDB metrics

## Cleanup

To delete the stack:
```bash
sam delete --stack-name your-stack-name
