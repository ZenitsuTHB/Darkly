# Darkly

## Stored Cross-Site Scripting (Stored XSS)

### Vulnerability

The feedback/guestbook page stores user-controlled input and later
renders it directly into the HTML response without proper output
encoding or sanitization.

The application therefore allows an attacker to inject HTML/JavaScript
that is stored on the server and executed when the page is viewed.

### Root Cause

User input from:

- `txtName`
- `mtxtMessage`

is stored and subsequently inserted into the HTML without contextual
output encoding.

The `maxlength` attributes only provide client-side validation and can
be bypassed by modifying the HTTP request.

### Proof of Concept

A malicious HTML payload can be submitted through the feedback form.
When the stored entry is rendered again, the browser interprets the
injected markup and executes JavaScript.

This confirms a Stored XSS vulnerability.

### Impact

An attacker could potentially execute JavaScript in the security
context of the vulnerable application when another user views the
affected page.

Depending on the application's authentication and browser security
controls, this could lead to actions being performed on behalf of the
victim, modification of page content, or exposure of accessible data.

### Mitigation

- Perform server-side input validation.
- Apply contextual HTML output encoding.
- Do not insert untrusted data using unsafe HTML rendering.
- Sanitize HTML if HTML input is genuinely required.
- Enforce server-side length limits.
- Deploy an appropriate Content Security Policy.
