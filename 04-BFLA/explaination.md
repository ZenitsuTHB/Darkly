# 1. Broken Function-Level Authorization — Internal API Documentation

## Severity

Medium

## Vulnerability Type

Broken Access Control / Missing Function-Level Authorization

## CWE

- CWE-862 — Missing Authorization
- CWE-285 — Improper Authorization

## Affected Endpoint

GET /api/docs-internal

## Description

The `/api/docs-internal` endpoint exposes internal API documentation
without enforcing the required staff-level authorization.

The application itself contains an internal comment stating:

> `/api/docs-internal still accessible without staff check — TODO fix in v1.4`

A low-privileged authenticated user with the `student` role can directly
request this endpoint and receive internal backend documentation.

The endpoint should enforce authorization based on the authenticated
user's role before returning its contents.

## Preconditions

- A valid authenticated session is required.
- The attacker only needs a low-privileged account such as `student`.

## Proof of Concept

Request:

GET /api/docs-internal HTTP/1.1
Host: localhost:4942
Cookie: session=<valid_student_session>

The server returns HTTP 200 instead of denying access.

Example response:

{
  "collections": {
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
      ],
      "note": "role writable via PATCH /api/profile"
    },
    "grades": {
      "fields": [
        "id",
        "student",
        "project",
        "score",
        "flag"
      ],
      "note": "flag field accessible via GET /api/grades?student={id}"
    }
  }
}

## Impact

A low-privileged user can access functionality intended for internal
staff users.

The exposed documentation reveals:

- internal API functionality;
- database collection structure;
- valid privilege levels;
- security-sensitive writable attributes;
- the endpoint used to retrieve student grades;
- the existence of the `flag` field.

This information significantly facilitates further attacks against
the application.

## Root Cause

The endpoint verifies that the requester has an authenticated session,
but does not perform the required server-side authorization check for
the user's role.

Authentication is therefore enforced, but authorization is not.

## Remediation

Implement server-side role-based authorization for `/api/docs-internal`.

The endpoint should return:

HTTP/1.1 403 Forbidden

for authenticated users who do not have the required staff privilege.

Authorization must be enforced on the server and must not rely on the
frontend hiding the endpoint.
