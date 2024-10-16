# Documentation for Auth Service on FastAPI

## Introduction

The Auth service is implemented using FastAPI and Docker. It provides functionality for user authentication and
authorization using JWT tokens signed with RSA. The service allows users to register, log in, and retrieve information
about the current user.

## Architecture

- **FastAPI**: Web framework for building APIs.
- **Docker**: Tool for containerizing the application.
- **JWT (JSON Web Tokens)**: Used for user authentication.
- **RSA**: Algorithm for signing JWT tokens.

## API Documentation

The API documentation can be accessed at `http://localhost:8001/auth/docs`.

## JWT

When a JWT token is generated upon user login, the payload includes the following fields:

```json
{
  "sub": "string",
  "username": "string"
}
```

The JWT token is included in the Authorization header of requests to protected endpoints in the following format:

`Authorization: Bearer <access_token>`