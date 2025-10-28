# 🔐 Secure Setup Guide - Born2Sub.x Access Only

**Author:** Cyrus Makai Schoonover  
**Repository:** https://github.com/CashMasterStone/I_Am_Trying  
**Authorized Access:** CashMasterStone (GitHub) | Born2Sub.x (Web3)

## Overview

This repository and all its services are configured for **restricted access only**:
- **GitHub:** CashMasterStone account only
- **Web3:** Born2Sub.x wallet only
- **Browser:** Brave Browser recommended for Web3 wallet integration

## Initial Setup

### 1. GitHub Repository Security

Configure your repository on GitHub:

```bash
# Settings → General → Visibility
✓ Make repository Private

# Settings → Branches → Branch protection rules for "Zenith"
✓ Require pull request reviews before merging
✓ Require status checks to pass
✓ Require signed commits
✓ Include administrators

# Settings → Security → Signing
✓ Enable GPG commit signature verification
✓ Enable vigilant mode
```

### 2. Environment Variables Setup

Create `.env` file in repository root (NEVER commit this):

```bash
# Copy the template
cp .env.example .env

# Edit with your actual values
nano .env
```

Required environment variables:

```bash
# Flask Secret (generate new one)
FLASK_SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")

# Your Born2Sub.x wallet address (lowercase)
AUTHORIZED_WALLET=0xyourborn2subwalletaddresshere

# GitHub token for API operations (create at: https://github.com/settings/tokens)
GITHUB_TOKEN=ghp_yourpersonalaccesstokenhere

# Optional: Ngrok for secure tunneling on public WiFi
NGROK_AUTH_TOKEN=your_ngrok_token_here
```

### 3. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Optional: For Web3 signature verification
pip install web3 eth-account
```

### 4. Configure Born2Sub.x Wallet

In Brave Browser:

1. **Install/Enable Web3 Wallet:**
   - Brave Browser has built-in crypto wallet
   - Or use MetaMask/WalletConnect
   - Ensure Born2Sub.x ENS/wallet is configured

2. **Get Your Wallet Address:**
   ```javascript
   // In Brave console (F12)
   ethereum.request({ method: 'eth_requestAccounts' })
   // Copy the address and add to .env as AUTHORIZED_WALLET
   ```

3. **Add to .env:**
   ```bash
   AUTHORIZED_WALLET=0xyouraddress  # lowercase
   ```

## Running Services Securely on Public WiFi

### Option 1: Local Network Only (Most Secure)

```bash
# Run server on localhost only
python3 scripts/upload_server.py --host 127.0.0.1 --port 8000

# Access from same device only
# Open: http://localhost:8000
```

### Option 2: Ngrok Secure Tunnel (Recommended for Phone Access)

```bash
# Terminal 1: Start upload server
python3 scripts/upload_server.py --host 127.0.0.1 --port 8000

# Terminal 2: Start ngrok tunnel with password
ngrok http 8000 --basic-auth "cashmasterstone:$(openssl rand -base64 32)"

# Ngrok will display:
# Forwarding: https://random-id.ngrok.io -> http://localhost:8000
# Copy this URL to your phone's Brave Browser
```

### Option 3: VPN + Local Network

```bash
# 1. Connect both devices to VPN
# 2. Find dev container IP
ip addr show

# 3. Run server
python3 scripts/upload_server.py --host 0.0.0.0 --port 8000

# 4. Access from phone (on same VPN)
# http://<container-ip>:8000
```

## Using the Upload Server

### From Your Phone (Brave Browser)

1. **Connect to Service:**
   - Open the ngrok URL or local IP in Brave
   - You'll see the "Web3 Wallet Authentication" screen

2. **Authenticate:**
   - Click "Connect Wallet"
   - Brave will prompt you to connect Born2Sub.x wallet
   - Sign the authentication message
   - Server validates your wallet address matches AUTHORIZED_WALLET

3. **Upload Files:**
   - Once authenticated, upload interface appears
   - Select files or directories
   - Upload button sends files to workspace

4. **Security:**
   - Only Born2Sub.x wallet can authenticate
   - All uploads logged with wallet address
   - Sessions expire after 1 hour

## Verifying Access Control

### Test Authentication

```bash
# Should fail (no auth)
curl http://localhost:8000/upload

# Should return 401/403 Unauthorized
```

### Check Audit Logs

```bash
# Server prints upload logs
[UPLOAD] 0xyourwallet uploaded: photo.jpg
[UPLOAD] 0xyourwallet uploaded: folder/document.pdf
```

### Verify Wallet Restriction

```python
# In scripts/upload_server.py, verify:
AUTHORIZED_WALLET = os.environ.get('AUTHORIZED_WALLET', '').lower()

# Only this wallet address can authenticate
```

## Security Checklist

Before using on public WiFi:

- [ ] `.env` file created with secrets (not committed)
- [ ] `AUTHORIZED_WALLET` set to Born2Sub.x address
- [ ] `FLASK_SECRET_KEY` generated and set
- [ ] Repository is private on GitHub
- [ ] Using ngrok with password OR VPN
- [ ] Brave Browser on phone with wallet configured
- [ ] TLS/HTTPS enabled (ngrok provides this)
- [ ] `.gitignore` prevents committing secrets
- [ ] GPG commit signing enabled

## Troubleshooting

### "No Web3 wallet detected"
- Use Brave Browser (has built-in wallet)
- Or install MetaMask extension
- Enable wallet in browser settings

### "Authentication failed"
- Check `.env` has correct `AUTHORIZED_WALLET` address
- Ensure address is lowercase
- Verify you're using Born2Sub.x wallet to sign
- Check server logs for details

### "Can't connect from phone"
- On public WiFi, use ngrok tunnel
- Check firewall allows connections
- Verify ngrok URL is HTTPS (secure)
- Ensure phone and server both online

### "Upload fails"
- Check authentication completed successfully
- Verify files not too large (100MB default limit)
- Check server logs for errors
- Ensure `uploads/` directory writable

## File Structure

```
I_Am_Trying/
├── .env                    # Your secrets (NEVER commit)
├── .env.example            # Template for .env
├── .gitignore             # Prevents committing secrets
├── .github/
│   ├── ACCESS_CONTROL.md  # Access policy
│   ├── SECURITY.md        # Security policy
│   └── copilot-instructions.md
├── scripts/
│   ├── upload_server.py   # Web3-authenticated upload server
│   └── build_lexeme_encyclopedia.py
├── uploads/               # Uploaded files (gitignored)
└── requirements.txt       # Python dependencies
```

## License & Ownership

All code and content in this repository:
- **Owner:** Cyrus Makai Schoonover
- **GitHub:** CashMasterStone
- **License:** RTPL (Restricted Truth Preservation License)
- **Web3 Identity:** Born2Sub.x

No unauthorized access permitted. See `LICENSE.md` and `.github/SECURITY.md`.

---

**Questions or Issues?**  
Contact: CashMasterStone on GitHub  
Web3: Born2Sub.x
