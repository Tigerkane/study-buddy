# Security Policy

## Supported Versions

| Version | Supported |
|---|---|
| latest (main) | ✅ |

## Reporting a Vulnerability

If you find a security issue, please **do not** open a public GitLab issue.

Instead, contact the maintainer directly:
- GitLab: @Saichaitanya9

We will respond within 48 hours and patch critical issues within 7 days.

## Security Notes

- This app runs **entirely locally** — no data is sent to external servers
- PDF content is processed in memory and never stored to disk
- Ollama runs on localhost — no external AI API calls
- No user authentication or sensitive data is collected
- No `.env` file with secrets is required
