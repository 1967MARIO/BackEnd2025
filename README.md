# Endpoints principales

## Auth
- POST /auth/register { email, password }
- POST /auth/login { email, password } -> { access_token, refresh_token }
- POST /auth/refresh (header Authorization: Bearer <refresh>) -> { access_token }
- GET /auth/me (Bearer access)

## Items
- GET /api/items?page=1&per_page=10&sort=id&order=asc (Bearer access)
- POST /api/items { name, description } (Bearer access)
- GET /api/items/<id> (Bearer access)
- PUT /api/items/<id> { name?, description? } (Bearer access)
- DELETE /api/items/<id> (Bearer access)

### Códigos de estado
- 200 OK, 201 Created, 204 No Content, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 409 Conflict, 429 Too Many Requests.