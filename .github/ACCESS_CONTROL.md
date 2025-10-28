# Repository Access Control Policy

**Author:** Cyrus Makai Schoonover  
**Repository:** https://github.com/CashMasterStone/I_Am_Trying  
**License:** See LICENSE.md in repository root

## Authorized Access Only

This repository and all its contents are restricted to:

1. **GitHub Account:** CashMasterStone
2. **Web3 Identity:** Born2Sub.x (ENS/wallet-based authentication)

## Access Methods

### GitHub Access
- Only the repository owner (CashMasterStone) has write access
- Repository is private or access is restricted via GitHub settings
- All commits must be signed and verified

### Web3/Crypto Wallet Access
- Primary wallet: Born2Sub.x
- All web services require wallet signature authentication
- No anonymous or public access permitted

## Security Requirements

### For All Services
- No hardcoded credentials
- Environment-based secrets only
- Signature-based authentication required
- IP whitelisting when possible
- TLS/HTTPS only for external access

### For Upload Server
- Wallet signature required before upload
- Only Born2Sub.x wallet authorized
- Session tokens expire after 1 hour
- File uploads logged with wallet address

### For API Access
- Bearer token or wallet signature required
- Rate limiting per wallet address
- Audit logging of all access attempts

## Violation Response

Unauthorized access attempts will result in:
- Immediate connection termination
- IP blocking
- Audit log entry
- Alert to repository owner

## Compliance

This access control policy aligns with:
- RTPL (Restricted Truth Preservation License)
- LLW/LLWΦ provenance and auditability requirements
- DEVICE_ATTEST and cryptographic witness principles

---

**Last Updated:** October 28, 2025  
**Policy Owner:** Cyrus Makai Schoonover
