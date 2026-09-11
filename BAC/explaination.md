## Broken Access Control - Internal API Documentation

### Severity

Medium

### Vulnerability Type

Broken Access Control / Missing Authorization

### CWE

CWE-862 - Missing Authorization

### Affected Endpoint

GET /api/docs-internal

### Description

The `/api/docs-internal` endpoint is accessible to authenticated
users without verifying that the user has the required staff
privileges.

The endpoint is intended to be restricted to staff users, as indicated
by the application's internal comments, but a user with the `student`
role can access it successfully.

### Preconditions

An authenticated account is required.

The `jdoe` account has the following role:

student

### Proof of Concept

Request:

GET /api/docs-internal HTTP/1.1
Host: localhost:4942
Cookie: session=<jdoe_session>

The server returns the internal API documentation instead of
rejecting the request.

### Exposed Information

The endpoint reveals internal API information, including:

- writable fields of the users collection;
- valid role values;
- the fact that `role` is writable through `PATCH /api/profile`;
- the grades collection;
- the `flag` field;
- the endpoint used to retrieve grades.

Example:

{
  "users": {
    "writable_fields": [
      "first_name",
      "last_name",
      "campus",
      "avatar",
      "role"
    ],
    "role_values": [
      "visitor",
      "student",
      "cadet",
      "staff",
      "god"
    ]
  }
}

### Impact

A student-level user can access information intended for staff users.

The exposed documentation also reveals privileged functionality and
significantly facilitates further exploitation of the application.

### Root Cause

The endpoint does not perform an appropriate authorization check
against the authenticated user's role before returning internal
documentation.

### Remediation

Implement server-side authorization checks before serving the
endpoint.

For example, access should be granted only when the authenticated
user has an authorized staff role.

Authorization must be enforced server-side and must not rely on the
client interface or on the endpoint being difficult to discover.
