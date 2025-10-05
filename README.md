# HelpDesk Mini API

This is a Django REST Framework project for a mini help desk ticketing system.

## API Endpoints

### Authentication

*   `POST /api/register/`: Create a new user.
*   `POST /api/login/`: Get an auth token.

### Tickets

*   `GET /api/tickets/`: List all tickets.
    *   Filtering: `?status=...`, `?priority=...`, `?assigned_to=...`
    *   Searching: `?search=...` (searches `title`, `description`, and latest `comment`)
    *   Pagination: `?limit=...`, `?offset=...`
*   `POST /api/tickets/`: Create a new ticket.
*   `GET /api/tickets/<int:id>/`: Retrieve a single ticket.
*   `PATCH /api/tickets/<int:id>/`: Update a ticket.
*   `DELETE /api/tickets/<int:id>/`: Delete a ticket (admin only).

### Comments

*   `POST /api/tickets/<int:id>/comments/`: Create a new comment for a ticket.

### Health Check

*   `GET /api/health/`: Check the health of the API.

## Example `curl` Requests

**Register a new user:**

```bash
curl -X POST -H "Content-Type: application/json" -d '{"username": "testuser", "password": "testpassword", "role": "user"}' http://127.0.0.1:8000/api/register/
```

**Login:**

```bash
curl -X POST -H "Content-Type: application/json" -d '{"username": "testuser", "password": "testpassword"}' http://127.0.0.1:8000/api/login/
```

**Create a new ticket:**

```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization: Token <your_auth_token>" -d '{"title": "New Ticket", "description": "This is a new ticket."}' http://127.0.0.1:8000/api/tickets/
```

**List tickets:**

```bash
curl -X GET -H "Authorization: Token <your_auth_token>" http://127.0.0.1:8000/api/tickets/
```

## Test Users

*   **user:**
    *   username: `user`
    *   password: `password`
*   **agent:**
    *   username: `agent`
    *   password: `password`
*   **admin:**
    *   username: `admin`
    *   password: `password`
