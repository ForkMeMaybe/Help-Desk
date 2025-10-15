# HelpDesk Mini API

Link: [https://helpdesk-mini-frontend-3ku8.onrender.com/login](https://helpdesk-mini-frontend-3ku8.onrender.com/login)

This is a Django REST Framework project for a mini help desk ticketing system.

## Test Users

- **user:**
  - email: `admin@example.com`
  - password: `ILoveDjango`
- **agent:**
  - email: `agent@example.com`
  - password: `ILoveDjango`
- **admin:**
  - email: `user@example.com`
  - password: `ILoveDjango`

## API Endpoints

### Authentication

- `POST /auth/users/`: Create a new user.
- `POST /auth/jwt/create/`: Get an auth token.
- `POST /auth/users/reset_password/`: Get an link to reset password on email.

### Tickets

- `GET /api/tickets/`: List all tickets.
  - Filtering: `?status=...`, `?priority=...`, `?assigned_to=...`, `?is_breached=true`
  - Searching: `?search=...` (searches `title`, `description`, and latest `comment`)
  - Pagination: `?limit=...`, `?offset=...`
- `POST /api/tickets/`: Create a new ticket.
- `GET /api/tickets/<int:id>/`: Retrieve a single ticket.
- `PATCH /api/tickets/<int:id>/`: Update a ticket. (admin or agent only)
- `DELETE /api/tickets/<int:id>/`: Delete a ticket (admin only).

### Comments

- `POST /api/tickets/<int:id>/comments/`: Create a new comment for a ticket.

### Ticket History

- `GET /api/tickets/`: Get the history of a ticket. (already included with each ticket)

### Meta

- `GET /api/_meta/`: Get project metadata.

### Health Check

- `GET /api/health/`: Check the health of the API.

## Example `curl` Requests

**Register a new user:**

```bash
cURL -X POST -H "Content-Type: application/json" -d '{"first_name": "john", "last_name": "doe", "email": "john@domain.com", "username": "testuser", "password": "testpassword", "re_password": "testpassword", "role": "user"}' /auth/users/
```

before you submit the form to create a user the email must be verified so make an api call to /api/send_otp/ (email) and /api/verify_otp/ (email and user otp)

**Login:**

```bash
curl -X POST -H "Content-Type: application/json" -d '{"email": "testuser@domain.com", "password": "testpassword"}' /auth/jwt/create/
```

**Create a new ticket:**

```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization: JWT <your_auth_token>" -d '{"title": "New Ticket", "description": "This is a new ticket."}' /api/tickets/
```

**List tickets:**

```bash
curl -X GET -H "Authorization: JWT <your_auth_token>" /api/tickets/
```

## Architecture Note

The project is built with Django and Django REST Framework. It follows a standard Django project structure with a core app for the custom user model and a tickets app for the ticketing system. The API is built using DRF's ModelViewSets for rapid CRUD development. The authentication is handled by djoser, which provides endpoints for registration and token-based authentication. The business logic is implemented in the views and models, with custom permissions for role-based access control. The project also includes features like rate limiting, idempotency, and a custom exception handler for a robust API.

## Implementation Notes

### Pagination

The API uses `LimitOffsetPagination` for all list endpoints. You can use the `limit` and `offset` query parameters to paginate through the results.

### Idempotency

The `POST /api/tickets/` endpoint supports an `Idempotency-Key` header. If a request with a previously seen key is received, the original successful response is returned without creating a new ticket.

### Rate Limiting

The API enforces a rate limit of 60 requests per minute per user. If the limit is exceeded, a `429 Too Many Requests` response is returned.

### Optimistic Locking

The API uses a `version` field on the `Ticket` model to implement optimistic locking. When a ticket is updated, the `version` number in the request is compared with the one in the database. If they do not match, the update is rejected with a `409 Conflict` status code.

### Role-Based Access Control

The API uses custom permission classes to enforce role-based access control:

- **User Role:** Can create new tickets. Can view and comment on ONLY their own tickets.
- **Agent Role:** Can do everything a User can, PLUS: view all tickets, assign any ticket to themselves, and change the status of any ticket, change priority of ticket.
- **Admin Role:** Can do everything an Agent can, PLUS: assign any ticket to any agent and delete any ticket or comment, change priority of ticket.

### Static File

The project is configured to serve a static JSON file at `/.well-known/hackathon.json`.
