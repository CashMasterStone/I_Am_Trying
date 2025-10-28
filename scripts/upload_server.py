#!/usr/bin/env python3
"""
Simple file upload server to accept files from a phone browser.

Author: Cyrus Makai Schoonover
Repository: https://github.com/CashMasterStone/I_Am_Trying
License: See LICENSE.md in repository root

Features:
- HTML upload form with optional directory upload support (Chrome/Android supports directory selection).
- Client-side JS preserves directory structure when using directory uploads.
- Saves files under `uploads/` inside the repository.
- Simple file listing and download links.

Security notes:
- This saves files into the repo workspace under `uploads/`.
- The server should only be run on trusted networks or with an authenticated tunnel (ngrok) when exposing to the Internet.
- Secret key is generated from environment variable for security.
"""
from __future__ import annotations

import json
import os
import secrets
from pathlib import Path
from typing import List

from flask import (
    Flask,
    flash,
    jsonify,
    redirect,
    render_template_string,
    request,
    send_from_directory,
    url_for,
)

BASE_DIR = Path(__file__).resolve().parents[1]
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

app = Flask(__name__)
# Use environment variable or generate secure random key
app.secret_key = os.environ.get('FLASK_SECRET_KEY', secrets.token_hex(32))

INDEX_HTML = """
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Upload Server</title>
    <style>
      body { font-family: system-ui, -apple-system, Roboto, Arial; max-width: 900px; margin: 2rem auto; }
      .box { padding: 1rem; border: 1px solid #ddd; border-radius: 8px; }
      input[type=file] { display:block; margin-top:.5rem }
      pre { background:#f7f7f7; padding: .5rem }
    </style>
  </head>
  <body>
    <h1>Upload files to workspace</h1>
    <div class="box">
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


@app.route('/')
def index():
    return render_template_string(INDEX_HTML)


@app.route('/upload', methods=['POST'])
def upload():
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
    files = []
    for p in UPLOAD_DIR.rglob('*'):
        if p.is_file():
            files.append(str(p.relative_to(UPLOAD_DIR)).replace('\\\\', '/'))
    files.sort()
    return jsonify({'files': files})


@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    # send from uploads directory
    safe = filename.lstrip('/\\')
    try:
        return send_from_directory(str(UPLOAD_DIR), safe, as_attachment=True)
    except Exception:
        return "Not found", 404


def main():
    import argparse

    p = argparse.ArgumentParser(description='Run upload server')
    p.add_argument('--host', default='0.0.0.0', help='Host to bind')
    p.add_argument('--port', type=int, default=8000, help='Port to listen on')
    args = p.parse_args()
    print(f"Upload server running on http://{args.host}:{args.port}/")
    app.run(host=args.host, port=args.port, debug=True)


if __name__ == '__main__':
    main()
