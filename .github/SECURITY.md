# Security Policy

**Author:** Cyrus Makai Schoonover  
**Repository:** https://github.com/CashMasterStone/I_Am_Trying  
**Authorized Access:** CashMasterStone (GitHub) | Born2Sub.x (Web3)

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

## Reporting Security Issues

If you discover a security vulnerability:

1. **DO NOT** open a public issue
2. Contact: CashMasterStone via GitHub private message
3. Or: Use Web3 encrypted message to Born2Sub.x
4. Include detailed description and reproduction steps

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
