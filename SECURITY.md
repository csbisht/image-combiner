# Security Policy

## Supported Versions

| Version | Supported |
| ------- | --------- |
| 0.1.x   | Yes       |

## Reporting a Vulnerability

**Do not open a public GitHub issue for security vulnerabilities.**

Please report security issues by emailing **csbisht1@gmail.com** with the subject line `[image-combiner] Security Vulnerability`.

Include:
- A description of the vulnerability and its potential impact
- Steps to reproduce (a minimal example or proof-of-concept image/command)
- Any suggested fix, if you have one

You can expect an acknowledgement within **72 hours** and a resolution or status update within **14 days**.

## Scope

This project processes local image files using [Pillow](https://python-pillow.org/). Relevant security concerns include:

- **Malicious image files** — specially crafted images that trigger decompression bombs, excessive memory use, or parser bugs in Pillow
- **Path traversal** — output paths that escape an expected directory
- **Dependency vulnerabilities** — CVEs in Pillow or other dependencies

Out of scope:
- Denial-of-service via extremely large inputs on a local machine (no network surface)
- Issues in Python itself or the operating system

## Dependencies

Security fixes in [Pillow](https://github.com/python-pillow/Pillow/security) are tracked upstream. If a Pillow CVE affects this tool, `requirements.txt` and `pyproject.toml` will be updated promptly. Pin to the latest Pillow release to stay protected:

```
pip install --upgrade Pillow
```
