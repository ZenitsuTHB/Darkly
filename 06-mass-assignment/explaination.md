# 3. Mass Assignment Leading to Vertical Privilege Escalation

## Severity

High

## Vulnerability Type

Mass Assignment / Broken Access Control / Vertical Privilege Escalation

## CWE

- CWE-915 — Improperly Controlled Modification of Dynamically-Determined
  Object Attributes
- CWE-862 — Missing Authorization

## Affected Endpoint

PATCH /api/profile

## Description

The `/api/profile` endpoint allows an authenticated user to submit
security-sensitive profile attributes that should be controlled by the
sercadet.

The internal API documentation explicitly identifies `role` as a
writable field:

"role writable via PATCH /api/profile"

However, the authenticated user's role is a security-sensitive
attribute and should not be freely controlled by the user themselves.

During testing, a user authenticated as `student` was able to submit
a request attempting to modify the `role` attribute. The server
processed the request and changed the user's role from `student` to
`cadet`.

This results in a vertical privilege escalation.

## Preconditions

- A valid authenticated student session is required.

## Initial State

The authenticated account initially had:

role = student

## Proof of Concept

Request:

PATCH /api/profile HTTP/1.1
Host: localhost:4942
Content-Type: application/json
Cookie: session=<valid_student_session>

{
  "role": "cadet",
  "last_name": "test",
  "first_name": "tesy",
  "campus": "here",
  "avatar": "avatar.png",
  "level": 70
}

The server responds with HTTP 200 OK and the resulting account state
contains:

{
  "first_name": "tesy",
  "last_name": "test",
  "campus": "here",
  "level": 70,
  "role": "cadet"
}

The important security property is that the original role: student

was changed to: cadet

without requiring authorization from a higher-privileged user.

## Demonstrated Privilege Escalation

Before: student

After:  cadet

Therefore: student → cadet

has been successfully demonstrated.

The application appears to prevent direct assignment to higher roles
such as `staff` or `god`, but the endpoint nevertheless allows a
low-privileged user to modify their own authorization level.

## Additional Observation

The same request also successfully modified the `level` attribute:

level = 70

This indicates that the endpoint does not sufficiently distinguish
between ordinary user-editable profile data and security-sensitive
server-controlled attributes.

## Impact

A low-privileged student can increase their authorization level by
modifying the `role` attribute.

Depending on the permissions associated with the `cadet` role, this
may provide access to functionality that is not intended to be
available to students.

The ability to modify authorization attributes also creates a
privilege-boundary violation and may facilitate further privilege
escalation if additional authorization checks rely on the modified
role.

## Root Cause

The profile update endpoint permits the client to submit the `role`
attribute and does not enforce sufficient authorization before applying
the change.

Security-sensitive attributes such as `role` and `level` should not be
controlled by a self-service profile update endpoint.

## Remediation

1. Create a strict allowlist of fields that ordinary users are allowed
   to modify.

2. Remove `role`, `level`, `id`, and other security-sensitive fields
   from the student profile update schema.

3. Only privileged administrative endpoints should be capable of
   modifying authorization attributes.

4. Enforce authorization server-side before changing a user's role.

5. Reject unauthorized attributes with HTTP 400 or 403 rather than
   silently processing them.

## Expected Behavior

A student attempting to modify their own role should receive:

HTTP/1.1 403 Forbidden

and their role should remain: student

## Actual Behavior

The student can submit the `role` parameter and the account is
successfully changed from:

student → cadet
