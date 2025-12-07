# Security Policy

## 🚨 CRITICAL SECURITY INCIDENT - API Key Exposure (2025-12-07)

### Incident Summary

A Google API key was accidentally committed to Git history in commit `2cc60bc` on 2025-12-07 11:42:43.

**Exposed Key**: `AIzaSyACJ-5a5KaFR1F0JCl6um-XhGyNKsojTSw`

### Remediation Actions Taken

✅ **Completed**:
1. Removed API key from all working directory files (3 markdown files)
2. Cleaned Git history using `git-filter-repo`
3. Force pushed cleaned history to GitHub
4. Verified API key completely removed from Git history

⚠️ **USER ACTION REQUIRED**:
1. **REVOKE THE EXPOSED API KEY IMMEDIATELY** at Google Cloud Console
   - Go to: https://console.cloud.google.com/apis/credentials
   - Find key: `AIzaSyACJ-5a5KaFR1F0JCl6um-XhGyNKsojTSw`
   - Click "Delete" or "Restrict"
2. Generate a new API key
3. Add new key to `.env` file (already in `.gitignore`)
4. Test with new key

### Files That Contained the Exposed Key

- `API-TEST-RESULTS.md` (2 instances)
- `COMPLETE-MARS-EVALUATION.md` (3 instances)
- `DEPENDENCY-ANALYSIS.md` (1 instance)

All instances replaced with `<GOOGLE_API_KEY_REDACTED>` placeholder.

### Timeline

| Time | Action |
|------|--------|
| 2025-12-07 11:42 | API key accidentally committed in `2cc60bc` |
| 2025-12-07 14:45 | Security issue detected |
| 2025-12-07 14:46 | Removed from working directory files |
| 2025-12-07 14:47 | Cleaned Git history with `git-filter-repo` |
| 2025-12-07 14:48 | Force pushed cleaned history to GitHub |
| 2025-12-07 14:48 | Verified API key completely removed |

---

## API Key Management Best Practices

### ✅ DO

1. **Use Environment Variables**
   ```bash
   # .env (NEVER commit this file)
   GOOGLE_API_KEY=your_api_key_here
   NANOBANANA_API_KEY=your_api_key_here
   ```

2. **Add .env to .gitignore**
   ```gitignore
   # .gitignore (already configured)
   .env
   .env.local
   .env.*.local
   *.key
   *.pem
   secrets/
   ```

3. **Use .env.example for Documentation**
   ```bash
   # .env.example (safe to commit)
   GOOGLE_API_KEY=your_google_api_key_here
   NANOBANANA_API_KEY=same_as_google_api_key
   ```

4. **Load Environment Variables in Code**
   ```python
   import os
   from dotenv import load_dotenv

   load_dotenv()  # Load from .env file
   api_key = os.getenv("GOOGLE_API_KEY")

   if not api_key:
       raise ValueError("GOOGLE_API_KEY not set")
   ```

5. **Use Secret Management for Production**
   - Google Cloud Secret Manager
   - AWS Secrets Manager
   - HashiCorp Vault
   - GitHub Secrets (for CI/CD)

### ❌ DON'T

1. **Never hardcode API keys in source code**
   ```python
   # ❌ WRONG
   api_key = "AIzaSyACJ-5a5KaFR1F0JCl6um-XhGyNKsojTSw"

   # ✅ RIGHT
   api_key = os.getenv("GOOGLE_API_KEY")
   ```

2. **Never commit API keys to Git**
   - Not in code files
   - Not in documentation
   - Not in commit messages
   - Not in test files

3. **Never log API keys**
   ```python
   # ❌ WRONG
   print(f"Using API key: {api_key}")
   logger.info(f"API key: {api_key}")

   # ✅ RIGHT
   logger.info("API key loaded successfully")
   logger.debug(f"API key length: {len(api_key)}")
   ```

4. **Never share API keys**
   - Don't send via email
   - Don't post in Slack/Discord
   - Don't include in screenshots
   - Don't share in documentation

---

## API Key Rotation Policy

### When to Rotate

Rotate API keys immediately if:
1. ✅ Key was committed to Git (this incident)
2. Key was accidentally shared publicly
3. Key was used in insecure context
4. Suspicious activity detected
5. Employee with key access leaves

### Rotation Process

1. **Generate New Key**
   - Go to Google Cloud Console → APIs & Credentials
   - Create new API key
   - Apply same restrictions as old key

2. **Update Environment**
   ```bash
   # Update .env file
   GOOGLE_API_KEY=new_key_here

   # Test new key
   python -c "import os; from gemini_client import GeminiClient; print('✅ New key works')"
   ```

3. **Deploy to Production**
   - Update Cloud Run environment variables
   - Update GitHub Secrets (if used in CI/CD)
   - Update any other deployment targets

4. **Revoke Old Key**
   - Wait 24 hours for all services to use new key
   - Delete old key from Google Cloud Console
   - Document rotation in change log

5. **Verify**
   - Check logs for any failed authentications
   - Monitor for unauthorized usage
   - Confirm old key no longer works

---

## Cloud Run Security

### Environment Variables

**Set API key in Cloud Run**:
```bash
gcloud run deploy nanobanana \
  --set-env-vars GOOGLE_API_KEY=your_new_key_here \
  --set-env-vars NANOBANANA_API_KEY=your_new_key_here
```

**Or use Secret Manager** (recommended):
```bash
# Create secret
gcloud secrets create google-api-key --data-file=- <<< "your_new_key_here"

# Deploy with secret
gcloud run deploy nanobanana \
  --set-secrets=GOOGLE_API_KEY=google-api-key:latest
```

### API Key Restrictions

**Configure in Google Cloud Console**:
1. **Application restrictions**:
   - HTTP referrers (for web apps)
   - IP addresses (for Cloud Run)
   - None (if using other authentication)

2. **API restrictions**:
   - Restrict to: Generative Language API
   - Don't allow access to all APIs

3. **Usage quotas**:
   - Set daily quota limits
   - Enable billing alerts
   - Monitor usage regularly

---

## Incident Response Plan

### If API Key is Exposed

**Immediate Actions** (within 1 hour):
1. ⚠️ **REVOKE THE KEY IMMEDIATELY**
2. Generate new API key
3. Update all services with new key
4. Remove key from Git history (if committed)
5. Force push cleaned history

**Investigation** (within 24 hours):
1. Check API usage logs for unauthorized requests
2. Identify how key was exposed
3. Determine potential impact
4. Document timeline

**Prevention** (within 1 week):
1. Implement pre-commit hooks to detect secrets
2. Add secret scanning to CI/CD pipeline
3. Review access controls
4. Update team training
5. Document lessons learned

### Detection Tools

**Pre-commit hooks**:
```bash
# Install pre-commit
pip install pre-commit

# Add .pre-commit-config.yaml
detect-secrets:
  - id: detect-secrets
    args: ['--baseline', '.secrets.baseline']
```

**GitHub Secret Scanning**:
- Enable in repository settings
- Automatically detects committed secrets
- Sends alerts to repository admins

**CI/CD Scanning**:
```yaml
# .github/workflows/security.yml
- name: Scan for secrets
  uses: trufflesecurity/trufflehog@main
  with:
    path: ./
    base: main
    head: HEAD
```

---

##Reporting Security Issues

If you discover a security vulnerability, please email:
- **Email**: manutej@gmail.com
- **Subject**: [SECURITY] NanoBanana Security Issue

**DO NOT** create a public GitHub issue for security vulnerabilities.

---

## Security Checklist

### Development
- [ ] Never hardcode secrets in code
- [ ] Use `.env` for local development
- [ ] Keep `.env` in `.gitignore`
- [ ] Use `os.getenv()` to load secrets
- [ ] Never log full API keys

### Production
- [ ] Use Cloud Run secrets or Secret Manager
- [ ] Restrict API keys by IP/referrer
- [ ] Enable API key restrictions
- [ ] Set usage quotas
- [ ] Monitor API usage
- [ ] Rotate keys quarterly

### CI/CD
- [ ] Use GitHub Secrets for workflows
- [ ] Never echo secrets in logs
- [ ] Scan for secrets in PRs
- [ ] Use short-lived credentials
- [ ] Audit secret access

---

**Last Updated**: 2025-12-07
**Incident Status**: ⚠️ **ACTIVE - USER ACTION REQUIRED TO REVOKE KEY**
