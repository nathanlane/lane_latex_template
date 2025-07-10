# Security Policy

## Reporting Security Issues

If you discover a security vulnerability, please email the maintainer directly instead of creating a public issue.

## API Keys and Secrets

This repository uses environment variables for API keys. These should NEVER be committed to version control.

### Setup
1. Copy `.env.example` to `.env`
2. Add your API keys to `.env`
3. Ensure `.env` is listed in `.gitignore`

### If You Accidentally Commit Secrets

If you accidentally commit sensitive data:

1. **Immediately revoke the exposed credentials**
2. Generate new credentials
3. Consider using `git filter-branch` or BFG Repo-Cleaner to remove from history
4. If the repository is public, assume the credentials are compromised

### Prevention

- Use `.env` files for local development
- Always check `git status` before committing
- Consider using pre-commit hooks to scan for secrets
- Use GitHub Secrets for GitHub Actions

## Supported Versions

Currently supporting the latest version only.

## Security Best Practices

- Keep your LaTeX distribution updated
- Don't run untrusted LaTeX code (it can execute shell commands)
- Be cautious with `\write18` and shell-escape features
- Review any third-party packages before use