#!/usr/bin/env python3
"""
Simple file upload server to accept files from a phone browser.

Author: Cyrus Makai Schoonover
Repository: https://github.com/CashMasterStone/I_Am_Trying
License: See LICENSE.md in repository root

Features:
- HTML upload form with optional directory upload support (Chrome/Android supports directory selection)
- Client-side JS preserves directory structure when using directory uploads
- Web3 wallet authentication (Born2Sub.x) for secure access on public WiFi
- Saves files under `uploads/` inside the repository
- Simple file listing and download links

Security notes:
- Requires wallet signature authentication when --wallet-auth flag is used
- Secret key is generated from environment variable for security
- This saves files into the repo workspace under `uploads/`
- The server should be accessed via HTTPS tunnel (ngrok) on public WiFi
"""
from __future__ import annotations

import json
import os
import secrets
import time
from pathlib import Path
from typing import List, Optional

from flask import (
    Flask,
    flash,
    jsonify,
    redirect,
    render_template_string,
    request,
    send_from_directory,
    session,
    url_for,
)

try:
    from eth_account.messages import encode_defunct
    from web3 import Web3
    WEB3_AVAILABLE = True
except ImportError:
    WEB3_AVAILABLE = False

BASE_DIR = Path(__file__).resolve().parents[1]
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

app = Flask(__name__)
# Use environment variable or generate secure random key
app.secret_key = os.environ.get('FLASK_SECRET_KEY', secrets.token_hex(32))

# Web3 configuration
WALLET_AUTH_ENABLED = False
AUTHORIZED_WALLET = os.environ.get('AUTHORIZED_WALLET', '').lower()  # Set via environment variable

INDEX_HTML = """
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Upload Server - Born2Sub.x</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
      body { font-family: system-ui, -apple-system, Roboto, Arial; max-width: 900px; margin: 2rem auto; padding: 1rem; }
      .box { padding: 1rem; border: 1px solid #ddd; border-radius: 8px; margin-bottom: 1rem; }
      .auth-box { background: #f0f9ff; border-color: #0891b2; }
      .authenticated { background: #f0fdf4; border-color: #22c55e; }
      input[type=file] { display:block; margin-top:.5rem }
      button { padding: 0.5rem 1rem; cursor: pointer; border-radius: 4px; border: 1px solid #ddd; background: #fff; }
      button:hover { background: #f5f5f5; }
      button:disabled { opacity: 0.5; cursor: not-allowed; }
      pre { background:#f7f7f7; padding: .5rem; overflow-x: auto; }
      .wallet-info { font-family: monospace; font-size: 0.9em; }
      .hidden { display: none; }
    </style>
  </head>
  <body>
    <h1>🔐 Upload Server - Born2Sub.x</h1>
    
    <div id="authBox" class="box auth-box">
      <h2>Web3 Wallet Authentication</h2>
      <p>Connect your Born2Sub.x wallet to upload files securely.</p>
      <button id="connectBtn" onclick="connectWallet()">Connect Wallet</button>
      <div id="authStatus"></div>
    </div>
    
    <div id="uploadBox" class="box hidden">
      <div class="authenticated">
        <p>✅ Authenticated as: <span id="walletAddress" class="wallet-info"></span></p>
      </div>
      <h2>Upload Files</h2>
      <p>Choose files or a directory (if your browser supports directory upload). The directory option preserves relative paths when supported.</p>
      <input id="fileInput" type="file" webkitdirectory directory multiple />
      <button id="uploadBtn">Upload</button>
      <div id="status"></div>
    </div>

    <h2>Uploaded files</h2>
    <div class="box">
      <div id="filesList">Loading…</div>
    </div>

  <script>
  let walletAuth = false;
  let userWallet = null;

  async function connectWallet() {
    const statusEl = document.getElementById('authStatus');
    
    if (!window.ethereum) {
      statusEl.innerHTML = '<p style="color:red;">❌ No Web3 wallet detected. Please use Brave Browser with Born2Sub.x wallet.</p>';
      return;
    }
    
    try {
      statusEl.innerHTML = '<p>Requesting wallet connection...</p>';
      const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
      const address = accounts[0];
      
      // Request signature for authentication
      const message = `Authenticate to I_Am_Trying Upload Server\\n\\nWallet: ${address}\\nTime: ${new Date().toISOString()}`;
      statusEl.innerHTML = '<p>Please sign the authentication message...</p>';
      
      const signature = await window.ethereum.request({
        method: 'personal_sign',
        params: [message, address]
      });
      
      // Verify signature with backend
      const resp = await fetch('/auth', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ address, message, signature })
      });
      
      const result = await resp.json();
      
      if (result.authenticated) {
        walletAuth = true;
        userWallet = address;
        document.getElementById('authBox').classList.add('hidden');
        document.getElementById('uploadBox').classList.remove('hidden');
        document.getElementById('walletAddress').innerText = address;
        listFiles();
      } else {
        statusEl.innerHTML = '<p style="color:red;">❌ Authentication failed: ' + (result.error || 'Unknown error') + '</p>';
      }
    } catch (error) {
      statusEl.innerHTML = '<p style="color:red;">❌ Error: ' + error.message + '</p>';
    }
  }

  async function listFiles(){
    const res = await fetch('/list');
    const data = await res.json();
    const el = document.getElementById('filesList');
    if(!data.files || data.files.length===0){ el.innerText = 'No files uploaded yet.'; return }
    const ul = document.createElement('ul');
    data.files.forEach(f=>{
      const li = document.createElement('li');
      const a = document.createElement('a');
      a.href = '/uploads/' + encodeURIComponent(f);
      a.innerText = f;
      a.target = '_blank';
      li.appendChild(a);
      ul.appendChild(li);
    });
    el.innerHTML = '';
    el.appendChild(ul);
  }

  document.getElementById('uploadBtn').addEventListener('click', async ()=>{
    const input = document.getElementById('fileInput');
    const files = Array.from(input.files);
    if(files.length===0){ alert('No files selected'); return }
    const fd = new FormData();
    const paths = files.map(f => f.webkitRelativePath || f.name);
    paths.forEach(p => fd.append('paths', p));
    files.forEach(f => fd.append('files', f));
    const status = document.getElementById('status');
    status.innerText = 'Uploading...';
    try{
      const resp = await fetch('/upload', { method: 'POST', body: fd });
      const json = await resp.json();
      status.innerText = json.message || 'Upload finished';
      listFiles();
    }catch(err){
      status.innerText = 'Upload failed: ' + err;
    }
  });

  listFiles();
  </script>
  </body>
</html>
"""


def secure_path_join(base: Path, rel_path: str) -> Path:
    """Join base and rel_path safely, preventing path traversal."""
    # Normalize
    rel = Path(rel_path)
    # Prevent absolute
    if rel.is_absolute():
        rel = Path(*rel.parts[1:])
    candidate = (base / rel).resolve()
    try:
        candidate.relative_to(base.resolve())
    except Exception:
        raise ValueError("Invalid path")
    return candidate


def check_auth() -> bool:
    """Check if user is authenticated (via wallet or disabled auth)."""
    if not WALLET_AUTH_ENABLED:
        return True
    return session.get('authenticated', False)


def verify_wallet_signature(address: str, message: str, signature: str) -> bool:
    """Verify Ethereum wallet signature."""
    if not WEB3_AVAILABLE:
        return False
    
    try:
        w3 = Web3()
        message_hash = encode_defunct(text=message)
        recovered_address = w3.eth.account.recover_message(message_hash, signature=signature)
        
        # Check if recovered address matches provided address
        if recovered_address.lower() != address.lower():
            return False
        
        # If AUTHORIZED_WALLET is set, check against it
        if AUTHORIZED_WALLET and recovered_address.lower() != AUTHORIZED_WALLET:
            return False
        
        return True
    except Exception as e:
        print(f"Signature verification error: {e}")
        return False


@app.route('/auth', methods=['POST'])
def authenticate():
    """Authenticate user via wallet signature."""
    if not WALLET_AUTH_ENABLED:
        return jsonify({'authenticated': True, 'message': 'Authentication disabled'})
    
    if not WEB3_AVAILABLE:
        return jsonify({'authenticated': False, 'error': 'Web3 libraries not available'}), 500
    
    data = request.json
    address = data.get('address', '').lower()
    message = data.get('message', '')
    signature = data.get('signature', '')
    
    if not all([address, message, signature]):
        return jsonify({'authenticated': False, 'error': 'Missing authentication data'}), 400
    
    if verify_wallet_signature(address, message, signature):
        session['authenticated'] = True
        session['wallet_address'] = address
        session['auth_time'] = time.time()
        return jsonify({'authenticated': True, 'wallet': address})
    else:
        return jsonify({'authenticated': False, 'error': 'Invalid signature or unauthorized wallet'}), 403


@app.route('/')
def index():
    """Main upload page - public for now, but upload requires auth."""
    return render_template_string(INDEX_HTML)

@app.route('/auth/check')
def auth_check():
    """Check if user is authorized."""
    wallet = request.args.get('wallet', '').lower()
    if is_authorized_wallet(wallet):
        return jsonify({
            'authorized': True,
            'wallet': wallet,
            'message': 'Access granted to Born2Sub.x'
        })
    return jsonify({
        'authorized': False,
        'message': 'Access restricted to Born2Sub.x and CashMasterStone only'
    }), 403

@app.route('/auth/session', methods=['POST'])
def create_session():
    """Create authenticated session for wallet."""
    data = request.get_json()
    wallet = data.get('wallet', '').lower()
    
    if not is_authorized_wallet(wallet):
        return jsonify({'error': 'Unauthorized wallet address'}), 403
    
    # Generate session token
    token = secrets.token_urlsafe(32)
    active_sessions[token] = {
        'wallet': wallet,
        'created': os.time(),
        'expires': os.time() + SESSION_TIMEOUT
    }
    
    return jsonify({
        'token': token,
        'expires_in': SESSION_TIMEOUT,
        'wallet': wallet
    })


@app.route('/upload', methods=['POST'])
def upload():
    """Upload files - requires authentication if enabled."""
    if not check_auth():
        return jsonify({'message': 'Authentication required'}), 401
    
    # paths are submitted as repeated form fields in the same order as files
    raw_paths: List[str] = request.form.getlist('paths')
    files = request.files.getlist('files')
    if not files:
        return jsonify({'message': 'no files received'}), 400

    saved = 0
    for i, f in enumerate(files):
        rel = raw_paths[i] if i < len(raw_paths) else f.filename
        # sanitize relative path
        rel = rel.lstrip('/\\')
        try:
            dest = secure_path_join(UPLOAD_DIR, rel)
        except ValueError:
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        f.save(str(dest))
        saved += 1

    return jsonify({'message': f'saved {saved} files'})


@app.route('/list')
def list_uploaded():
    """List uploaded files - requires authentication if enabled."""
    if not check_auth():
        return jsonify({'files': [], 'error': 'Authentication required'}), 401
    
    files = []
    for p in UPLOAD_DIR.rglob('*'):
        if p.is_file():
            files.append(str(p.relative_to(UPLOAD_DIR)).replace('\\\\', '/'))
    files.sort()
    return jsonify({'files': files})


@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    """Download uploaded file - requires authentication if enabled."""
    if not check_auth():
        return "Authentication required", 401
    # send from uploads directory
    safe = filename.lstrip('/\\')
    try:
        return send_from_directory(str(UPLOAD_DIR), safe, as_attachment=True)
    except Exception:
        return "Not found", 404


def main():
    global WALLET_AUTH_ENABLED
    
    import argparse

    p = argparse.ArgumentParser(
        description='Run upload server for I_Am_Trying repository',
        epilog='Author: Cyrus Makai Schoonover | Repository: https://github.com/CashMasterStone/I_Am_Trying'
    )
    p.add_argument('--host', default='0.0.0.0', help='Host to bind (default: 0.0.0.0)')
    p.add_argument('--port', type=int, default=8000, help='Port to listen on (default: 8000)')
    p.add_argument('--wallet-auth', action='store_true', 
                   help='Enable Web3 wallet authentication (Born2Sub.x)')
    p.add_argument('--authorized-wallet', type=str, 
                   help='Specific wallet address to authorize (optional, uses env AUTHORIZED_WALLET if not set)')
    args = p.parse_args()
    
    # Set global auth flag
    WALLET_AUTH_ENABLED = args.wallet_auth
    
    # Set authorized wallet if provided
    if args.authorized_wallet:
        global AUTHORIZED_WALLET
        AUTHORIZED_WALLET = args.authorized_wallet.lower()
    
    # Check dependencies if wallet auth enabled
    if WALLET_AUTH_ENABLED and not WEB3_AVAILABLE:
        print("❌ Error: Web3 authentication enabled but required packages not installed.")
        print("   Install with: pip install web3 eth-account")
        return
    
    print(f"🔐 Upload Server - I_Am_Trying")
    print(f"   Author: Cyrus Makai Schoonover")
    print(f"   Repository: https://github.com/CashMasterStone/I_Am_Trying")
    print(f"")
    print(f"   Server: http://{args.host}:{args.port}/")
    print(f"   Upload directory: {UPLOAD_DIR}")
    print(f"   Wallet Authentication: {'✅ ENABLED' if WALLET_AUTH_ENABLED else '❌ DISABLED'}")
    
    if WALLET_AUTH_ENABLED:
        if AUTHORIZED_WALLET:
            print(f"   Authorized Wallet: {AUTHORIZED_WALLET}")
        else:
            print(f"   Authorized Wallet: Any wallet (set AUTHORIZED_WALLET env var to restrict)")
        print(f"")
        print(f"⚠️  SECURITY: Use HTTPS tunnel (ngrok) on public WiFi!")
        print(f"   Example: ngrok http {args.port}")
    
    print(f"")
    app.run(host=args.host, port=args.port, debug=False)


if __name__ == '__main__':
    main()
