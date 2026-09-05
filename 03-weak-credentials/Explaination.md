# Weak Credentials leading to Account Takeover

## Vulnerability

Weak Credentials / Weak Authentication

## Affected Account

jdoe@student.42.tech

## Description

The `jdoe` account is protected by a short, predictable dictionary
password that was never changed from the initial signup password.

Publicly accessible forum content further discloses information about
the password, significantly reducing the password search space.

## Evidence

The forum contains several clues:

- `jdoe` states that the signup password was never changed.
- The password is described as short.
- The password is described as a classic dictionary word.
- Multiple references are made to "rock".
- Other users explicitly describe the account as a "soft target".

## Exploitation

Using the information disclosed by the application, the weak password
was identified and used to authenticate through:

POST /login

with:

jdoe@student.42.tech

The application returned:

HTTP/1.1 302 Found
Location: /

and issued an authenticated `session` cookie.

## Impact

Successful exploitation allows an unauthenticated attacker to
authenticate as another user.

In this case, the attacker obtained access to the `jdoe` account,
which has the `student` role.

This constitutes an account takeover resulting from weak credentials.

## Attack Chain

Public Information Disclosure
        ↓
Password Hints
        ↓
Weak Credentials
        ↓
Authentication
        ↓
Account Takeover
        ↓
Authenticated Student Session

## Root Cause

The application permits a weak, dictionary-based password to protect
a user account and does not adequately prevent the use of predictable
credentials.

The application also exposes password-related information through a
public forum.

## Remediation

- Enforce strong password requirements.
- Reject common and dictionary passwords.
- Check passwords against breached-password databases.
- Require users to change insecure initial passwords.
- Avoid exposing password-related information publicly.
- Implement rate limiting and brute-force protection.
- Monitor unusual authentication attempts.
