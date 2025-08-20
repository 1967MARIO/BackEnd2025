# Endpoints principales

## Backend con Flask: API REST + Autenticación JWT + Escalabilidad

Este proyecto implementa un backend funcional en Flask con:

API RESTful (CRUD de items) con validación y paginación.

Autenticación y autorización con JWT (registro, login, refresh, roles).

Optimización y escalabilidad: rate limiting, caching con Redis, logging estructurado, configuración 12‑factor, Docker y Gunicorn.

### Auth
- POST /auth/register { email, password }
- POST /auth/login { email, password } -> { access_token, refresh_token }
- POST /auth/refresh (header Authorization: Bearer <refresh>) -> { access_token }
- GET /auth/me (Bearer access)

#### Items
- GET /api/items?page=1&per_page=10&sort=id&order=asc (Bearer access)
- POST /api/items { name, description } (Bearer access)
- GET /api/items/<id> (Bearer access)
- PUT /api/items/<id> { name?, description? } (Bearer access)
- DELETE /api/items/<id> (Bearer access)

##### Códigos de estado
- 200 OK, 201 Created, 204 No Content, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 409 Conflict, 429 Too Many Requests.
  
###### Buenas prácticas de seguridad y rendimiento (incluidas)
-Hash de contraseñas con Werkzeug (PBKDF2).
-JWT con expiración y refresh tokens.
-Roles en claims (RABC simple).
-Rate limiting en /auth/login y /auth/register para mitigar fuerza bruta.
-Caching de respuestas GET con Redis.
-Paginación y ordenación para colecciones.
-12‑factor config con .env.
-Gunicorn con workers y threads para I/O bound.
-Usuario no root dentro del contenedor.



