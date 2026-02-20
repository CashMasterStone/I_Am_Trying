import { useState, useEffect } from 'react';
import { 
  Server, 
  Link2, 
  Activity, 
  Shield, 
  Cpu, 
  HardDrive, 
  Wifi,
  CheckCircle2,
  AlertCircle,
  Clock,
  TrendingUp,
  Globe,
  Zap,
  Radio
} from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Separator } from '@/components/ui/separator';

// ═══════════════════════════════════════════════════════════════════════════
// ECOSYSTEM DASHBOARD - Real-time System Overview
// ═══════════════════════════════════════════════════════════════════════════

interface SystemStatus {
  trace: string;
  phase: string;
  nodes: number;
  chains: number;
  brockbox: string;
  lastSync: string;
}

interface EcosystemDashboardProps {
  systemStatus: SystemStatus;
}

interface NodeStatus {
  id: string;
  name: string;
  status: 'online' | 'syncing' | 'offline';
  cpu: number;
  memory: number;
  storage: number;
  uptime: string;
  location: string;
  lastSeen: string;
}

interface ChainStatus {
  name: string;
  symbol: string;
  status: 'connected' | 'syncing' | 'disconnected';
  blockHeight: number;
  latency: number;
  anchors: number;
  color: string;
}

const EcosystemDashboard = ({ systemStatus }: EcosystemDashboardProps) => {
  const [nodes, setNodes] = useState<NodeStatus[]>([
    { id: 'node-001', name: 'Galaxy S24 Ultra', status: 'online', cpu: 34, memory: 62, storage: 45, uptime: '14d 7h 23m', location: 'Las Vegas, NV', lastSeen: '2s ago' },
    { id: 'node-002', name: 'Pixel 9 Pro', status: 'online', cpu: 28, memory: 55, storage: 38, uptime: '8d 12h 45m', location: 'Austin, TX', lastSeen: '5s ago' },
    { id: 'node-003', name: 'iPhone 16 Pro', status: 'syncing', cpu: 67, memory: 78, storage: 52, uptime: '3d 4h 12m', location: 'Dallas, TX', lastSeen: '1m ago' },
    { id: 'node-004', name: 'OnePlus 12', status: 'online', cpu: 22, memory: 48, storage: 31, uptime: '21d 9h 56m', location: 'Houston, TX', lastSeen: '8s ago' },
    { id: 'node-005', name: 'Xiaomi 14', status: 'online', cpu: 41, memory: 63, storage: 67, uptime: '5d 16h 34m', location: 'San Antonio, TX', lastSeen: '12s ago' },
    { id: 'node-006', name: 'Nothing Phone 3', status: 'offline', cpu: 0, memory: 0, storage: 0, uptime: '-', location: 'El Paso, TX', lastSeen: '2h ago' },
    { id: 'node-007', name: 'Zenfone 11', status: 'online', cpu: 19, memory: 42, storage: 28, uptime: '11d 3h 18m', location: 'Fort Worth, TX', lastSeen: '3s ago' },
  ]);

  const [chains, setChains] = useState<ChainStatus[]>([
    { name: 'Solana', symbol: 'SOL', status: 'connected', blockHeight: 284739421, latency: 12, anchors: 127, color: '#9945ff' },
    { name: 'Ethereum', symbol: 'ETH', status: 'connected', blockHeight: 19847231, latency: 45, anchors: 98, color: '#627eea' },
    { name: 'Polygon', symbol: 'MATIC', status: 'connected', blockHeight: 61284739, latency: 8, anchors: 84, color: '#8247e5' },
    { name: 'Base', symbol: 'BASE', status: 'connected', blockHeight: 18472931, latency: 15, anchors: 73, color: '#0052ff' },
    { name: 'Bitcoin', symbol: 'BTC', status: 'syncing', blockHeight: 828471, latency: 120, anchors: 45, color: '#f7931a' },
    { name: 'Sonic', symbol: 'S', status: 'connected', blockHeight: 4729381, latency: 6, anchors: 32, color: '#f4f4f5' },
  ]);

  const [metrics, setMetrics] = useState({
    totalAnchors: 459,
    proofsVerified: 2847,
    dataStored: '2.4 TB',
    networkThroughput: '1.2 GB/s',
    avgLatency: 18,
    syncProgress: 98.7
  });

  // Simulate real-time updates
  useEffect(() => {
    const interval = setInterval(() => {
      setNodes(prev => prev.map(node => ({
        ...node,
        cpu: node.status === 'online' ? Math.floor(Math.random() * 40) + 15 : node.cpu,
        memory: node.status === 'online' ? Math.floor(Math.random() * 30) + 40 : node.memory,
      })));
      
      setMetrics(prev => ({
        ...prev,
        proofsVerified: prev.proofsVerified + Math.floor(Math.random() * 3),
        avgLatency: Math.floor(Math.random() * 20) + 10
      }));
    }, 3000);
    
    return () => clearInterval(interval);
  }, []);

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'online':
      case 'connected':
        return <div className="status-dot status-online" />;
      case 'syncing':
        return <div className="status-dot status-pending" />;
      default:
        return <div className="status-dot status-offline" />;
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'online':
      case 'connected':
        return <Badge className="bg-green-500/10 border-green-500/30 text-green-400">Online</Badge>;
      case 'syncing':
        return <Badge className="bg-yellow-500/10 border-yellow-500/30 text-yellow-400">Syncing</Badge>;
      default:
        return <Badge className="bg-red-500/10 border-red-500/30 text-red-400">Offline</Badge>;
    }
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold text-white mb-2">Ecosystem Dashboard</h2>
          <p className="text-gray-400">Real-time overview of all sovereign nodes and chain anchors</p>
        </div>
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 px-4 py-2 bg-[#00ff41]/10 border border-[#00ff41]/20 rounded-lg">
            <Radio className="w-4 h-4 text-[#00ff41]" />
            <span className="text-sm text-[#00ff41] font-medium">Live</span>
          </div>
          <div className="text-right">
            <div className="text-xs text-gray-500">Last Sync</div>
            <div className="text-sm text-white">{new Date(systemStatus.lastSync).toLocaleTimeString()}</div>
          </div>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-6 gap-4">
        {[
          { label: 'Total Anchors', value: metrics.totalAnchors.toString(), icon: Link2, color: 'text-purple-400' },
          { label: 'Proofs Verified', value: metrics.proofsVerified.toLocaleString(), icon: CheckCircle2, color: 'text-blue-400' },
          { label: 'Data Stored', value: metrics.dataStored, icon: HardDrive, color: 'text-amber-400' },
          { label: 'Network I/O', value: metrics.networkThroughput, icon: Wifi, color: 'text-cyan-400' },
          { label: 'Avg Latency', value: `${metrics.avgLatency}ms`, icon: Clock, color: 'text-pink-400' },
          { label: 'Sync Progress', value: `${metrics.syncProgress}%`, icon: TrendingUp, color: 'text-green-400' },
        ].map((metric, idx) => (
          <div key={idx} className="glass-card p-4">
            <metric.icon className={`w-5 h-5 ${metric.color} mb-2`} />
            <div className="text-2xl font-bold text-white">{metric.value}</div>
            <div className="text-xs text-gray-500">{metric.label}</div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-2 gap-8">
        {/* Nodes Panel */}
        <div className="glass-card p-6">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-white flex items-center gap-2">
              <Server className="w-5 h-5 text-[#00ff41]" />
              Sovereign Nodes
            </h3>
            <Badge className="bg-[#00ff41]/10 border-[#00ff41]/30 text-[#00ff41]">
              {nodes.filter(n => n.status === 'online').length}/{nodes.length} Online
            </Badge>
          </div>

          <div className="space-y-4">
            {nodes.map((node) => (
              <div 
                key={node.id} 
                className={`p-4 rounded-xl border transition-all ${
                  node.status === 'online' 
                    ? 'bg-white/[0.03] border-white/[0.08] hover:bg-white/[0.05]' 
                    : node.status === 'syncing'
                    ? 'bg-yellow-500/5 border-yellow-500/20'
                    : 'bg-red-500/5 border-red-500/20'
                }`}
              >
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-3">
                    {getStatusIcon(node.status)}
                    <div>
                      <div className="font-medium text-white">{node.name}</div>
                      <div className="text-xs text-gray-500">{node.id}</div>
                    </div>
                  </div>
                  {getStatusBadge(node.status)}
                </div>

                {node.status !== 'offline' && (
                  <div className="space-y-2">
                    <div className="flex items-center gap-4 text-xs">
                      <div className="flex-1">
                        <div className="flex justify-between mb-1">
                          <span className="text-gray-500">CPU</span>
                          <span className="text-white">{node.cpu}%</span>
                        </div>
                        <Progress value={node.cpu} className="h-1" />
                      </div>
                      <div className="flex-1">
                        <div className="flex justify-between mb-1">
                          <span className="text-gray-500">Memory</span>
                          <span className="text-white">{node.memory}%</span>
                        </div>
                        <Progress value={node.memory} className="h-1" />
                      </div>
                    </div>
                    <div className="flex items-center gap-4 text-xs text-gray-500">
                      <span className="flex items-center gap-1">
                        <Globe className="w-3 h-3" />
                        {node.location}
                      </span>
                      <span className="flex items-center gap-1">
                        <Clock className="w-3 h-3" />
                        {node.uptime}
                      </span>
                      <span className="ml-auto">{node.lastSeen}</span>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Chains Panel */}
        <div className="glass-card p-6">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-white flex items-center gap-2">
              <Link2 className="w-5 h-5 text-purple-400" />
              Chain Anchors
            </h3>
            <Badge className="bg-purple-500/10 border-purple-500/30 text-purple-400">
              {chains.filter(c => c.status === 'connected').length}/{chains.length} Connected
            </Badge>
          </div>

          <div className="space-y-3">
            {chains.map((chain) => (
              <div 
                key={chain.name}
                className="p-4 rounded-xl bg-white/[0.03] border border-white/[0.08] hover:bg-white/[0.05] transition-all"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div 
                      className="w-10 h-10 rounded-lg flex items-center justify-center font-bold text-sm"
                      style={{ backgroundColor: `${chain.color}20`, color: chain.color }}
                    >
                      {chain.symbol}
                    </div>
                    <div>
                      <div className="font-medium text-white">{chain.name}</div>
                      <div className="text-xs text-gray-500">
                        Block #{chain.blockHeight.toLocaleString()}
                      </div>
                    </div>
                  </div>
                  <div className="text-right">
                    {getStatusBadge(chain.status)}
                    <div className="text-xs text-gray-500 mt-1">
                      {chain.latency}ms • {chain.anchors} anchors
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* BrockBox Integration Status */}
          <div className="mt-6 p-4 rounded-xl bg-blue-500/5 border border-blue-500/20">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg bg-blue-500/20 flex items-center justify-center">
                  <Shield className="w-5 h-5 text-blue-400" />
                </div>
                <div>
                  <div className="font-medium text-white">BrockBox Audit</div>
                  <div className="text-xs text-gray-500">Physics-anchored proofs</div>
                </div>
              </div>
              <div className="text-right">
                <Badge className="bg-blue-500/10 border-blue-500/30 text-blue-400">
                  Connected
                </Badge>
                <div className="text-xs text-blue-400 mt-1">
                  459 proofs verified
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* System Health */}
      <div className="glass-card p-6">
        <h3 className="text-lg font-semibold text-white mb-6 flex items-center gap-2">
          <Activity className="w-5 h-5 text-[#00ff41]" />
          System Health
        </h3>
        
        <div className="grid grid-cols-4 gap-6">
          <div className="text-center">
            <div className="relative w-24 h-24 mx-auto mb-3">
              <svg className="w-full h-full transform -rotate-90">
                <circle cx="48" cy="48" r="40" stroke="rgba(255,255,255,0.1)" strokeWidth="8" fill="none" />
                <circle cx="48" cy="48" r="40" stroke="#00ff41" strokeWidth="8" fill="none"
                  strokeDasharray={`${2 * Math.PI * 40}`}
                  strokeDashoffset={`${2 * Math.PI * 40 * (1 - 0.94)}`}
                  strokeLinecap="round"
                />
              </svg>
              <div className="absolute inset-0 flex items-center justify-center">
                <span className="text-2xl font-bold text-white">94%</span>
              </div>
            </div>
            <div className="text-sm text-gray-400">Overall Health</div>
          </div>

          <div className="space-y-4">
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-gray-400">Node Uptime</span>
                <span className="text-[#00ff41]">99.7%</span>
              </div>
              <Progress value={99.7} className="h-2" />
            </div>
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-gray-400">Chain Sync</span>
                <span className="text-purple-400">98.5%</span>
              </div>
              <Progress value={98.5} className="h-2" />
            </div>
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-gray-400">BrockBox Bridge</span>
                <span className="text-blue-400">100%</span>
              </div>
              <Progress value={100} className="h-2" />
            </div>
          </div>

          <div className="col-span-2 space-y-3">
            {[
              { label: 'IPFS Peers', value: '247', status: 'healthy', icon: Globe },
              { label: 'Network I/O', value: '1.2 GB/s ↓ / 340 MB/s ↑', status: 'healthy', icon: Wifi },
              { label: 'Storage Available', value: '1.8 TB / 4.2 TB', status: 'warning', icon: HardDrive },
              { label: 'Proof Queue', value: '12 pending', status: 'healthy', icon: Shield },
            ].map((item, idx) => (
              <div key={idx} className="flex items-center justify-between p-3 rounded-lg bg-white/[0.03]">
                <div className="flex items-center gap-3">
                  <item.icon className="w-4 h-4 text-gray-500" />
                  <span className="text-sm text-gray-400">{item.label}</span>
                </div>
                <div className="flex items-center gap-3">
                  <span className="text-sm text-white">{item.value}</span>
                  <div className={`w-2 h-2 rounded-full ${
                    item.status === 'healthy' ? 'bg-green-400' : 'bg-yellow-400'
                  }`} />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default EcosystemDashboard;
