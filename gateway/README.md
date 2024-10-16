# Documentation for Gateway Service

## Introduction

The Gateway service acts as a reverse proxy, routing requests to the appropriate backend services, specifically the Auth
service and the Catalog service. It is configured using Nginx and provides basic request handling, including token
validation for protected endpoints.

## Token Validation

Requests to the `/api/` path require a valid JWT token. The token is validated by the Auth service through the internal
`_check_token` endpoint. If the token is invalid or missing, the request will be rejected.

The JWT token should be included in the Authorization header of requests made to the /api/ endpoints in the following
format:

`Authorization: Bearer <access_token>`