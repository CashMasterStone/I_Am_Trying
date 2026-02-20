import { useState, useEffect } from 'react';
import { 
  Shield, 
  Cpu, 
  Link2, 
  Activity, 
  Globe, 
  Zap,
  Menu,
  X,
  ChevronRight,
  Server,
  Fingerprint,
  Lock,
  Radio
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import HeroSection from '@/sections/HeroSection';
import EcosystemDashboard from '@/sections/EcosystemDashboard';
import TRACEMonitor from '@/sections/TRACEMonitor';
import NodeManager from '@/sections/NodeManager';
import BrockBoxBridge from '@/sections/BrockBoxBridge';
import ChainExplorer from '@/sections/ChainExplorer';
import AuditTrail from '@/sections/AuditTrail';
import Footer from '@/sections/Footer';

// ═══════════════════════════════════════════════════════════════════════════
// BORN2SUB.X ECOSYSTEM - MAIN APPLICATION
// Copyright © 2026 Cyrus Makai Schoonover | Born2Build, LLC
// Integrated with BrockBox.com - Kyle Brockley
// RTPL-BORN2BUILD™ | SIPL™ Licensed
// TRACE Chain: 0x0 → SOVEREIGN_INIT → IPFS_ANCHOR → MULTICHAIN_BIND → BROCKBOX_AUDIT
// ═══════════════════════════════════════════════════════════════════════════

type ViewType = 'overview' | 'trace' | 'nodes' | 'brockbox' | 'chains' | 'audit';

interface NavItem {
  id: ViewType;
  label: string;
  icon: React.ElementType;
  badge?: string;
}

const navItems: NavItem[] = [
  { id: 'overview', label: 'Ecosystem', icon: Globe },
  { id: 'trace', label: 'TRACE Monitor', icon: Activity, badge: 'LIVE' },
  { id: 'nodes', label: 'Node Manager', icon: Server },
  { id: 'brockbox', label: 'BrockBox Bridge', icon: Link2, badge: 'NEW' },
  { id: 'chains', label: 'Chain Explorer', icon: Link2 },
  { id: 'audit', label: 'Audit Trail', icon: Shield },
];

function App() {
  const [currentView, setCurrentView] = useState<ViewType>('overview');
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [systemStatus, setSystemStatus] = useState({
    trace: '0x9',
    phase: 'MULTICHAIN_BIND',
    nodes: 7,
    chains: 6,
    brockbox: 'connected',
    lastSync: new Date().toISOString()
  });

  // Simulate live system updates
  useEffect(() => {
    const interval = setInterval(() => {
      setSystemStatus(prev => ({
        ...prev,
        lastSync: new Date().toISOString()
      }));
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const renderView = () => {
    switch (currentView) {
      case 'overview':
        return <EcosystemDashboard systemStatus={systemStatus} />;
      case 'trace':
        return <TRACEMonitor />;
      case 'nodes':
        return <NodeManager />;
      case 'brockbox':
        return <BrockBoxBridge />;
      case 'chains':
        return <ChainExplorer />;
      case 'audit':
        return <AuditTrail />;
      default:
        return <EcosystemDashboard systemStatus={systemStatus} />;
    }
  };

  return (
    <div className="min-h-screen bg-[#0a0a0a] text-gray-200 flex">
      {/* Sidebar Navigation */}
      <aside 
        className={`fixed left-0 top-0 h-full bg-[#0f0f0f] border-r border-white/[0.08] z-50 transition-all duration-300 ${
          sidebarOpen ? 'w-72' : 'w-20'
        }`}
      >
        {/* Logo Area */}
        <div className="p-6 border-b border-white/[0.08]">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[#00ff41] to-[#00cc33] flex items-center justify-center flex-shrink-0">
              <Fingerprint className="w-6 h-6 text-black" />
            </div>
            {sidebarOpen && (
              <div className="animate-fade-in">
                <h1 className="font-bold text-white text-lg leading-tight">Born2Sub.X</h1>
                <p className="text-xs text-[#00ff41]">Sovereign Ecosystem</p>
              </div>
            )}
          </div>
        </div>

        {/* Navigation */}
        <nav className="p-4 space-y-2">
          {navItems.map((item) => (
            <button
              key={item.id}
              onClick={() => setCurrentView(item.id)}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 group ${
                currentView === item.id
                  ? 'bg-[#00ff41]/10 border border-[#00ff41]/30 text-[#00ff41]'
                  : 'hover:bg-white/5 text-gray-400 hover:text-white'
              }`}
            >
              <item.icon className={`w-5 h-5 flex-shrink-0 ${
                currentView === item.id ? 'text-[#00ff41]' : 'group-hover:text-[#00ff41]'
              }`} />
              {sidebarOpen && (
                <span className="flex-1 text-left text-sm font-medium animate-fade-in">
                  {item.label}
                </span>
              )}
              {sidebarOpen && item.badge && (
                <Badge 
                  variant="outline" 
                  className={`text-xs ${
                    item.badge === 'LIVE' 
                      ? 'border-[#00ff41]/30 text-[#00ff41]' 
                      : 'border-blue-500/30 text-blue-400'
                  }`}
                >
                  {item.badge}
                </Badge>
              )}
            </button>
          ))}
        </nav>

        {/* BrockBox Integration Card */}
        {sidebarOpen && (
          <div className="p-4 mt-auto">
            <div className="glass-card p-4 gradient-border">
              <div className="flex items-center gap-2 mb-3">
                <div className="w-8 h-8 rounded-lg bg-blue-500/20 flex items-center justify-center">
                  <Link2 className="w-4 h-4 text-blue-400" />
                </div>
                <span className="text-sm font-medium text-white">BrockBox</span>
                <div className="status-dot status-online ml-auto" />
              </div>
              <p className="text-xs text-gray-400 mb-3">
                AI audit bridge active. Physics-anchored proofs verified.
              </p>
              <Button 
                size="sm" 
                variant="outline" 
                className="w-full text-xs border-blue-500/30 text-blue-400 hover:bg-blue-500/10"
                onClick={() => setCurrentView('brockbox')}
              >
                View Bridge
                <ChevronRight className="w-3 h-3 ml-1" />
              </Button>
            </div>
          </div>
        )}

        {/* Toggle Sidebar */}
        <button
          onClick={() => setSidebarOpen(!sidebarOpen)}
          className="absolute -right-3 top-1/2 -translate-y-1/2 w-6 h-12 bg-[#1a1a1a] border border-white/[0.08] rounded-r-lg flex items-center justify-center hover:bg-[#252525] transition-colors"
        >
          {sidebarOpen ? (
            <ChevronRight className="w-4 h-4 text-gray-400 rotate-180" />
          ) : (
            <ChevronRight className="w-4 h-4 text-gray-400" />
          )}
        </button>
      </aside>

      {/* Main Content */}
      <main className={`flex-1 transition-all duration-300 ${sidebarOpen ? 'ml-72' : 'ml-20'}`}>
        {/* Top Header */}
        <header className="sticky top-0 z-40 bg-[#0a0a0a]/80 backdrop-blur-xl border-b border-white/[0.08]">
          <div className="flex items-center justify-between px-8 py-4">
            {/* Breadcrumb */}
            <div className="flex items-center gap-2 text-sm">
              <span className="text-gray-500">Born2Sub.X</span>
              <ChevronRight className="w-4 h-4 text-gray-600" />
              <span className="text-[#00ff41] font-medium">
                {navItems.find(n => n.id === currentView)?.label}
              </span>
            </div>

            {/* System Status Bar */}
            <div className="flex items-center gap-6">
              {/* TRACE Status */}
              <div className="flex items-center gap-2">
                <Radio className="w-4 h-4 text-[#00ff41]" />
                <span className="text-xs text-gray-400">TRACE:</span>
                <Badge variant="outline" className="border-[#00ff41]/30 text-[#00ff41] text-xs">
                  {systemStatus.trace}
                </Badge>
              </div>

              {/* Nodes */}
              <div className="flex items-center gap-2">
                <Server className="w-4 h-4 text-blue-400" />
                <span className="text-xs text-gray-400">Nodes:</span>
                <span className="text-xs text-white font-medium">{systemStatus.nodes}</span>
              </div>

              {/* Chains */}
              <div className="flex items-center gap-2">
                <Link2 className="w-4 h-4 text-purple-400" />
                <span className="text-xs text-gray-400">Chains:</span>
                <span className="text-xs text-white font-medium">{systemStatus.chains}</span>
              </div>

              <Separator orientation="vertical" className="h-6 bg-white/10" />

              {/* BrockBox Status */}
              <div className="flex items-center gap-2">
                <div className="status-dot status-online" />
                <span className="text-xs text-blue-400">BrockBox</span>
              </div>

              {/* Security Badge */}
              <div className="flex items-center gap-2 px-3 py-1.5 bg-[#00ff41]/10 border border-[#00ff41]/20 rounded-lg">
                <Lock className="w-3 h-3 text-[#00ff41]" />
                <span className="text-xs text-[#00ff41] font-medium">Zero-Trust</span>
              </div>
            </div>
          </div>
        </header>

        {/* Page Content */}
        <div className="p-8">
          {renderView()}
        </div>

        {/* Footer */}
        <Footer />
      </main>
    </div>
  );
}

export default App;
