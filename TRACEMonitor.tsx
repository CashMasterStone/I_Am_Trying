import { useState, useEffect, useRef } from 'react';
import { 
  Activity, 
  Play, 
  Pause, 
  RotateCcw,
  Terminal,
  Shield,
  Cpu,
  HardDrive,
  Wifi,
  CheckCircle2,
  AlertCircle,
  Radio,
  Zap,
  Fingerprint
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';

// ═══════════════════════════════════════════════════════════════════════════
// TRACE MONITOR - Real-time State Machine Visualization
// TRACE Chain: 0x0 → 0x3 → 0x6 → 0x9
// ═══════════════════════════════════════════════════════════════════════════

type TraceState = '0x0' | '0x3' | '0x6' | '0x9';
type PhaseType = 'INIT' | 'SOVEREIGN_INIT' | 'IPFS_ANCHOR' | 'MULTICHAIN_BIND';

interface LogEntry {
  timestamp: string;
  message: string;
  type: 'info' | 'success' | 'trace' | 'error' | 'audit';
}

interface ChainAnchor {
  chain: string;
  txHash: string;
  block: number;
  status: 'pending' | 'confirmed' | 'failed';
}

const traceStates: Record<TraceState, { next: TraceState | null; label: string; color: string; description: string }> = {
  '0x0': { next: '0x3', label: 'SOURCE', color: '#00ff41', description: 'System initialization and verification' },
  '0x3': { next: '0x6', label: 'PROCESS', color: '#00cc33', description: 'IPFS anchoring and content addressing' },
  '0x6': { next: '0x9', label: 'ALIGN', color: '#00aa22', description: 'Multi-chain binding and verification' },
  '0x9': { next: null, label: 'COMPLETE', color: '#008811', description: 'Deployment complete - Node operational' },
};

const TRACEMonitor = () => {
  const [trace, setTrace] = useState<TraceState>('0x0');
  const [phase, setPhase] = useState<PhaseType>('INIT');
  const [isRunning, setIsRunning] = useState(false);
  const [progress, setProgress] = useState(0);
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [ipfsPID, setIpfsPID] = useState<string | null>(null);
  const [chainAnchors, setChainAnchors] = useState<ChainAnchor[]>([]);
  const [systemHealth, setSystemHealth] = useState<any>({});
  const logsEndRef = useRef<HTMLDivElement>(null);

  const addLog = (message: string, type: LogEntry['type'] = 'info') => {
    const timestamp = new Date().toISOString().split('T')[1].slice(0, 12);
    setLogs(prev => [...prev, { timestamp, message, type }]);
  };

  const scrollToBottom = () => {
    logsEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [logs]);

  useEffect(() => {
    addLog('Born2Sub TRACE Monitor initialized', 'info');
    addLog('Zero-Trust Protocol: ACTIVE', 'info');
    addLog('Waiting for deployment trigger...', 'info');
  }, []);

  const transitionTrace = (newTrace: TraceState) => {
    const currentState = traceStates[trace];
    const newState = traceStates[newTrace];
    addLog(`TRACE: ${currentState.label} → ${newState.label}`, 'trace');
    setTrace(newTrace);
  };

  const simulateDeployment = async () => {
    if (isRunning || trace === '0x9') return;
    
    setIsRunning(true);
    setProgress(0);
    addLog('═══════════════════════════════════════', 'info');
    addLog('DEPLOYMENT SEQUENCE INITIATED', 'success');
    addLog('═══════════════════════════════════════', 'info');

    // Phase 1: SOVEREIGN_INIT
    if (trace === '0x0') {
      addLog('Phase 1: SOVEREIGN_INIT', 'info');
      setPhase('SOVEREIGN_INIT');
      
      for (let i = 0; i <= 33; i++) {
        setProgress(i);
        await new Promise(r => setTimeout(r, 50));
      }
      
      setSystemHealth({
        cpu: 'Snapdragon 8 Gen 3',
        ram: '12GB LPDDR5X',
        storage: '256GB UFS 4.0',
        network: '5G + WiFi 7'
      });
      
      addLog('✓ Hardware verification complete', 'success');
      addLog('✓ CPU: Snapdragon 8 Gen 3', 'success');
      addLog('✓ RAM: 12GB LPDDR5X', 'success');
      addLog('✓ Storage: 256GB UFS 4.0', 'success');
      addLog('✓ Network: 5G + WiFi 7', 'success');
      
      transitionTrace('0x3');
      await new Promise(r => setTimeout(r, 500));
    }

    // Phase 2: IPFS_ANCHOR
    if (trace === '0x3') {
      addLog('Phase 2: IPFS_ANCHOR', 'info');
      setPhase('IPFS_ANCHOR');
      
      for (let i = 34; i <= 66; i++) {
        setProgress(i);
        await new Promise(r => setTimeout(r, 50));
      }
      
      const mockIPFSPID = `Qm${Math.random().toString(36).substring(2, 15)}${Math.random().toString(36).substring(2, 15)}`;
      setIpfsPID(mockIPFSPID);
      
      addLog('✓ IPFS node initialized', 'success');
      addLog(`✓ Content PID: ${mockIPFSPID.substring(0, 20)}...`, 'success');
      addLog('✓ DHT bootstrap complete', 'success');
      addLog('✓ 247 peers connected', 'success');
      
      transitionTrace('0x6');
      await new Promise(r => setTimeout(r, 500));
    }

    // Phase 3: MULTICHAIN_BIND
    if (trace === '0x6') {
      addLog('Phase 3: MULTICHAIN_BIND', 'info');
      setPhase('MULTICHAIN_BIND');
      
      for (let i = 67; i <= 100; i++) {
        setProgress(i);
        await new Promise(r => setTimeout(r, 50));
      }
      
      const chains = ['Solana', 'Ethereum', 'Polygon', 'Base', 'Bitcoin', 'Sonic'];
      const anchors: ChainAnchor[] = chains.map(chain => ({
        chain,
        txHash: `0x${Math.random().toString(16).substring(2, 42)}`,
        block: Math.floor(Math.random() * 100000000),
        status: 'confirmed'
      }));
      
      setChainAnchors(anchors);
      
      for (const anchor of anchors) {
        addLog(`✓ ${anchor.chain}: Block #${anchor.block.toLocaleString()}`, 'success');
        await new Promise(r => setTimeout(r, 200));
      }
      
      addLog('✓ All chain anchors confirmed', 'success');
      addLog('✓ Merkle root generated', 'success');
      
      // BrockBox Audit Integration
      addLog('═══════════════════════════════════════', 'audit');
      addLog('BROCKBOX AUDIT INTEGRATION', 'audit');
      addLog('═══════════════════════════════════════', 'audit');
      addLog('✓ Physics-anchored proof generated', 'audit');
      addLog('✓ NIST constants verified', 'audit');
      addLog('✓ On-chain notarization complete', 'audit');
      addLog('✓ Audit trail immutable', 'audit');
      
      transitionTrace('0x9');
    }

    addLog('═══════════════════════════════════════', 'success');
    addLog('🎉 DEPLOYMENT COMPLETE', 'success');
    addLog('Sovereign Node Operational', 'success');
    addLog('═══════════════════════════════════════', 'success');
    
    setIsRunning(false);
  };

  const resetDeployment = () => {
    setTrace('0x0');
    setPhase('INIT');
    setProgress(0);
    setIpfsPID(null);
    setChainAnchors([]);
    setSystemHealth({});
    setLogs([]);
    addLog('TRACE state machine reset', 'info');
    addLog('Ready for new deployment', 'info');
  };

  const getLogColor = (type: LogEntry['type']) => {
    switch (type) {
      case 'success': return 'text-[#00ff41]';
      case 'trace': return 'text-[#00cc33]';
      case 'error': return 'text-red-400';
      case 'audit': return 'text-blue-400';
      default: return 'text-gray-400';
    }
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold text-white mb-2">TRACE Monitor</h2>
          <p className="text-gray-400">Real-time state machine visualization and deployment control</p>
        </div>
        <div className="flex items-center gap-3">
          <Button 
            variant="outline" 
            onClick={resetDeployment}
            className="border-white/20 text-white hover:bg-white/5"
          >
            <RotateCcw className="w-4 h-4 mr-2" />
            Reset
          </Button>
          <Button 
            onClick={simulateDeployment}
            disabled={isRunning || trace === '0x9'}
            className={`${
              trace === '0x9' 
                ? 'bg-green-500/20 text-green-400 cursor-not-allowed' 
                : 'bg-[#00ff41] hover:bg-[#00cc33] text-black'
            } font-semibold`}
          >
            {isRunning ? (
              <>
                <Pause className="w-4 h-4 mr-2" />
                Deploying...
              </>
            ) : trace === '0x9' ? (
              <>
                <CheckCircle2 className="w-4 h-4 mr-2" />
                Deployed
              </>
            ) : (
              <>
                <Play className="w-4 h-4 mr-2" />
                Deploy Node
              </>
            )}
          </Button>
        </div>
      </div>

      {/* TRACE State Visualization */}
      <div className="glass-card p-8">
        <div className="flex items-center justify-between mb-8">
          <h3 className="text-lg font-semibold text-white flex items-center gap-2">
            <Activity className="w-5 h-5 text-[#00ff41]" />
            TRACE State Machine
          </h3>
          <div className="flex items-center gap-4">
            <Badge className="bg-[#00ff41]/10 border-[#00ff41]/30 text-[#00ff41]">
              TRACE: {trace}
            </Badge>
            <Badge className="bg-blue-500/10 border-blue-500/30 text-blue-400">
              Phase: {phase}
            </Badge>
          </div>
        </div>

        {/* State Circles */}
        <div className="flex items-center justify-between mb-8">
          {(Object.keys(traceStates) as TraceState[]).map((stateKey, idx, arr) => {
            const state = traceStates[stateKey];
            const isActive = trace === stateKey;
            const isCompleted = (() => {
              const states = Object.keys(traceStates) as TraceState[];
              return states.indexOf(trace) > states.indexOf(stateKey);
            })();
            
            return (
              <div key={stateKey} className="flex items-center flex-1">
                <div className="flex flex-col items-center flex-1">
                  <div 
                    className={`w-20 h-20 rounded-full flex items-center justify-center text-xl font-bold transition-all duration-500 ${
                      isActive 
                        ? 'glow-green scale-110' 
                        : isCompleted 
                          ? '' 
                          : ''
                    }`}
                    style={{
                      backgroundColor: isActive ? state.color : isCompleted ? `${state.color}40` : 'rgba(255,255,255,0.05)',
                      color: isActive ? '#0a0a0a' : isCompleted ? state.color : '#666',
                      boxShadow: isActive ? `0 0 30px ${state.color}60` : 'none'
                    }}
                  >
                    {isCompleted ? <CheckCircle2 className="w-8 h-8" /> : stateKey}
                  </div>
                  <span 
                    className={`mt-3 text-sm font-medium transition-colors ${
                      isActive || isCompleted ? 'text-[#00ff41]' : 'text-gray-500'
                    }`}
                  >
                    {state.label}
                  </span>
                  <span className="text-xs text-gray-600 mt-1 text-center max-w-[120px]">
                    {state.description}
                  </span>
                </div>
                {idx < arr.length - 1 && (
                  <div className="flex-1 h-1 mx-4 relative">
                    <div className="absolute inset-0 bg-white/10 rounded-full" />
                    <div 
                      className="absolute inset-y-0 left-0 bg-gradient-to-r from-[#00ff41] to-[#00cc33] rounded-full transition-all duration-500"
                      style={{ 
                        width: isCompleted ? '100%' : isActive ? `${progress}%` : '0%'
                      }}
                    />
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {/* Progress Bar */}
        <div className="space-y-2">
          <div className="flex justify-between text-sm">
            <span className="text-gray-400">Deployment Progress</span>
            <span className="text-[#00ff41] font-medium">{progress}%</span>
          </div>
          <Progress value={progress} className="h-3" />
        </div>
      </div>

      <div className="grid grid-cols-3 gap-6">
        {/* System Health */}
        <div className="glass-card p-6">
          <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
            <Cpu className="w-5 h-5 text-[#00ff41]" />
            System Health
          </h3>
          
          {systemHealth.cpu ? (
            <div className="space-y-4">
              <div className="flex items-center justify-between p-3 rounded-lg bg-white/[0.03]">
                <div className="flex items-center gap-3">
                  <Cpu className="w-4 h-4 text-gray-500" />
                  <span className="text-sm text-gray-400">CPU</span>
                </div>
                <span className="text-sm text-[#00ff41]">{systemHealth.cpu}</span>
              </div>
              <div className="flex items-center justify-between p-3 rounded-lg bg-white/[0.03]">
                <div className="flex items-center gap-3">
                  <Zap className="w-4 h-4 text-gray-500" />
                  <span className="text-sm text-gray-400">RAM</span>
                </div>
                <span className="text-sm text-[#00ff41]">{systemHealth.ram}</span>
              </div>
              <div className="flex items-center justify-between p-3 rounded-lg bg-white/[0.03]">
                <div className="flex items-center gap-3">
                  <HardDrive className="w-4 h-4 text-gray-500" />
                  <span className="text-sm text-gray-400">Storage</span>
                </div>
                <span className="text-sm text-[#00ff41]">{systemHealth.storage}</span>
              </div>
              <div className="flex items-center justify-between p-3 rounded-lg bg-white/[0.03]">
                <div className="flex items-center gap-3">
                  <Wifi className="w-4 h-4 text-gray-500" />
                  <span className="text-sm text-gray-400">Network</span>
                </div>
                <span className="text-sm text-[#00ff41]">{systemHealth.network}</span>
              </div>
            </div>
          ) : (
            <div className="text-center py-8 text-gray-500">
              <Cpu className="w-12 h-12 mx-auto mb-3 opacity-30" />
              <p className="text-sm">System health data will appear after SOVEREIGN_INIT</p>
            </div>
          )}
        </div>

        {/* IPFS Status */}
        <div className="glass-card p-6">
          <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
            <Fingerprint className="w-5 h-5 text-purple-400" />
            IPFS Status
          </h3>
          
          {ipfsPID ? (
            <div className="space-y-4">
              <div className="p-4 rounded-lg bg-purple-500/5 border border-purple-500/20">
                <div className="text-xs text-gray-500 mb-2">Content Identifier (PID)</div>
                <div className="font-mono text-sm text-purple-400 break-all">
                  {ipfsPID}
                </div>
              </div>
              
              <div className="space-y-2">
                <div className="flex items-center justify-between p-2 rounded bg-white/[0.03]">
                  <span className="text-sm text-gray-400">Status</span>
                  <Badge className="bg-green-500/10 border-green-500/30 text-green-400">
                    Active
                  </Badge>
                </div>
                <div className="flex items-center justify-between p-2 rounded bg-white/[0.03]">
                  <span className="text-sm text-gray-400">Peers</span>
                  <span className="text-sm text-white">247</span>
                </div>
                <div className="flex items-center justify-between p-2 rounded bg-white/[0.03]">
                  <span className="text-sm text-gray-400">Bandwidth</span>
                  <span className="text-sm text-white">12.4 MB/s</span>
                </div>
                <div className="flex items-center justify-between p-2 rounded bg-white/[0.03]">
                  <span className="text-sm text-gray-400">Pinned</span>
                  <span className="text-sm text-white">1,247 objects</span>
                </div>
              </div>
            </div>
          ) : (
            <div className="text-center py-8 text-gray-500">
              <Fingerprint className="w-12 h-12 mx-auto mb-3 opacity-30" />
              <p className="text-sm">IPFS data will appear after IPFS_ANCHOR phase</p>
            </div>
          )}
        </div>

        {/* Chain Anchors */}
        <div className="glass-card p-6">
          <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
            <Radio className="w-5 h-5 text-blue-400" />
            Chain Anchors
          </h3>
          
          {chainAnchors.length > 0 ? (
            <div className="space-y-2 max-h-[280px] overflow-y-auto">
              {chainAnchors.map((anchor, idx) => (
                <div 
                  key={idx}
                  className="p-3 rounded-lg bg-white/[0.03] border border-white/[0.08]"
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-medium text-white">{anchor.chain}</span>
                    <Badge className="bg-green-500/10 border-green-500/30 text-green-400 text-xs">
                      {anchor.status}
                    </Badge>
                  </div>
                  <div className="text-xs text-gray-500 mb-1">
                    Block #{anchor.block.toLocaleString()}
                  </div>
                  <div className="font-mono text-xs text-gray-600 truncate">
                    {anchor.txHash}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8 text-gray-500">
              <Radio className="w-12 h-12 mx-auto mb-3 opacity-30" />
              <p className="text-sm">Chain anchors will appear after MULTICHAIN_BIND phase</p>
            </div>
          )}
        </div>
      </div>

      {/* Deployment Log */}
      <div className="glass-card p-6">
        <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
          <Terminal className="w-5 h-5 text-[#00ff41]" />
          Deployment Log
        </h3>
        
        <div className="terminal h-64 overflow-y-auto font-mono text-sm">
          {logs.map((log, idx) => (
            <div key={idx} className="terminal-line">
              <span className="terminal-timestamp">[{log.timestamp}]</span>{' '}
              <span className={getLogColor(log.type)}>{log.message}</span>
            </div>
          ))}
          <div ref={logsEndRef} />
        </div>
      </div>
    </div>
  );
};

export default TRACEMonitor;
