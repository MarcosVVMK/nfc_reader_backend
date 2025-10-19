
# FastAPI Backend - API Endpoints Documentation

## Base URL
- Development: `http://localhost:8000`
- API Base: `http://localhost:8000/api/v1`

## Available Endpoints

### 1. Root Endpoint
- **GET** `/`
  - Description: Welcome message
  - Response: `{"message": "Programação 3 Backend API is running!"}`

### 2. Health Check Endpoints
- **GET** `/api/v1/health`
  - Description: Check if the API is running
  - Response: `{"status": "healthy", "message": "API is running"}`

- **GET** `/api/v1/health/db`  
  - Description: Check database connectivity
  - Response: 
    - Success: `{"status": "healthy", "message": "Database connection is working"}`
    - Error: `{"status": "unhealthy", "message": "Database connection failed: <error>"}`

### 3. Users CRUD Endpoints

#### Create User
- **POST** `/api/v1/users/`
  - Description: Create a new user
  - Request Body:
    ```json
    {
      "name": "João Silva",
      "email": "joao@example.com"
    }
    ```
  - Response (201):
    ```json
    {
      "id": 1,
      "name": "João Silva", 
      "email": "joao@example.com",
      "created_at": "2024-01-01T12:00:00",
      "updated_at": null
    }
    ```

#### List Users
- **GET** `/api/v1/users/`
  - Description: Get all users with pagination
  - Query Parameters:
    - `skip`: Number of users to skip (default: 0)
    - `limit`: Maximum number of users to return (default: 100)
  - Example: `/api/v1/users/?skip=0&limit=10`
  - Response:
    ```json
    [
      {
        "id": 1,
        "name": "João Silva",
        "email": "joao@example.com", 
        "created_at": "2024-01-01T12:00:00",
        "updated_at": null
      }
    ]
    ```

#### Get User by ID
- **GET** `/api/v1/users/{user_id}`
  - Description: Get a specific user by ID
  - Path Parameters:
    - `user_id`: User ID (integer)
  - Example: `/api/v1/users/1`
  - Response (200):
    ```json
    {
      "id": 1,
      "name": "João Silva",
      "email": "joao@example.com",
      "created_at": "2024-01-01T12:00:00", 
      "updated_at": null
    }
    ```
  - Error (404):
    ```json
    {"detail": "User not found"}
    ```

#### Update User
- **PUT** `/api/v1/users/{user_id}`
  - Description: Update a user
  - Path Parameters:
    - `user_id`: User ID (integer)
  - Request Body (partial update allowed):
    ```json
    {
      "name": "João Santos",
      "email": "joao.santos@example.com"
    }
    ```
  - Response (200):
    ```json
    {
      "id": 1,
      "name": "João Santos",
      "email": "joao.santos@example.com",
      "created_at": "2024-01-01T12:00:00",
      "updated_at": "2024-01-01T13:00:00"
    }
    ```

#### Delete User  
- **DELETE** `/api/v1/users/{user_id}`
  - Description: Delete a user
  - Path Parameters:
    - `user_id`: User ID (integer)
  - Response (204): No content
  - Error (404):
    ```json
    {"detail": "User not found"}
    ```

## Interactive Documentation
When the server is running, you can access:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Error Responses
All endpoints may return the following error responses:

### 400 Bad Request
```json
{"detail": "Email already registered"}
```

### 404 Not Found  
```json
{"detail": "User not found"}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 500 Internal Server Error
```json
{"detail": "Internal server error"}
```

## Example Usage with curl

### Create a user:
```bash
curl -X POST "http://localhost:8000/api/v1/users/" \
     -H "Content-Type: application/json" \
     -d '{"name": "João Silva", "email": "joao@example.com"}'
```

### Get all users:
```bash
curl "http://localhost:8000/api/v1/users/"
```

### Get specific user:
```bash  
curl "http://localhost:8000/api/v1/users/1"
```

### Update user:
```bash
curl -X PUT "http://localhost:8000/api/v1/users/1" \
     -H "Content-Type: application/json" \
     -d '{"name": "João Santos"}'
```

### Delete user:
```bash
curl -X DELETE "http://localhost:8000/api/v1/users/1"
```
