# API Documentation

## Base URL

- **Development:** `http://localhost:8000/api/v1`
- **Production:** `https://api.sabsteck.com/api/v1` (TBD)

## Authentication

Alle geschützten Endpoints benötigen einen JWT-Token im Authorization Header:

```
Authorization: Bearer <token>
```

### Token erhalten

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

## API Endpoints

### Authentication

#### Register
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword",
  "name": "John Doe"
}
```

**Response (201):**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "name": "John Doe",
  "created_at": "2025-10-23T00:00:00Z"
}
```

#### Login
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

#### Refresh Token
```http
POST /api/v1/auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJhbGc..."
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### Users

#### Get Current User
```http
GET /api/v1/users/me
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "name": "John Doe",
  "created_at": "2025-10-23T00:00:00Z",
  "updated_at": "2025-10-23T00:00:00Z"
}
```

#### Update Profile
```http
PUT /api/v1/users/me
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Jane Doe",
  "email": "jane@example.com"
}
```

**Response (200):**
```json
{
  "id": "uuid",
  "email": "jane@example.com",
  "name": "Jane Doe",
  "updated_at": "2025-10-23T01:00:00Z"
}
```

#### Delete Account
```http
DELETE /api/v1/users/me
Authorization: Bearer <token>
```

**Response (204):** No Content

### Income Sources

#### List Income Sources
```http
GET /api/v1/income?page=1&per_page=20
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "items": [
    {
      "id": "uuid",
      "user_id": "uuid",
      "name": "Salary",
      "amount": 5000.00,
      "currency": "EUR",
      "frequency": "monthly",
      "category": "employment",
      "description": "Main job salary",
      "active": true,
      "created_at": "2025-10-23T00:00:00Z",
      "updated_at": "2025-10-23T00:00:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "per_page": 20,
  "pages": 1
}
```

#### Create Income Source
```http
POST /api/v1/income
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Freelance Work",
  "amount": 2000.00,
  "currency": "EUR",
  "frequency": "monthly",
  "category": "freelance",
  "description": "Web development projects",
  "active": true
}
```

**Response (201):**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "name": "Freelance Work",
  "amount": 2000.00,
  "currency": "EUR",
  "frequency": "monthly",
  "category": "freelance",
  "description": "Web development projects",
  "active": true,
  "created_at": "2025-10-23T00:00:00Z",
  "updated_at": "2025-10-23T00:00:00Z"
}
```

#### Get Income Source
```http
GET /api/v1/income/{id}
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "name": "Salary",
  "amount": 5000.00,
  "currency": "EUR",
  "frequency": "monthly",
  "category": "employment",
  "description": "Main job salary",
  "active": true,
  "created_at": "2025-10-23T00:00:00Z",
  "updated_at": "2025-10-23T00:00:00Z"
}
```

#### Update Income Source
```http
PUT /api/v1/income/{id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "amount": 5500.00,
  "description": "Salary after raise"
}
```

**Response (200):**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "name": "Salary",
  "amount": 5500.00,
  "currency": "EUR",
  "frequency": "monthly",
  "category": "employment",
  "description": "Salary after raise",
  "active": true,
  "created_at": "2025-10-23T00:00:00Z",
  "updated_at": "2025-10-23T01:00:00Z"
}
```

#### Delete Income Source
```http
DELETE /api/v1/income/{id}
Authorization: Bearer <token>
```

**Response (204):** No Content

### Recommendations

#### Get Recommendations
```http
GET /api/v1/recommendations
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "recommendations": [
    {
      "id": "uuid",
      "type": "diversification",
      "title": "Diversify Income Sources",
      "description": "Consider adding passive income streams",
      "priority": "medium",
      "confidence": 0.85,
      "action_items": [
        "Research dividend stocks",
        "Consider rental properties",
        "Explore online courses"
      ],
      "created_at": "2025-10-23T00:00:00Z"
    }
  ]
}
```

#### Send Recommendation Feedback
```http
POST /api/v1/recommendations/feedback
Authorization: Bearer <token>
Content-Type: application/json

{
  "recommendation_id": "uuid",
  "helpful": true,
  "comment": "Great suggestion!"
}
```

**Response (201):**
```json
{
  "id": "uuid",
  "recommendation_id": "uuid",
  "helpful": true,
  "comment": "Great suggestion!",
  "created_at": "2025-10-23T00:00:00Z"
}
```

### Synchronization

#### Get Sync Status
```http
GET /api/v1/sync/status
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "last_sync": "2025-10-23T00:00:00Z",
  "pending_changes": 0,
  "sync_enabled": true
}
```

#### Get Changes Since Last Sync
```http
GET /api/v1/sync/changes?since=2025-10-23T00:00:00Z
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "changes": [
    {
      "entity_type": "income",
      "entity_id": "uuid",
      "action": "update",
      "timestamp": "2025-10-23T01:00:00Z",
      "data": {
        "amount": 5500.00
      }
    }
  ],
  "timestamp": "2025-10-23T02:00:00Z"
}
```

#### Push Local Changes
```http
POST /api/v1/sync/push
Authorization: Bearer <token>
Content-Type: application/json

{
  "changes": [
    {
      "entity_type": "income",
      "entity_id": "uuid",
      "action": "create",
      "timestamp": "2025-10-23T00:30:00Z",
      "data": {
        "name": "Side Project",
        "amount": 500.00
      }
    }
  ]
}
```

**Response (200):**
```json
{
  "processed": 1,
  "conflicts": [],
  "timestamp": "2025-10-23T02:00:00Z"
}
```

## Error Responses

### Standard Error Format
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable error message",
    "details": {}
  }
}
```

### Common Status Codes

- **200** OK - Request successful
- **201** Created - Resource created
- **204** No Content - Successful deletion
- **400** Bad Request - Invalid input
- **401** Unauthorized - Missing/invalid token
- **403** Forbidden - Insufficient permissions
- **404** Not Found - Resource not found
- **409** Conflict - Data conflict (e.g., sync)
- **422** Unprocessable Entity - Validation error
- **429** Too Many Requests - Rate limit exceeded
- **500** Internal Server Error - Server error

### Example Validation Error (422)
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": {
      "amount": ["Must be a positive number"],
      "email": ["Invalid email format"]
    }
  }
}
```

## Rate Limiting

- **Limit:** 100 requests per minute per user
- **Headers:**
  - `X-RateLimit-Limit`: Maximum requests
  - `X-RateLimit-Remaining`: Remaining requests
  - `X-RateLimit-Reset`: Reset timestamp

## Pagination

List endpoints support pagination:

```http
GET /api/v1/income?page=1&per_page=20
```

**Parameters:**
- `page` - Page number (default: 1)
- `per_page` - Items per page (default: 20, max: 100)

## Versioning

API versioning via URL: `/api/v1/`, `/api/v2/`, etc.

## OpenAPI/Swagger

Interactive API documentation:
- **Development:** http://localhost:8000/docs
- **Production:** https://api.sabsteck.com/docs

## Weitere Informationen

- [Architecture Documentation](../architecture/README.md)
- [Backend README](../../backend/README.md)
