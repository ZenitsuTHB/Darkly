## Reflected XSS - Newsletter

### Severity

Medium / High

### Endpoint

GET /newsletter

### Parameter

email

### Vulnerability

The `email` parameter is reflected into the application's response
without appropriate output encoding.

### Proof of Concept

Payload:

<script>alert('XSS')</script>

URL/request:

GET /newsletter?email=<PAYLOAD>&msg=subscribed

### Result

The injected JavaScript is executed by the browser.

### Impact

An attacker may be able to execute arbitrary JavaScript in the
context of the victim's browser.

Depending on the application's functionality, this could allow
access to DOM data, actions available to the victim, or session
information.

### Root Cause

User-controlled input is inserted into an HTML context without
proper context-aware output encoding.

### Remediation

Apply context-aware output encoding before inserting user-controlled
data into HTML. Prefer safe templating mechanisms and avoid
dangerous HTML sinks.

### Evidence

See screenshots/01-payload.png
See screenshots/02-execution.png
