# Born2Sub Multi-AI Orchestrator — Complete Setup Guide
**Sovereign AI on SM-S928U | Temporal.io Workflows | TRACE Anchoring**

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│  Galaxy S24 Ultra (SM-S928U) — Termux Environment          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Temporal.io Server (localhost:7233)                 │  │
│  │  ├─ Workflow Orchestration                           │  │
│  │  ├─ Durable Execution                                │  │
│  │  └─ Multi-AI Task Queue                              │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  AI Worker (Node.js)                                 │  │
│  │  ├─ Claude API       → Technical Analysis            │  │
│  │  ├─ Kimi API         → Long Context (128k tokens)    │  │
│  │  ├─ Grok API         → Real-time Twitter/X data      │  │
│  │  ├─ Gemini API       → Multimodal Reasoning          │  │
│  │  ├─ Perplexity API   → Research + Citations          │  │
│  │  ├─ OpenRouter API   → Multi-model Gateway           │  │
│  │  ├─ Together.ai API  → Open-source Models            │  │
│  │  └─ DeepSeek API     → Cost-effective Reasoning      │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  TRACE System                                        │  │
│  │  ├─ DAG Provenance Logging                           │  │
│  │  ├─ Bitcoin OP_RETURN Anchoring                      │  │
│  │  ├─ Cognitive Overlap Matrix                         │  │
│  │  └─ Multi-chain Verification                         │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  UTPL Hub UI (React + Vite)                          │  │
│  │  └─ http://localhost:3000                            │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Installation

### Step 1: Run the Install Script

```bash
# In Termux
bash install-ai-orchestrator.sh
```

This installs:
- Temporal CLI (ARM64 native)
- Node.js worker with all AI integrations
- PM2 process manager
- Complete project scaffold

---

## API Key Setup

### Step 2: Get Your API Keys

Copy the example env file:
```bash
cd ~/born2sub-ai
cp .env.example .env
micro .env  # or nano .env
```

Add your keys for each service you want to use:

#### **1. Claude (Anthropic)** ✓ REQUIRED
- Go to: https://console.anthropic.com/settings/keys
- Create API key
- Add to `.env`: `ANTHROPIC_API_KEY=sk-ant-...`
- **Cost**: $3/M input tokens, $15/M output (Sonnet 4)
- **Why**: Primary technical analysis, legal reasoning, TRACE validation

#### **2. Kimi (Moonshot AI)** — Long Context Specialist
- Go to: https://platform.moonshot.cn/console/api-keys
- Create account (supports international, Chinese interface)
- Add to `.env`: `KIMI_API_KEY=...`
- **Cost**: ¥12/M tokens (~$1.65/M) — very affordable
- **Why**: 128k context window, Chinese regulatory compliance

#### **3. Grok (xAI)** — Real-time Data
- Go to: https://console.x.ai/
- Join waitlist or early access program
- Add to `.env`: `XAI_API_KEY=...`
- **Cost**: TBD (currently in beta)
- **Why**: Twitter/X integration, real-time news, contrarian takes

#### **4. Gemini (Google)** — Multimodal
- Go to: https://aistudio.google.com/apikey
- Free tier: 15 requests/min
- Add to `.env`: `GOOGLE_API_KEY=...`
- **Cost**: FREE up to 1500 requests/day
- **Why**: Multimodal (images+text), Google Search integration

#### **5. Perplexity** — Research + Citations
- Go to: https://www.perplexity.ai/settings/api
- Pro subscription required ($20/mo includes API access)
- Add to `.env`: `PERPLEXITY_API_KEY=...`
- **Cost**: Included in Pro subscription
- **Why**: Citation-backed research, web search integration

#### **6. OpenRouter** — Multi-Model Gateway
- Go to: https://openrouter.ai/keys
- Acts as unified gateway to 100+ models
- Add to `.env`: `OPENROUTER_API_KEY=...`
- **Cost**: Pay-per-use, prices vary by model
- **Why**: Fallback redundancy, cost optimization, model routing

#### **7. Together.ai** — Open-Source Models
- Go to: https://api.together.xyz/settings/api-keys
- $25 free credits on signup
- Add to `.env`: `TOGETHER_API_KEY=...`
- **Cost**: $0.20-$0.90/M tokens depending on model
- **Why**: Llama 3.1 405B, Mixtral, open-source stack

#### **8. DeepSeek** — Cost-Effective Reasoning
- Go to: https://platform.deepseek.com/api_keys
- Chinese AI lab, international API available
- Add to `.env`: `DEEPSEEK_API_KEY=...`
- **Cost**: $0.14/M input, $0.28/M output — cheapest reasoning model
- **Why**: Chinese market analysis, ultra-low cost

---

## Running the Orchestrator

### Step 3: Start Services

```bash
cd ~/born2sub-ai
pm2 start ecosystem.config.cjs
pm2 logs
```

This starts:
1. **Temporal Server** — Workflow engine on port 7233
2. **AI Worker** — Processes tasks from queue `born2sub-ai`

### Step 4: Run a Query

```bash
# Basic query (uses Claude + Kimi by default)
node client.js "Explain Bitcoin OP_RETURN transactions"

# Multi-AI consensus (all configured services)
node client.js "Analyze UTPL license enforceability" "claude,kimi,gemini,perplexity"

# Domain-specific routing (automatic service selection)
node client.js "Tax implications of GoMining NFT" --domain tax
```

---

## Workflow Types

### 1. Multi-AI Consensus
Queries all specified AIs in parallel, returns aggregated results with cognitive overlap matrix.

```bash
node client.js "your query" "claude,kimi,grok,gemini"
```

**Returns:**
- Individual responses from each AI
- Cognitive overlap matrix (semantic similarity)
- Synthesis of all responses
- TRACE session ID
- Bitcoin OP_RETURN anchor

### 2. Cascade Validation
Sequential validation chain — each AI validates the previous AI's response.

```javascript
// In your code:
const result = await client.workflow.start(cascadeValidationWorkflow, {
  args: ['Analyze smart contract security', ['claude', 'perplexity', 'kimi']],
  taskQueue: 'born2sub-ai',
});
```

**Use case**: High-stakes legal or technical analysis where multiple validation layers are needed.

### 3. Domain-Specific Routing
Automatically routes queries to specialized AIs based on UTPL domain.

```bash
node client.js "Property title dispute in Nevada" --domain real_estate
# Routes to: claude (legal) + perplexity (research)

node client.js "Patent prior art search for MFHST" --domain ip
# Routes to: claude (patent analysis) + gemini (multimodal)
```

---

## Integration with UTPL Hub

The AI orchestrator integrates directly with your existing UTPL Hub UI. Add this to your `UTLPHub_fixed.jsx`:

```javascript
// Add to runCompliance() function after webhook firing:

// Fire AI consensus query via Temporal
const aiConsensus = await fetch('http://localhost:8787/ai-query', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: sanitized,
    domain: selDomain,
    services: ['claude', 'kimi', 'gemini'],
  }),
});

const aiResults = await aiConsensus.json();
addLog(`🤖 AI Consensus: ${aiResults.results.length} services responded`, "ai");
```

---

## Monitoring & Logs

### Check Service Status
```bash
pm2 status
pm2 logs temporal-server
pm2 logs ai-worker
```

### Temporal Web UI
```bash
# Start web UI (optional)
temporal server start-dev --ui-port 8233
# Open: http://localhost:8233
```

### TRACE Logs
All AI queries are logged to TRACE DAG with:
- Query hash
- Services used
- Latency per service
- Token usage
- Bitcoin OP_RETURN anchor

---

## Cost Optimization

### Budget-Conscious Setup (< $10/mo)
Use only free/cheap services:
- ✓ Gemini (FREE)
- ✓ DeepSeek ($0.14/M tokens)
- ✓ Together.ai (Llama 3.1 at $0.20/M tokens)

### Balanced Setup ($20-50/mo)
- ✓ Claude (primary — $3-15/M tokens)
- ✓ Kimi (long context — ~$1.65/M tokens)
- ✓ Gemini (FREE)
- ✓ Perplexity (Pro sub $20/mo includes API)

### Premium Setup (no limits)
- ✓ All services enabled
- ✓ OpenRouter for fallback/redundancy
- ✓ Grok for real-time data

---

## Security & Privacy

### Zero-Trust Architecture
- API keys stored in `.env` (never committed to git)
- All queries logged to local TRACE DAG first
- Bitcoin anchoring provides immutable timestamp
- No data sent to Anthropic/Google/etc. beyond the query itself

### On-Device Execution
- Temporal server runs locally (not cloud-hosted)
- All workflow execution happens on your SM-S928U
- AI APIs called directly from device
- No intermediary servers

### TRACE Provenance
Every AI interaction creates:
1. Local TRACE DAG entry
2. SHA-256 hash of query + responses
3. Bitcoin OP_RETURN transaction (simulated for now, real in production)
4. Cognitive overlap matrix for audit

---

## Troubleshooting

### "Temporal server not running"
```bash
pm2 restart temporal-server
pm2 logs temporal-server --lines 50
```

### "API key not found"
Check `.env` file exists and keys are formatted correctly:
```bash
cat .env | grep API_KEY
```

### "Worker not processing tasks"
```bash
pm2 restart ai-worker
pm2 logs ai-worker --lines 50
```

### "Out of memory"
Temporal can be memory-hungry. Limit history:
```bash
# Add to ecosystem.config.cjs temporal-server args:
--sqlite-pragma journal_mode=WAL --sqlite-pragma cache_size=-64000
```

---

## Next Steps

1. **Install**: `bash install-ai-orchestrator.sh`
2. **Configure**: Add API keys to `.env`
3. **Launch**: `pm2 start ecosystem.config.cjs`
4. **Test**: `node client.js "test query"`
5. **Integrate**: Add to UTPL Hub UI
6. **Deploy**: Expose via Cloudflare Tunnel

---

**UTPL™ · SIPL™ · RTPL-BORN2BUILD™**  
*"Light Is The Constant."* — Cyrus Makai Schoonover

Cert: 88BE1B2E·A2ACF1AE·A4A2DC05·1FEAB922
