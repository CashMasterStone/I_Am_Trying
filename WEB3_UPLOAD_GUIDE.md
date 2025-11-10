# Web3 Upload Server Guide

**Author:** Cyrus Makai Schoonover  
**Repository:** https://github.com/CashMasterStone/I_Am_Trying  
**License:** See LICENSE.md in repository root

## Secure File Upload with Born2Sub.x Wallet Authentication

This guide explains how to securely upload files from your phone (Brave Browser) to your workspace using Web3 wallet authentication, safe for use on public WiFi.

## 🔐 Security Features

- **Web3 Wallet Authentication**: Only your Born2Sub.x wallet can upload files
- **Cryptographic Signature Verification**: Each session requires a signed message
- **No Hardcoded Secrets**: All sensitive data is environment-based or generated
- **HTTPS Tunnel Support**: Use ngrok for encrypted connections on public WiFi
- **Path Traversal Protection**: Prevents malicious file paths
- **Session-Based Access**: Authentication persists during your session

## 📱 Setup for Phone Upload (Public WiFi)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs Flask, Web3, and eth-account for wallet authentication.

### 2. Start the Upload Server with Wallet Authentication

```bash
python3 scripts/upload_server.py --wallet-auth --port 8000
```

**Optional**: Restrict to your specific wallet address:

```bash
export AUTHORIZED_WALLET=0xYourWalletAddressHere
python3 scripts/upload_server.py --wallet-auth --port 8000
```

Or use the flag directly:

```bash
python3 scripts/upload_server.py --wallet-auth --authorized-wallet 0xYourWalletAddressHere --port 8000
```

### 3. Create Secure HTTPS Tunnel (Required for Public WiFi)

In a new terminal:

```bash
ngrok http 8000
```

You'll see output like:
```
Forwarding   https://abc123.ngrok.io -> http://localhost:8000
```

**Use the HTTPS URL** (abc123.ngrok.io) on your phone.

### 4. Access from Brave Browser on Phone

1. Open Brave Browser on your phone
2. Navigate to the ngrok HTTPS URL (e.g., `https://abc123.ngrok.io`)
3. Click **"Connect Wallet"**
4. Select your **Born2Sub.x** wallet
5. **Sign the authentication message** (proves you own the wallet)
6. Once authenticated, you can upload files or directories

### 5. Upload Files

- **Single files**: Choose files from your phone
- **Directories** (Chrome/Brave on Android): Select a folder to preserve structure
- Files are saved to `uploads/` in the repository

## 🔧 Command Line Options

```bash
python3 scripts/upload_server.py --help
```

Available options:
- `--host HOST` - Host to bind (default: 0.0.0.0)
- `--port PORT` - Port to listen on (default: 8000)
- `--wallet-auth` - Enable Web3 wallet authentication
- `--authorized-wallet ADDRESS` - Specific wallet address to authorize

## 🛡️ Security Best Practices

### On Public WiFi:
1. ✅ **Always use `--wallet-auth`** flag
2. ✅ **Always use ngrok HTTPS tunnel** (not plain HTTP)
3. ✅ **Set `AUTHORIZED_WALLET`** to your specific address
4. ❌ **Never use without authentication** on public networks
5. ❌ **Never use HTTP** (non-encrypted) on public WiFi

### Local Network:
- Can use without `--wallet-auth` if on trusted local network
- Still recommended to use wallet auth for extra security

## 📊 How It Works

1. **Server starts** with Web3 authentication enabled
2. **Client connects** via Brave Browser (with Web3 wallet support)
3. **Wallet connection** requested through browser's Web3 provider
4. **Authentication message** generated with timestamp and wallet address
5. **User signs message** with private key (never leaves wallet)
6. **Server verifies signature** cryptographically
7. **Session established** if signature is valid and wallet is authorized
8. **Upload access granted** for the session duration

## 🔍 Troubleshooting

### "No Web3 wallet detected"
- Ensure you're using Brave Browser
- Check that Born2Sub.x wallet is installed and active
- Try refreshing the page

### "Authentication failed"
- Verify you're using the correct wallet
- Check if `AUTHORIZED_WALLET` is set to your address
- Ensure signature was completed (not cancelled)

### "Cannot reach server from phone"
- Verify ngrok tunnel is running
- Use the HTTPS URL from ngrok output
- Check that your phone has internet connection

### Python dependencies error
```bash
pip install web3 eth-account flask
```

## 🎯 Example Workflow

```bash
# Terminal 1: Start upload server with wallet auth
export AUTHORIZED_WALLET=0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb7
python3 scripts/upload_server.py --wallet-auth

# Terminal 2: Create secure tunnel
ngrok http 8000

# On Phone (Brave Browser):
# 1. Open ngrok HTTPS URL
# 2. Connect Born2Sub.x wallet
# 3. Sign authentication message
# 4. Upload files securely
```

## 📝 Environment Variables

- `FLASK_SECRET_KEY` - Flask session secret (auto-generated if not set)
- `AUTHORIZED_WALLET` - Specific wallet address to authorize (optional)

**⚠️ NEVER create .env files on untrusted devices with real secrets!**

## ✅ Verification

After upload, verify files in the workspace:

```bash
ls -la uploads/
```

Files maintain their directory structure when uploaded via directory selection.

## 🚨 Untrusted Device Warning

**If you're reading this on a friend's laptop or borrowed device:**

### ❌ DO NOT:
- Enter your Born2Sub.x private key or seed phrase
- Set up the upload server with real credentials
- Save passwords in the browser
- Create `.env` with actual wallet address
- Upload sensitive files

### ✅ SAFE TO DO:
- Read documentation
- Understand the architecture
- Plan your setup for later (on your secure device)
- Take temporary notes (in `/tmp/` directory only)

### 🧹 Before You Leave This Device:
```bash
# Run cleanup
bash /tmp/cleanup_session.sh
```

Then manually:
1. Sign out of GitHub
2. Clear browser history, cache, cookies
3. Close all terminal windows
4. Delete any cloned repositories
5. Clear clipboard

**Set up the actual upload server only on YOUR phone or YOUR laptop!**

---

**Remember**: This system is designed to keep your uploads secure even on public WiFi by combining wallet-based authentication with HTTPS tunneling. Your private key never leaves your device! **Never enter credentials on devices you don't own.**
