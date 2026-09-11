## Sensitive Information Disclosure - Forum

### Severity

Medium

### Location

localhost:4249/forum

### Vulnerability

Sensitive information about the authentication credentials of the
user `jdoe` is publicly exposed through forum posts.

### Evidence

The user `jdoe` publicly states that:

- the signup password was never changed;
- the password is short;
- the password is a common/dictionary word;
- the password is related to "rock".

Other users explicitly describe the account as a soft target.

### Impact

The exposed information significantly reduces the password search
space and facilitates a dictionary attack against the account.

### Exploitation

The information disclosed through the forum was used to identify
the weak password associated with the `jdoe` account.

Authentication was then successfully performed as:

jdoe@student.42.tech

### Result

An attacker can obtain an authenticated session belonging to another
user.

### Remediation

Do not expose authentication-related information through publicly
accessible resources.

Users should be prevented from using weak/common passwords and
passwords should be checked against compromised/common-password
lists.
