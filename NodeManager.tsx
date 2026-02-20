import { useState } from 'react';
import { 
  Server, 
  Plus, 
  Settings, 
  Power, 
  Trash2, 
  Cpu, 
  HardDrive, 
  Wifi,
  Globe,
  Clock,
  CheckCircle2,
  AlertCircle,
  RefreshCw,
  Terminal,
  Shield,
  Fingerprint
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

// ═══════════════════════════════════════════════════════════════════════════
// NODE MANAGER - Sovereign Node Deployment & Management
// ═══════════════════════════════════════════════════════════════════════════

interface Node {
  id: string;
  name: string;
  device: string;
  status: 'online' | 'offline' | 'syncing' | 'deploying';
  location: string;
  ip: string;
  cpu: number;
  memory: number;
  storage: number;
  uptime: string;
  lastSeen: string;
  trace: string;
  anchors: number;
}

const NodeManager = () => {
  const [nodes, setNodes] = useState<Node[]>([
    { 
      id: 'b2s-node-001', 
      name: 'Vegas Prime', 
      device: 'Galaxy S24 Ultra',
      status: 'online', 
      location: 'Las Vegas, NV',
      ip: '192.168.1.101',
      cpu: 34, 
      memory: 62, 
      storage: 45,
      uptime: '14d 7h 23m',
      lastSeen: '2s ago',
      trace: '0x9',
      anchors: 127
    },
    { 
      id: 'b2s-node-002', 
      name: 'Austin Edge', 
      device: 'Pixel 9 Pro',
      status: 'online', 
      location: 'Austin, TX',
      ip: '192.168.1.102',
      cpu: 28, 
      memory: 55, 
      storage: 38,
      uptime: '8d 12h 45m',
      lastSeen: '5s ago',
      trace: '0x9',
      anchors: 98
    },
    { 
      id: 'b2s-node-003', 
      name: 'Dallas Core', 
      device: 'iPhone 16 Pro',
      status: 'syncing', 
      location: 'Dallas, TX',
      ip: '192.168.1.103',
      cpu: 67, 
      memory: 78, 
      storage: 52,
      uptime: '3d 4h 12m',
      lastSeen: '1m ago',
      trace: '0x6',
      anchors: 84
    },
    { 
      id: 'b2s-node-004', 
      name: 'Houston Relay', 
      device: 'OnePlus 12',
      status: 'online', 
      location: 'Houston, TX',
      ip: '192.168.1.104',
      cpu: 22, 
      memory: 48, 
      storage: 31,
      uptime: '21d 9h 56m',
      lastSeen: '8s ago',
      trace: '0x9',
      anchors: 73
    },
    { 
      id: 'b2s-node-005', 
      name: 'San Antonio Node', 
      device: 'Xiaomi 14',
      status: 'online', 
      location: 'San Antonio, TX',
      ip: '192.168.1.105',
      cpu: 41, 
      memory: 63, 
      storage: 67,
      uptime: '5d 16h 34m',
      lastSeen: '12s ago',
      trace: '0x9',
      anchors: 45
    },
    { 
      id: 'b2s-node-006', 
      name: 'El Paso Gateway', 
      device: 'Nothing Phone 3',
      status: 'offline', 
      location: 'El Paso, TX',
      ip: '192.168.1.106',
      cpu: 0, 
      memory: 0, 
      storage: 0,
      uptime: '-',
      lastSeen: '2h ago',
      trace: '0x0',
      anchors: 0
    },
    { 
      id: 'b2s-node-007', 
      name: 'Fort Worth Link', 
      device: 'Zenfone 11',
      status: 'online', 
      location: 'Fort Worth, TX',
      ip: '192.168.1.107',
      cpu: 19, 
      memory: 42, 
      storage: 28,
      uptime: '11d 3h 18m',
      lastSeen: '3s ago',
      trace: '0x9',
      anchors: 32
    },
  ]);

  const [selectedNode, setSelectedNode] = useState<Node | null>(null);
  const [isDeploying, setIsDeploying] = useState(false);

  const getStatusBadge = (status: Node['status']) => {
    switch (status) {
      case 'online':
        return <Badge className="bg-green-500/10 border-green-500/30 text-green-400">Online</Badge>;
      case 'syncing':
        return <Badge className="bg-yellow-500/10 border-yellow-500/30 text-yellow-400">Syncing</Badge>;
      case 'deploying':
        return <Badge className="bg-blue-500/10 border-blue-500/30 text-blue-400">Deploying</Badge>;
      default:
        return <Badge className="bg-red-500/10 border-red-500/30 text-red-400">Offline</Badge>;
    }
  };

  const getStatusIcon = (status: Node['status']) => {
    switch (status) {
      case 'online':
        return <div className="status-dot status-online" />;
      case 'syncing':
      case 'deploying':
        return <div className="status-dot status-pending" />;
      default:
        return <div className="status-dot status-offline" />;
    }
  };

  const handleDeploy = async (nodeId: string) => {
    setIsDeploying(true);
    setNodes(prev => prev.map(n => 
      n.id === nodeId ? { ...n, status: 'deploying' } : n
    ));
    
    // Simulate deployment
    await new Promise(r => setTimeout(r, 3000));
    
    setNodes(prev => prev.map(n => 
      n.id === nodeId ? { ...n, status: 'online', trace: '0x9' } : n
    ));
    setIsDeploying(false);
  };

  const handlePowerToggle = (nodeId: string) => {
    setNodes(prev => prev.map(n => {
      if (n.id === nodeId) {
        return { ...n, status: n.status === 'offline' ? 'syncing' : 'offline' };
      }
      return n;
    }));
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold text-white mb-2">Node Manager</h2>
          <p className="text-gray-400">Deploy and manage sovereign nodes across your ecosystem</p>
        </div>
        <Dialog>
          <DialogTrigger asChild>
            <Button className="bg-[#00ff41] hover:bg-[#00cc33] text-black font-semibold">
              <Plus className="w-4 h-4 mr-2" />
              Add Node
            </Button>
          </DialogTrigger>
          <DialogContent className="bg-[#1a1a1a] border-white/10 text-white">
            <DialogHeader>
              <DialogTitle>Deploy New Sovereign Node</DialogTitle>
            </DialogHeader>
            <div className="space-y-4 py-4">
              <div className="space-y-2">
                <Label>Node Name</Label>
                <Input placeholder="e.g., Phoenix Prime" className="bg-white/5 border-white/10" />
              </div>
              <div className="space-y-2">
                <Label>Device Type</Label>
                <Select>
                  <SelectTrigger className="bg-white/5 border-white/10">
                    <SelectValue placeholder="Select device" />
                  </SelectTrigger>
                  <SelectContent className="bg-[#1a1a1a] border-white/10">
                    <SelectItem value="s24">Galaxy S24 Ultra</SelectItem>
                    <SelectItem value="pixel9">Pixel 9 Pro</SelectItem>
                    <SelectItem value="iphone16">iPhone 16 Pro</SelectItem>
                    <SelectItem value="oneplus12">OnePlus 12</SelectItem>
                    <SelectItem value="custom">Custom Device</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <Label>Location</Label>
                <Input placeholder="e.g., Phoenix, AZ" className="bg-white/5 border-white/10" />
              </div>
              <Button className="w-full bg-[#00ff41] hover:bg-[#00cc33] text-black font-semibold">
                <Fingerprint className="w-4 h-4 mr-2" />
                Initialize Deployment
              </Button>
            </div>
          </DialogContent>
        </Dialog>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-4 gap-4">
        <div className="glass-card p-4 text-center">
          <div className="text-3xl font-bold text-white">{nodes.length}</div>
          <div className="text-sm text-gray-400">Total Nodes</div>
        </div>
        <div className="glass-card p-4 text-center">
          <div className="text-3xl font-bold text-green-400">
            {nodes.filter(n => n.status === 'online').length}
          </div>
          <div className="text-sm text-gray-400">Online</div>
        </div>
        <div className="glass-card p-4 text-center">
          <div className="text-3xl font-bold text-yellow-400">
            {nodes.filter(n => n.status === 'syncing').length}
          </div>
          <div className="text-sm text-gray-400">Syncing</div>
        </div>
        <div className="glass-card p-4 text-center">
          <div className="text-3xl font-bold text-purple-400">
            {nodes.reduce((acc, n) => acc + n.anchors, 0).toLocaleString()}
          </div>
          <div className="text-sm text-gray-400">Total Anchors</div>
        </div>
      </div>

      {/* Node Grid */}
      <div className="grid grid-cols-2 gap-6">
        {nodes.map((node) => (
          <div 
            key={node.id}
            className={`glass-card p-6 hover:bg-white/[0.05] transition-all cursor-pointer ${
              selectedNode?.id === node.id ? 'ring-2 ring-[#00ff41]' : ''
            }`}
            onClick={() => setSelectedNode(node)}
          >
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center gap-3">
                {getStatusIcon(node.status)}
                <div>
                  <h3 className="font-semibold text-white">{node.name}</h3>
                  <p className="text-xs text-gray-500">{node.id}</p>
                </div>
              </div>
              <div className="flex items-center gap-2">
                {getStatusBadge(node.status)}
                <Badge variant="outline" className="border-[#00ff41]/30 text-[#00ff41]">
                  TRACE: {node.trace}
                </Badge>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4 mb-4">
              <div className="flex items-center gap-2 text-sm text-gray-400">
                <Server className="w-4 h-4" />
                {node.device}
              </div>
              <div className="flex items-center gap-2 text-sm text-gray-400">
                <Globe className="w-4 h-4" />
                {node.location}
              </div>
              <div className="flex items-center gap-2 text-sm text-gray-400">
                <Clock className="w-4 h-4" />
                {node.uptime}
              </div>
              <div className="flex items-center gap-2 text-sm text-gray-400">
                <Shield className="w-4 h-4" />
                {node.anchors} anchors
              </div>
            </div>

            {node.status !== 'offline' && (
              <div className="space-y-2 mb-4">
                <div className="flex justify-between text-xs">
                  <span className="text-gray-500">CPU</span>
                  <span className="text-white">{node.cpu}%</span>
                </div>
                <Progress value={node.cpu} className="h-1.5" />
                <div className="flex justify-between text-xs">
                  <span className="text-gray-500">Memory</span>
                  <span className="text-white">{node.memory}%</span>
                </div>
                <Progress value={node.memory} className="h-1.5" />
              </div>
            )}

            <div className="flex items-center gap-2">
              {node.status === 'offline' ? (
                <Button 
                  size="sm" 
                  className="flex-1 bg-[#00ff41] hover:bg-[#00cc33] text-black"
                  onClick={(e) => {
                    e.stopPropagation();
                    handleDeploy(node.id);
                  }}
                  disabled={isDeploying}
                >
                  <Power className="w-4 h-4 mr-2" />
                  Power On
                </Button>
              ) : (
                <Button 
                  size="sm" 
                  variant="outline"
                  className="flex-1 border-white/20 text-white hover:bg-white/5"
                  onClick={(e) => {
                    e.stopPropagation();
                    handlePowerToggle(node.id);
                  }}
                >
                  <Power className="w-4 h-4 mr-2" />
                  Power Off
                </Button>
              )}
              <Button 
                size="sm" 
                variant="outline"
                className="border-white/20 text-white hover:bg-white/5"
              >
                <Settings className="w-4 h-4" />
              </Button>
              <Button 
                size="sm" 
                variant="outline"
                className="border-red-500/30 text-red-400 hover:bg-red-500/10"
              >
                <Trash2 className="w-4 h-4" />
              </Button>
            </div>
          </div>
        ))}
      </div>

      {/* Selected Node Details */}
      {selectedNode && (
        <div className="glass-card p-6">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-white flex items-center gap-2">
              <Terminal className="w-5 h-5 text-[#00ff41]" />
              Node Details: {selectedNode.name}
            </h3>
            <Button 
              variant="ghost" 
              size="sm"
              onClick={() => setSelectedNode(null)}
              className="text-gray-400 hover:text-white"
            >
              Close
            </Button>
          </div>

          <div className="grid grid-cols-3 gap-6">
            <div className="space-y-4">
              <h4 className="text-sm font-medium text-gray-400 uppercase">Identity</h4>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-500">Node ID</span>
                  <span className="text-white font-mono">{selectedNode.id}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-500">Device</span>
                  <span className="text-white">{selectedNode.device}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-500">Location</span>
                  <span className="text-white">{selectedNode.location}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-500">IP Address</span>
                  <span className="text-white font-mono">{selectedNode.ip}</span>
                </div>
              </div>
            </div>

            <div className="space-y-4">
              <h4 className="text-sm font-medium text-gray-400 uppercase">Status</h4>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-500">State</span>
                  {getStatusBadge(selectedNode.status)}
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-500">TRACE</span>
                  <Badge variant="outline" className="border-[#00ff41]/30 text-[#00ff41]">
                    {selectedNode.trace}
                  </Badge>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-500">Uptime</span>
                  <span className="text-white">{selectedNode.uptime}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-500">Last Seen</span>
                  <span className="text-white">{selectedNode.lastSeen}</span>
                </div>
              </div>
            </div>

            <div className="space-y-4">
              <h4 className="text-sm font-medium text-gray-400 uppercase">Anchors</h4>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-500">Total Anchors</span>
                  <span className="text-white">{selectedNode.anchors}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-500">Chains</span>
                  <span className="text-white">6</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-500">IPFS Peers</span>
                  <span className="text-white">247</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-500">BrockBox</span>
                  <span className="text-blue-400">Connected</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default NodeManager;
