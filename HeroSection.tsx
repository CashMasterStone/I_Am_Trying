import { useEffect, useState } from 'react';
import { 
  Shield, 
  Cpu, 
  Link2, 
  Activity, 
  Globe, 
  Zap,
  Fingerprint,
  ArrowRight,
  Radio,
  Lock,
  Server,
  CheckCircle2
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';

// ═══════════════════════════════════════════════════════════════════════════
// HERO SECTION - Born2Sub.X Ecosystem Landing
// ═══════════════════════════════════════════════════════════════════════════

const HeroSection = () => {
  const [animated, setAnimated] = useState(false);

  useEffect(() => {
    setAnimated(true);
  }, []);

  const ecosystemStats = [
    { label: 'Active Nodes', value: '7', icon: Server, color: 'text-[#00ff41]' },
    { label: 'Chains Anchored', value: '6', icon: Link2, color: 'text-purple-400' },
    { label: 'Proofs Verified', value: '459', icon: CheckCircle2, color: 'text-blue-400' },
    { label: 'Uptime', value: '99.9%', icon: Activity, color: 'text-green-400' },
  ];

  const features = [
    {
      icon: Shield,
      title: 'Sovereign Infrastructure',
      description: 'Self-hosted nodes with deterministic machine code. DSMCALLE enforced.',
      color: 'from-[#00ff41]/20 to-[#00cc33]/10'
    },
    {
      icon: Link2,
      title: 'Multi-Chain Anchoring',
      description: 'Simultaneous binding across Solana, Ethereum, Polygon, Base, Bitcoin, Sonic.',
      color: 'from-purple-500/20 to-purple-600/10'
    },
    {
      icon: Cpu,
      title: 'IPFS Persistence',
      description: 'Content-addressed storage with permanent identifiers and replication.',
      color: 'from-blue-500/20 to-blue-600/10'
    },
    {
      icon: Lock,
      title: 'BrockBox Audit',
      description: 'Physics-anchored AI audit trails with on-chain verification.',
      color: 'from-amber-500/20 to-amber-600/10'
    }
  ];

  return (
    <div className="space-y-16">
      {/* Main Hero */}
      <section className="relative overflow-hidden rounded-3xl">
        {/* Background Gradient */}
        <div className="absolute inset-0 bg-gradient-to-br from-[#0a0a0a] via-[#0f1f0f] to-[#0a0a1f]" />
        
        {/* Animated Grid Background */}
        <div className="absolute inset-0 opacity-20">
          <div 
            className="w-full h-full"
            style={{
              backgroundImage: `
                linear-gradient(rgba(0, 255, 65, 0.1) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 255, 65, 0.1) 1px, transparent 1px)
              `,
              backgroundSize: '50px 50px'
            }}
          />
        </div>

        {/* Glow Effects */}
        <div className="absolute top-0 right-0 w-96 h-96 bg-[#00ff41]/10 rounded-full blur-[120px]" />
        <div className="absolute bottom-0 left-0 w-96 h-96 bg-blue-500/10 rounded-full blur-[120px]" />

        <div className="relative z-10 px-12 py-20">
          {/* Badges */}
          <div className={`flex items-center gap-4 mb-8 transition-all duration-700 ${animated ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}`}>
            <Badge className="bg-[#00ff41]/10 border-[#00ff41]/30 text-[#00ff41] px-4 py-1.5">
              <Radio className="w-3 h-3 mr-2" />
              RTPL-BORN2BUILD™
            </Badge>
            <Badge className="bg-blue-500/10 border-blue-500/30 text-blue-400 px-4 py-1.5">
              <Link2 className="w-3 h-3 mr-2" />
              BrockBox Integrated
            </Badge>
            <Badge className="bg-purple-500/10 border-purple-500/30 text-purple-400 px-4 py-1.5">
              <Lock className="w-3 h-3 mr-2" />
              Zero-Trust Active
            </Badge>
          </div>

          {/* Main Title */}
          <div className={`transition-all duration-700 delay-100 ${animated ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}`}>
            <h1 className="text-6xl md:text-7xl font-bold text-white mb-6 leading-tight">
              Born2Sub.X
              <span className="block text-transparent bg-clip-text bg-gradient-to-r from-[#00ff41] to-[#00cc33]">
                Sovereign Ecosystem
              </span>
            </h1>
            <p className="text-xl text-gray-400 max-w-2xl mb-8">
              A deterministic infrastructure for sovereign computation, multi-chain anchoring, 
              and physics-verified AI audit trails. Integrated with{' '}
              <span className="text-blue-400 font-medium">BrockBox.com</span>.
            </p>
          </div>

          {/* CTA Buttons */}
          <div className={`flex items-center gap-4 transition-all duration-700 delay-200 ${animated ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}`}>
            <Button 
              size="lg" 
              className="bg-[#00ff41] hover:bg-[#00cc33] text-black font-semibold px-8 py-6 text-lg glow-green"
            >
              <Zap className="w-5 h-5 mr-2" />
              Deploy Node
              <ArrowRight className="w-5 h-5 ml-2" />
            </Button>
            <Button 
              size="lg" 
              variant="outline" 
              className="border-white/20 text-white hover:bg-white/5 px-8 py-6 text-lg"
            >
              <Activity className="w-5 h-5 mr-2" />
              View TRACE
            </Button>
            <Button 
              size="lg" 
              variant="outline" 
              className="border-blue-500/30 text-blue-400 hover:bg-blue-500/10 px-8 py-6 text-lg"
            >
              <Link2 className="w-5 h-5 mr-2" />
              BrockBox Bridge
            </Button>
          </div>

          {/* TRACE Chain Visualization */}
          <div className={`mt-16 transition-all duration-700 delay-300 ${animated ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}`}>
            <div className="glass-card p-8">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-lg font-semibold text-white flex items-center gap-2">
                  <Activity className="w-5 h-5 text-[#00ff41]" />
                  TRACE State Machine
                </h3>
                <Badge className="bg-[#00ff41]/10 border-[#00ff41]/30 text-[#00ff41]">
                  0x9 COMPLETE
                </Badge>
              </div>
              
              <div className="flex items-center justify-between">
                {[
                  { state: '0x0', label: 'SOURCE', active: true },
                  { state: '0x3', label: 'PROCESS', active: true },
                  { state: '0x6', label: 'ALIGN', active: true },
                  { state: '0x9', label: 'COMPLETE', active: true },
                ].map((step, idx, arr) => (
                  <div key={step.state} className="flex items-center flex-1">
                    <div className="flex flex-col items-center">
                      <div className={`w-16 h-16 rounded-full flex items-center justify-center text-lg font-bold transition-all duration-500 ${
                        step.active 
                          ? 'bg-[#00ff41] text-black glow-green' 
                          : 'bg-white/5 text-gray-500'
                      }`}>
                        {step.state}
                      </div>
                      <span className={`mt-2 text-sm font-medium ${step.active ? 'text-[#00ff41]' : 'text-gray-500'}`}>
                        {step.label}
                      </span>
                    </div>
                    {idx < arr.length - 1 && (
                      <div className="flex-1 h-0.5 bg-gradient-to-r from-[#00ff41] to-[#00cc33] mx-4" />
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Bar */}
      <section className={`transition-all duration-700 delay-400 ${animated ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}`}>
        <div className="grid grid-cols-4 gap-6">
          {ecosystemStats.map((stat, idx) => (
            <div key={idx} className="glass-card p-6 text-center hover:bg-white/[0.05] transition-colors">
              <stat.icon className={`w-8 h-8 ${stat.color} mx-auto mb-3`} />
              <div className="text-3xl font-bold text-white mb-1">{stat.value}</div>
              <div className="text-sm text-gray-400">{stat.label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* Features Grid */}
      <section className={`transition-all duration-700 delay-500 ${animated ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}`}>
        <div className="text-center mb-10">
          <h2 className="text-3xl font-bold text-white mb-4">Ecosystem Components</h2>
          <p className="text-gray-400 max-w-2xl mx-auto">
            Integrated sovereign infrastructure with deterministic computation, 
            multi-chain anchoring, and physics-verified audit trails.
          </p>
        </div>
        
        <div className="grid grid-cols-2 gap-6">
          {features.map((feature, idx) => (
            <div 
              key={idx} 
              className={`glass-card p-8 hover:bg-white/[0.05] transition-all duration-300 group cursor-pointer gradient-border`}
            >
              <div className={`w-14 h-14 rounded-xl bg-gradient-to-br ${feature.color} flex items-center justify-center mb-6 group-hover:scale-110 transition-transform`}>
                <feature.icon className="w-7 h-7 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-3">{feature.title}</h3>
              <p className="text-gray-400 leading-relaxed">{feature.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Integration Banner */}
      <section className={`transition-all duration-700 delay-600 ${animated ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}`}>
        <div className="glass-card p-8 gradient-border relative overflow-hidden">
          <div className="absolute top-0 right-0 w-64 h-64 bg-blue-500/10 rounded-full blur-[80px]" />
          
          <div className="relative z-10 flex items-center justify-between">
            <div className="flex items-center gap-6">
              <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-[#00ff41] to-[#00cc33] flex items-center justify-center">
                <Fingerprint className="w-8 h-8 text-black" />
              </div>
              <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center">
                <Link2 className="w-8 h-8 text-white" />
              </div>
              <div>
                <h3 className="text-2xl font-bold text-white mb-2">
                  Born2Sub.X ↔ BrockBox.com
                </h3>
                <p className="text-gray-400">
                  Seamless integration between sovereign infrastructure and AI audit trails. 
                  Every deployment generates physics-anchored proofs.
                </p>
              </div>
            </div>
            <Button 
              size="lg" 
              className="bg-blue-500 hover:bg-blue-600 text-white font-semibold px-6"
            >
              Configure Bridge
              <ArrowRight className="w-5 h-5 ml-2" />
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
};

export default HeroSection;
