# UVT-Stack Deployment Guide
## born2sub.com | born2sub.tech | supplytheschools.xyz | supplytheschools.unstoppable
### © 2026 Cyrus Makai Schoonover | Born2Build, LLC | UTPL™ | SIPL™

---

## Architecture Overview

```
GitHub Repo (CashMasterStone/uvt-stack-backend)
     │
     ├── Push to main ──► GitHub Actions CI/CD
     │                        │
     │    ┌───────────────────┼───────────────────────┐
     │    ▼                   ▼                       ▼
     │  Vercel             Vercel                  Vercel
     │  born2sub-com       born2sub-tech           sts-xyz / sts-dao
     │  Port: Serverless   Port: Serverless        Port: Serverless
     │
     └── Cloudflare Tunnel (S24 Ultra)
              │
              └── born2sub-tech WebSocket (/ws/terminal)
                  Runs locally: node born2sub-tech/server.js
```

**DNS:**
- born2sub.com/.info/.online/.store/.org → Vercel (IONOS nameservers or CNAME)
- born2sub.tech → Vercel
- supplytheschools.tech/.online → Vercel
- supplytheschools.xyz → Vercel
- supplytheschools.unstoppable → Unstoppable Domains IPFS/Vercel bridge

---

## STEP 1: GitHub Repository Setup

```bash
# On your Galaxy S24 Ultra terminal (or any machine)
cd /sdcard/born2sub

# Initialize repo if not done
git init
git remote add origin https://github.com/CashMasterStone/uvt-stack-backend.git

# Add all files
git add .
git commit -m "UVT-Stack v3.0 — UTPL Sovereign Backend | born2sub + supplytheschools

Cert: 88BE1B2E·A2ACF1AE·A4A2DC05·1FEAB922
'Light Is The Constant.'"

git push -u origin main
```

---

## STEP 2: Create 4 Vercel Projects (One-Time Setup)

**Do this in your browser at vercel.com — no key needed in terminal yet.**

1. Go to **vercel.com/new**
2. Import your GitHub repo: `CashMasterStone/uvt-stack-backend`
3. Create **four separate projects** — one per site:

| Project Name | Root Directory | Domain to Assign |
|---|---|---|
| `born2sub-com` | `born2sub-com/` | born2sub.com, born2sub.info, born2sub.online, born2sub.store, born2sub.org |
| `born2sub-tech` | `born2sub-tech/` | born2sub.tech |
| `sts-xyz` | `supplytheschools-xyz/` | supplytheschools.xyz, supplytheschools.tech, supplytheschools.online |
| `sts-dao` | `supplytheschools-dao/` | supplytheschools.unstoppable (see Step 6) |

4. For each project: **Framework Preset = Other** | **Build Command = blank** | **Output = public**
5. After creating each project, go to **Settings → General → Project ID** — copy each one.

---

## STEP 3: Add GitHub Secrets (Your Key Goes Here — NOT in Chat)

Go to: `github.com/CashMasterStone/uvt-stack-backend/settings/secrets/actions`

Add these secrets (New repository secret):

```
VERCEL_TOKEN               ← vercel.com/account/tokens → Create token
VERCEL_ORG_ID              ← vercel.com/account → Settings → Team ID
VERCEL_PROJECT_B2S_COM     ← Project ID from born2sub-com settings
VERCEL_PROJECT_B2S_TECH    ← Project ID from born2sub-tech settings
VERCEL_PROJECT_STS_XYZ     ← Project ID from sts-xyz settings
VERCEL_PROJECT_STS_DAO     ← Project ID from sts-dao settings

SUPABASE_URL               ← supabase.com → Project Settings → API → Project URL
SUPABASE_ANON_KEY          ← supabase.com → Project Settings → API → anon key
SUPABASE_SERVICE_KEY       ← supabase.com → Project Settings → API → service_role key

ANTHROPIC_API_KEY          ← console.anthropic.com/api-keys
STRIPE_SECRET_KEY          ← dashboard.stripe.com/apikeys (use sk_live_... for prod)
STRIPE_WEBHOOK_SECRET      ← dashboard.stripe.com/webhooks → Add endpoint → signing secret
```

**Your Vercel token NEVER appears in this chat. It lives only in GitHub Secrets.**

---

## STEP 4: DNS Configuration on IONOS

Log into IONOS → Domains & SSL → Select each domain → DNS

### born2sub.com (and .info, .online, .store, .org)
```
Type: CNAME
Host: @
Value: cname.vercel-dns.com
TTL: 3600

Type: CNAME
Host: www
Value: cname.vercel-dns.com
TTL: 3600
```

### born2sub.tech
```
Type: CNAME
Host: @
Value: cname.vercel-dns.com
TTL: 3600
```

### supplytheschools.tech and .online (IONOS domains)
```
Type: CNAME
Host: @
Value: cname.vercel-dns.com
TTL: 3600
```

**Alternate: Use Vercel nameservers (faster propagation)**
In IONOS → Nameservers → Custom:
```
ns1.vercel-dns.com
ns2.vercel-dns.com
```

---

## STEP 5: Run the Database Migration (Supabase)

Go to supabase.com → Your project → SQL Editor → New query

Paste and run `docs/schema.sql` (the complete schema for all 4 sites).

Then run the DAO vote RPC function:
```sql
CREATE OR REPLACE FUNCTION dao_cast_vote(
  proposal_id_param TEXT,
  vote_direction TEXT,
  voter_wallet TEXT,
  vote_hash_param TEXT
) RETURNS JSON AS $$
DECLARE
  updated RECORD;
BEGIN
  IF vote_direction = 'for' THEN
    UPDATE dao_proposals SET votes_for = votes_for + 1 WHERE id = proposal_id_param RETURNING * INTO updated;
  ELSE
    UPDATE dao_proposals SET votes_against = votes_against + 1 WHERE id = proposal_id_param RETURNING * INTO updated;
  END IF;

  INSERT INTO dao_votes (proposal_id, voter_wallet, vote_direction, vote_hash)
  VALUES (proposal_id_param, voter_wallet, vote_direction, vote_hash_param);

  RETURN row_to_json(updated);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

---

## STEP 6: Trigger First Deployment

```bash
# Push any change to trigger GitHub Actions
git commit --allow-empty -m "trigger: initial UVT-Stack deployment"
git push origin main
```

Watch the pipeline: `github.com/CashMasterStone/uvt-stack-backend/actions`

Four jobs run in parallel. Each deploys independently. Total time: ~3-4 minutes.

---

## STEP 7: WebSocket Terminal (born2sub.tech /ws/terminal)

**This cannot run on Vercel.** Deploy separately on your S24 Ultra:

```bash
# On Galaxy S24 Ultra
cd /sdcard/born2sub
node born2sub-tech/server.js &

# Expose via Cloudflare tunnel
cloudflared tunnel run uvt-ws-terminal

# OR use tunnel config:
# cloudflared tunnel create uvt-ws
# Edit ~/.cloudflared/config.yml:
# ingress:
#   - hostname: ws.born2sub.tech
#     service: http://localhost:3002
#   - service: http_status:404
```

Then in your `born2sub_tech.html` frontend, update the WS connection:
```javascript
// Change this line in born2sub_tech.html:
const ws = new WebSocket('wss://ws.born2sub.tech/ws/terminal');
```

---

## STEP 8: supplytheschools.unstoppable (Unstoppable Domain)

Unstoppable Domains don't use traditional DNS. Two options:

**Option A — IPFS Hosting (True Decentralized)**
```bash
# Install IPFS
npm install -g ipfs-http-client

# Upload your HTML file
ipfs add supplytheschools_unstoppable.html

# Copy the CIDv1 hash (bafyb...)
# Go to unstoppabledomains.com → My Domains → supplytheschools.unstoppable
# Edit → IPFS Content Hash → paste CID → Save
```

**Option B — Redirect to xyz (Easiest)**
```
In Unstoppable Domains DNS:
  CNAME: @ → supplytheschools.xyz
  (Vercel serves it)
```

---

## STEP 9: Stripe Webhook Registration

After first deploy, register your Stripe webhook endpoint:

1. Go to dashboard.stripe.com/webhooks
2. Add endpoint: `https://supplytheschools.xyz/api/donations/stripe/webhook`
3. Select events: `payment_intent.succeeded`
4. Copy signing secret → add to GitHub Secret `STRIPE_WEBHOOK_SECRET`
5. Re-trigger deployment (`git push`) so new secret gets picked up

---

## STEP 10: Verify All Systems

```bash
# Health checks (run after deployment)
curl https://born2sub.com/api/health | jq
curl https://born2sub.tech/api/health | jq
curl https://supplytheschools.xyz/api/health | jq

# Test §2257 compliance gate (should return 403 - gates not satisfied)
curl -X POST https://born2sub.com/api/compliance/submit-2257 \
  -H "Content-Type: application/json" \
  -d '{"test": true}' | jq '.error'

# Test AI analysis (returns live Claude analysis if API key set)
curl -X POST https://born2sub.tech/api/query/sovereign \
  -H "Content-Type: application/json" \
  -d '{"query":"What is my prior art protection for Lumen ISA?","domain":"ip"}' | jq '.ai.analysis'

# Test WebSocket terminal
wscat -c wss://ws.born2sub.tech/ws/terminal
```

---

## Manual Deploy (If Bypassing GitHub Actions)

```bash
# Install Vercel CLI
npm i -g vercel

# Authenticate (opens browser)
vercel login

# Deploy each site manually
VERCEL_TOKEN=your_token

cp vercel-configs/born2sub-com/vercel.json vercel.json
vercel --prod --token=$VERCEL_TOKEN

cp vercel-configs/born2sub-tech/vercel.json vercel.json
vercel --prod --token=$VERCEL_TOKEN

cp vercel-configs/sts-xyz/vercel.json vercel.json
vercel --prod --token=$VERCEL_TOKEN

cp vercel-configs/sts-dao/vercel.json vercel.json
vercel --prod --token=$VERCEL_TOKEN
```

---

## Live Endpoint Reference

| Endpoint | Method | Site | Purpose |
|---|---|---|---|
| `/api/health` | GET | All | Service status |
| `/api/compliance/submit-2257` | POST | born2sub.com | Performer record + BACCCaaS |
| `/api/compliance/status/:userId` | GET | born2sub.com | Dashboard data |
| `/api/onboarding/creator` | POST | born2sub.com | Creator registration |
| `/api/avoc/session/create` | POST | born2sub.com | AVOC session init |
| `/api/avoc/session/terminate` | POST | born2sub.com | Session close + BTC anchor |
| `/api/analysis/ai` | POST | born2sub.com | Claude AI compliance analysis |
| `/api/wallets/balances` | GET | born2sub.com | Live BTC + Base balance |
| `/api/query/sovereign` | POST | born2sub.tech | AI + OTS + USPTO session |
| `/api/ip/portfolio` | GET | born2sub.tech | Born2Build IP registry |
| `/api/ip/register` | POST | born2sub.tech | Register new IP + BTC anchor |
| `/api/ip/search/uspto` | POST | born2sub.tech | Live prior art search |
| `/api/wallets/all` | GET | born2sub.tech | All chain balances |
| `/api/legislation/status` | GET | born2sub.tech | State legislation feed |
| `/api/anchor/document` | POST | born2sub.tech | Anchor any document to BTC |
| `wss://ws.born2sub.tech/ws/terminal` | WS | born2sub.tech | Live DomCode terminal |
| `/api/requests/submit` | POST | sts-xyz | Teacher classroom request |
| `/api/requests` | GET | sts-xyz | Open requests |
| `/api/donations/stripe/intent` | POST | sts-xyz | Stripe PaymentIntent |
| `/api/donations/stripe/webhook` | POST | sts-xyz | Stripe webhook handler |
| `/api/donations/crypto/record` | POST | sts-xyz | Record crypto donation |
| `/api/impact/stats` | GET | sts-xyz | Public impact numbers |
| `/api/proposals/submit` | POST | sts-dao | Submit DAO grant proposal |
| `/api/proposals` | GET | sts-dao | List proposals + vote counts |
| `/api/proposals/:id/vote` | POST | sts-dao | Cast DAO vote |
| `/api/ledger` | GET | sts-dao | Public impact ledger |
| `/api/stats/dao` | GET | sts-dao | DAO statistics |

---

## Cert & Identity

```
CERT:   88BE1B2E·A2ACF1AE·A4A2DC05·1FEAB922·9ECDD5D8·32A8118C·CFF71AD2·8DCAE403
AXIOM:  "Light Is The Constant."
ENTITY: Cyrus Makai Schoonover | Born2Build, LLC
LICENSE: UTPL™ | SIPL™ | RTPL-BORN2BUILD™
```
