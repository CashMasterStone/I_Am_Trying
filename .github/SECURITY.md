# Security Policy

**Author:** Cyrus Makai Schoonover  
**Repository:** https://github.com/CashMasterStone/I_Am_Trying  
**Authorized Access:** CashMasterStone (GitHub) | Born2Sub.x (Web3)

## ⚠️ CRITICAL: Device Security

**NEVER enter credentials on untrusted/borrowed devices:**
- Friend's laptops or computers
- Public computers (libraries, cafes, etc.)
- Shared workstations
- Any device you don't own and control

**ONLY use credentials on:**
- Your personal phone (with Born2Sub.x wallet)
- Your personal laptop/desktop
- Devices you own with full disk encryption
- Secure, isolated environments you control

## Authorized Identities

### GitHub
- **Account:** CashMasterStone
- **Profile:** https://github.com/CashMasterStone
- All commits must be signed with verified GPG key

### Web3/Crypto
- **ENS/Primary Wallet:** Born2Sub.x
- Signature verification required for all web service access
- Only this wallet address may authenticate to repository services

## Access Restrictions

### Repository Level
- Private repository - no public access
- Collaborator access requires explicit approval from CashMasterStone
- All pull requests require owner review and approval
- Branch protection enabled on main/Zenith branches

### Service Level
- Upload server: Born2Sub.x wallet signature required
- API endpoints: Authentication token or wallet signature
- Local development: Environment variables for secrets
- No hardcoded credentials anywhere in codebase

### Network Level
- Public WiFi: Use VPN or secure tunnel (ngrok with password)
- Brave Browser: Web3 wallet integration enabled
- TLS/HTTPS required for all external connections
- CORS restricted to authorized origins only

## Untrusted Device Protocol

If you must access this repository from an untrusted device:

### ✅ SAFE Operations:
- View public documentation (read-only)
- Review code and architecture
- Take temporary notes (in `/tmp/` only)
- Plan future work

### ❌ NEVER Do This:
- Enter wallet private keys or seed phrases
- Save GitHub credentials in browser
- Create `.env` files with real secrets
- Push commits containing sensitive data
- Enter passwords or tokens
- Clone to persistent storage on device

### 🧹 Before Leaving Device:
```bash
# Run cleanup script
bash /tmp/cleanup_session.sh

# Manually:
# 1. Sign out of GitHub
# 2. Clear browser history/cache/cookies
# 3. Close all terminals
# 4. Delete any cloned repos
# 5. Clear clipboard
```

## Reporting Security Issues

If you discover a security vulnerability:

1. **DO NOT** open a public issue
2. Contact: CashMasterStone via GitHub private message (from secure device only)
3. Or: Use Web3 encrypted message to Born2Sub.x
4. Include detailed description and reproduction steps
5. **NEVER** report from compromised or untrusted devices

## Security Best Practices

### For Development
- Use `.env` files for local secrets (never commit)
- Rotate tokens and keys regularly
- Enable 2FA on GitHub account
- Sign all commits with GPG key
- Review dependencies for vulnerabilities

### For Deployment
- Use environment variables for production secrets
- Enable audit logging on all services
- Implement rate limiting
- Use fail2ban or similar for intrusion prevention
- Regular security updates and patches

### For Web3 Services
- Verify wallet signatures server-side
- Implement nonce-based replay protection
- Time-bound authentication tokens
- Log all wallet authentication attempts
- Whitelist only Born2Sub.x wallet address

## Cryptographic Standards

Per LLW/LLWΦ architecture requirements:
- Deterministic hashing (NORMALFORMHASH)
- Merkle tree provenance
- Device attestation (DEVICE_ATTEST)
- Threshold signatures (TSS_PARTIAL, TSS_COMBINE)
- Quorum-based authorization where applicable

## Compliance

This security policy enforces:
- Restricted Truth Preservation License (RTPL)
- Single-owner access control
- Cryptographic auditability
- Provenance chain integrity

---

**Security Contact:** CashMasterStone  
**Last Updated:** October 28, 2025
