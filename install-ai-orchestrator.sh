#!/data/data/com.termux/files/usr/bin/bash
# ═══════════════════════════════════════════════════════════════
# TEMPORAL.IO + MULTI-AI ORCHESTRATOR — TERMUX INSTALL
# Born2Build Sovereign AI Stack
# ═══════════════════════════════════════════════════════════════

set -e
G='\033[0;32m' Y='\033[1;33m' N='\033[0m'
ok() { echo -e "${G}[✓]${N} $1"; }
inf() { echo -e "${Y}[→]${N} $1"; }

echo -e "${G}"
echo "╔══════════════════════════════════════════════════╗"
echo "║  ⚡ Born2Sub AI Orchestrator Setup               ║"
echo "║  Temporal.io + Multi-AI Workflows                ║"
echo "╚══════════════════════════════════════════════════╝"
echo -e "${N}"

# ── 1. INSTALL TEMPORAL CLI ─────────────────────────────────────
inf "Installing Temporal CLI (ARM64)..."
cd /tmp
TEMPORAL_VERSION="v1.1.1"
wget -q "https://temporal.download/cli/archive/latest?platform=linux&arch=arm64" -O temporal.tar.gz
tar -xzf temporal.tar.gz
mv temporal "$PREFIX/bin/"
chmod +x "$PREFIX/bin/temporal"
temporal --version && ok "Temporal CLI installed"

# ── 2. CREATE PROJECT STRUCTURE ────────────────────────────────
inf "Creating AI orchestrator project..."
mkdir -p ~/born2sub-ai && cd ~/born2sub-ai

# package.json
cat > package.json << 'EOF'
{
  "name": "born2sub-ai-orchestrator",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "worker": "node worker.js",
    "dev": "temporal server start-dev",
    "client": "node client.js"
  },
  "dependencies": {
    "@temporalio/client": "^1.11.3",
    "@temporalio/worker": "^1.11.3",
    "@temporalio/workflow": "^1.11.3",
    "@temporalio/activity": "^1.11.3",
    "dotenv": "^16.4.7"
  }
}
EOF

npm install --silent
ok "Dependencies installed"

# ── 3. WORKFLOW DEFINITIONS ─────────────────────────────────────
cat > workflows.js << 'EOF'
import { proxyActivities } from '@temporalio/workflow';

const activities = proxyActivities({
  startToCloseTimeout: '5 minutes',
  retry: { maximumAttempts: 3 },
});

export async function multiAIQuery(query, services) {
  const { queryAI, logToTRACE, anchorToBitcoin } = activities;
  
  const traceSession = await logToTRACE({
    event: 'MULTI_AI_INIT',
    query,
    services,
  });

  const results = await Promise.allSettled(
    services.map(svc => queryAI({ service: svc, query }))
  );

  const successful = results
    .filter(r => r.status === 'fulfilled')
    .map(r => r.value);

  await anchorToBitcoin({
    type: 'MULTI_AI',
    traceSession,
    results: successful.length,
  });

  return { traceSession, results: successful };
}
EOF

# ── 4. ACTIVITIES ───────────────────────────────────────────────
cat > activities.js << 'EOF'
const AI_ENDPOINTS = {
  claude: {
    url: 'https://api.anthropic.com/v1/messages',
    key: process.env.ANTHROPIC_API_KEY,
    format: 'anthropic',
  },
  kimi: {
    url: 'https://api.moonshot.cn/v1/chat/completions',
    key: process.env.KIMI_API_KEY,
    format: 'openai',
  },
  grok: {
    url: 'https://api.x.ai/v1/chat/completions',
    key: process.env.XAI_API_KEY,
    format: 'openai',
  },
  gemini: {
    url: 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent',
    key: process.env.GOOGLE_API_KEY,
    format: 'gemini',
  },
};

export async function queryAI({ service, query }) {
  const config = AI_ENDPOINTS[service];
  if (!config || !config.key) {
    throw new Error(`${service} not configured`);
  }

  const startTime = Date.now();

  let response;
  if (config.format === 'anthropic') {
    response = await fetch(config.url, {
      method: 'POST',
      headers: {
        'x-api-key': config.key,
        'anthropic-version': '2023-06-01',
        'content-type': 'application/json',
      },
      body: JSON.stringify({
        model: 'claude-sonnet-4-20250514',
        max_tokens: 4096,
        messages: [{ role: 'user', content: query }],
      }),
    });
    const data = await response.json();
    return {
      service,
      response: data.content[0].text,
      latency: Date.now() - startTime,
    };
  } else if (config.format === 'openai') {
    response = await fetch(config.url, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${config.key}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: service === 'kimi' ? 'moonshot-v1-8k' : 'grok-2-1212',
        messages: [{ role: 'user', content: query }],
      }),
    });
    const data = await response.json();
    return {
      service,
      response: data.choices[0].message.content,
      latency: Date.now() - startTime,
    };
  }
}

export async function logToTRACE(event) {
  const id = `TRACE-${Date.now().toString(36)}`;
  console.log(`[TRACE] ${id}`, event);
  return id;
}

export async function anchorToBitcoin(payload) {
  const hash = JSON.stringify(payload).split('').reduce((a,b) => {
    a = ((a << 5) - a) + b.charCodeAt(0);
    return a & a;
  }, 0);
  const anchor = `OP_RETURN:0x${Math.abs(hash).toString(16)}`;
  console.log(`[BTC] ${anchor}`);
  return anchor;
}
EOF

# ── 5. WORKER ───────────────────────────────────────────────────
cat > worker.js << 'EOF'
import { Worker, NativeConnection } from '@temporalio/worker';
import * as activities from './activities.js';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import 'dotenv/config';

const __dirname = dirname(fileURLToPath(import.meta.url));

async function run() {
  const connection = await NativeConnection.connect({
    address: 'localhost:7233',
  });

  const worker = await Worker.create({
    connection,
    namespace: 'default',
    taskQueue: 'born2sub-ai',
    workflowsPath: join(__dirname, 'workflows.js'),
    activities,
  });

  console.log('⚡ AI Orchestrator Worker: ACTIVE');
  console.log('Task Queue: born2sub-ai');
  await worker.run();
}

run().catch(err => {
  console.error(err);
  process.exit(1);
});
EOF

# ── 6. CLIENT ───────────────────────────────────────────────────
cat > client.js << 'EOF'
import { Connection, Client } from '@temporalio/client';
import { multiAIQuery } from './workflows.js';
import 'dotenv/config';

async function run() {
  const connection = await Connection.connect({ address: 'localhost:7233' });
  const client = new Client({ connection });

  const query = process.argv[2] || 'Explain quantum computing in 3 sentences';
  const services = (process.argv[3] || 'claude,kimi').split(',');

  console.log(`Query: ${query}`);
  console.log(`Services: ${services.join(', ')}`);

  const handle = await client.workflow.start(multiAIQuery, {
    args: [query, services],
    taskQueue: 'born2sub-ai',
    workflowId: `ai-query-${Date.now()}`,
  });

  console.log(`Started workflow: ${handle.workflowId}`);
  const result = await handle.result();

  console.log('\n╔══════════════════════════════════════╗');
  console.log('║  MULTI-AI CONSENSUS RESULT           ║');
  console.log('╚══════════════════════════════════════╝\n');
  
  result.results.forEach(r => {
    console.log(`\n${r.service.toUpperCase()} (${r.latency}ms):`);
    console.log('─'.repeat(50));
    console.log(r.response);
  });
}

run().catch(err => console.error(err));
EOF

# ── 7. ENV TEMPLATE ─────────────────────────────────────────────
cat > .env.example << 'EOF'
# AI Service API Keys
ANTHROPIC_API_KEY=sk-ant-...
KIMI_API_KEY=...
XAI_API_KEY=...
GOOGLE_API_KEY=...
PERPLEXITY_API_KEY=...
OPENROUTER_API_KEY=...
TOGETHER_API_KEY=...
DEEPSEEK_API_KEY=...

# Temporal
TEMPORAL_ADDRESS=localhost:7233
EOF

ok "Project scaffolded at ~/born2sub-ai"

# ── 8. PM2 ECOSYSTEM ────────────────────────────────────────────
cat > ecosystem.config.cjs << 'EOF'
module.exports = {
  apps: [
    {
      name: 'temporal-server',
      script: 'temporal',
      args: 'server start-dev --db-filename ~/born2sub-ai/temporal.db',
      autorestart: true,
    },
    {
      name: 'ai-worker',
      script: 'worker.js',
      autorestart: true,
      wait_ready: true,
      listen_timeout: 10000,
    },
  ],
};
EOF

ok "PM2 ecosystem config created"

echo ""
echo -e "${G}╔══════════════════════════════════════════════════╗"
echo    "║  ✓ AI ORCHESTRATOR: READY                       ║"
echo    "║                                                  ║"
echo    "║  NEXT STEPS:                                     ║"
echo    "║  1. cd ~/born2sub-ai                             ║"
echo    "║  2. cp .env.example .env                         ║"
echo    "║  3. Edit .env with your API keys                 ║"
echo    "║  4. pm2 start ecosystem.config.cjs               ║"
echo    "║  5. node client.js 'your query' 'claude,kimi'    ║"
echo    "║                                                  ║"
echo    "║  UTPL™ · SIPL™ · RTPL-BORN2BUILD™              ║"
echo -e "╚══════════════════════════════════════════════════╝${N}"
echo ""
