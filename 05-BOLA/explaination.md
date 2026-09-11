# 2. Broken Object Level Authorization (BOLA) / IDOR — Student Grades

## Severity

High

## Vulnerability Type

Broken Access Control / Broken Object Level Authorization (BOLA) /
Insecure Direct Object Reference (IDOR)

## CWE

- CWE-639 — Authorization Bypass Through User-Controlled Key
- CWE-284 — Improper Access Control

## Affected Endpoint

GET /api/grades?student={id}

## Description

The `/api/grades` endpoint does not properly enforce authorization on
the student object specified by the `student` parameter.

A low-privileged authenticated student can modify the `student`
identifier and retrieve academic records belonging to another student.

The server appears to trust the user-supplied identifier without
verifying that it corresponds to the authenticated user or that the
requester has sufficient privileges to access the target student's
records.

## Preconditions

- A valid authenticated student session is required.
- A valid student identifier is required.

## Proof of Concept

The authenticated session belongs to:

Username: jdoe

Role: student

Session subject: z4p1cnx47mfy50f

The attacker then requests a different student identifier:

GET /api/grades?student=8l16vboi47dmand HTTP/1.1
Host: localhost:4942
Cookie: session=<valid_jdoe_session>

The server returns HTTP 200 and provides records belonging to:

8l16vboi47dmand

Example response:

[
  {
    "collectionName": "grades",
    "score": 92,
    "student": "8l16vboi47dmand",
    "project": "wl8jjufomev59ha",
    "flag": ""
  },
  {
    "collectionName": "grades",
    "score": 0,
    "student": "8l16vboi47dmand",
    "project": "i9bnu5ze2u87g5m",
    "flag": ""
  }
]

The authenticated user is not the owner of these records.

## Expected Behavior

A student requesting another student's grades should receive:

HTTP/1.1 403 Forbidden

or an equivalent authorization error.

## Actual Behavior

The application returns:

HTTP/1.1 200 OK

and exposes the requested student's academic records.

## Impact

A low-privileged student can access academic information belonging to
other students.

The exposed information includes:

- student identifiers;
- project participation;
- project information;
- grades/scores;
- potentially project flags.

The internal API documentation also explicitly identifies the `flag`
field as accessible through this endpoint, increasing the potential
impact of the authorization failure.

## Root Cause

The authorization decision is not bound to the authenticated user's
identity.

The server accepts the user-controlled `student` identifier and
retrieves the corresponding records without verifying that the
requester is authorized to access that student object.

## Remediation

For student users, restrict the query to the authenticated user's own
student identifier.

For example:

- compare `request.student` with the authenticated user's ID;
- reject mismatches with HTTP 403;
- allow cross-student access only to explicitly authorized staff roles.

Authorization must be performed server-side before querying the
database.
