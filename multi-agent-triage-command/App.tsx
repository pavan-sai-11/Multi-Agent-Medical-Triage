
import React, { useState } from 'react';
import {
  Activity,
  ShieldCheck,
  Cpu,
  AlertCircle,
  Users,
  LineChart,
  BrainCircuit,
  Settings,
  Bell
} from 'lucide-react';
import MedicalBackground from './components/MedicalBackground';

/**
 * 4. Minimal HTML / JSX snippet showing how to mount it
 * EXACTLY where to paste: The MedicalBackground component should be placed at the top-level 
 * of your main App container to ensure it sits behind all other UI content.
 */

const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState('triage');
  const [symptoms, setSymptoms] = useState('');
  const [age, setAge] = useState('');
  const [history, setHistory] = useState('');
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const runTriage = async () => {
    if (!symptoms || !age) return;
    setLoading(true);
    setResult(null);
    try {
      const response = await fetch('http://localhost:8000/api/triage', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ symptoms, age, history })
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error("Triage Error:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative min-h-screen font-sans">
      {/* PASTE THE BACKGROUND HERE - Top level, z-index managed by class */}
      <MedicalBackground />

      {/* Main UI Content */}
      <nav className="border-b border-teal-900/30 bg-[#020617]/80 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-teal-500/10 p-2 rounded-lg border border-teal-500/20">
              <Activity className="w-6 h-6 text-teal-400" />
            </div>
            <div>
              <h1 className="text-xl font-bold tracking-tight text-slate-100">MULTI-AGENT TRIAGE COMMAND</h1>
              <p className="text-[10px] uppercase tracking-widest text-teal-500 font-semibold">Automated Clinical Intelligence Network</p>
            </div>
          </div>

          <div className="flex items-center gap-6">
            <div className="flex gap-1">
              {['triage', 'agents', 'analytics'].map((tab) => (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tab)}
                  className={`px-4 py-1.5 rounded-md text-sm font-medium transition-all ${activeTab === tab
                    ? 'bg-teal-500/10 text-teal-300 border border-teal-500/30'
                    : 'text-slate-400 hover:text-slate-100'
                    }`}
                >
                  {tab.charAt(0).toUpperCase() + tab.slice(1)}
                </button>
              ))}
            </div>
            <div className="h-6 w-[1px] bg-slate-800" />
            <div className="flex items-center gap-4">
              <Bell className="w-5 h-5 text-slate-400 cursor-pointer hover:text-teal-400" />
              <div className="flex items-center gap-2 bg-slate-900/50 border border-slate-800 px-3 py-1.5 rounded-full">
                <div className="w-2 h-2 rounded-full bg-green-500 shadow-[0_0_8px_rgba(34,197,94,0.5)] animate-pulse" />
                <span className="text-xs font-mono text-slate-300">NETWORK ONLINE</span>
              </div>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 py-8 relative">
        <header className="mb-8">
          <div className="flex justify-between items-end">
            <div>
              <h2 className="text-3xl font-bold text-slate-100">Live Operation Dashboard</h2>
              <p className="text-slate-400 mt-1">Real-time patient prioritization and agent allocation across 14 nodes.</p>
            </div>
            <div className="flex gap-3">
              <button className="flex items-center gap-2 px-4 py-2 bg-teal-600 hover:bg-teal-500 text-white rounded-lg transition-colors text-sm font-medium">
                <BrainCircuit className="w-4 h-4" /> Deploy New Agent
              </button>
            </div>
          </div>
        </header>

        {/* Main Split View: Inputs (Left) vs Analysis (Right) */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">

          {/* Left Column: Triage Intake */}
          <div className="bg-[#020b1f]/40 border border-slate-800 rounded-2xl overflow-hidden backdrop-blur-xl p-6 h-fit">
            <div className="flex items-center justify-between mb-6">
              <h3 className="font-bold flex items-center gap-2 text-slate-100">
                <Activity className="w-5 h-5 text-teal-400" /> Triage Intake Protocol
              </h3>
              {result && (
                <span className={`px-3 py-1 rounded-full text-xs font-bold ${result.final_decision?.includes('URGENT') ? 'bg-red-500/20 text-red-500 border border-red-500/50' :
                  result.final_decision?.includes('CONSULT') ? 'bg-amber-500/20 text-amber-500 border border-amber-500/50' :
                    'bg-green-500/20 text-green-500 border border-green-500/50'
                  }`}>
                  {result.final_decision}
                </span>
              )}
            </div>

            <div className="space-y-4 mb-6">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <label className="text-xs uppercase tracking-wider text-slate-500 font-bold">Patient Age</label>
                  <input
                    type="text"
                    value={age}
                    onChange={(e) => setAge(e.target.value)}
                    className="w-full bg-[#0B1221] border border-slate-700 rounded-lg px-4 py-3 text-slate-100 focus:border-teal-500 outline-none transition-colors"
                    placeholder="e.g. 45"
                  />
                </div>
                <div className="space-y-2">
                  <label className="text-xs uppercase tracking-wider text-slate-500 font-bold">Medical History</label>
                  <input
                    type="text"
                    value={history}
                    onChange={(e) => setHistory(e.target.value)}
                    className="w-full bg-[#0B1221] border border-slate-700 rounded-lg px-4 py-3 text-slate-100 focus:border-teal-500 outline-none transition-colors"
                    placeholder="e.g. Hypertension, Diabetes"
                  />
                </div>
              </div>
              <div className="space-y-2">
                <label className="text-xs uppercase tracking-wider text-slate-500 font-bold">Presenting Symptoms</label>
                <textarea
                  value={symptoms}
                  onChange={(e) => setSymptoms(e.target.value)}
                  className="w-full bg-[#0B1221] border border-slate-700 rounded-lg px-4 py-3 text-slate-100 focus:border-teal-500 outline-none transition-colors h-40 resize-none"
                  placeholder="Describe symptoms in detail... (e.g. Severe chest pain radiating to left arm)"
                />
              </div>
            </div>

            <div className="flex justify-end">
              <button
                onClick={runTriage}
                disabled={loading}
                className={`flex items-center gap-2 px-6 py-3 rounded-lg font-bold transition-all shadow-lg w-full justify-center ${loading
                  ? 'bg-slate-700 text-slate-400 cursor-not-allowed'
                  : 'bg-teal-600 hover:bg-teal-500 text-white shadow-teal-500/20'
                  }`}
              >
                {loading ? (
                  <><div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" /> PROCESSING ENTROPY...</>
                ) : (
                  <><BrainCircuit className="w-5 h-5" /> EXECUTE TRIAGE PROTOCOL</>
                )}
              </button>
            </div>
          </div>

          {/* Right Column: Results & Analysis */}
          <div className="space-y-6">
            {result ? (
              <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
                <div className="bg-[#020b1f]/60 border border-teal-900/40 p-5 rounded-2xl backdrop-blur-sm h-full">
                  <h4 className="text-xs font-bold text-teal-400 uppercase tracking-widest mb-3 flex items-center gap-2">
                    <LineChart className="w-4 h-4" /> Reasoning Analysis
                  </h4>
                  <p className="text-sm text-slate-300 leading-relaxed whitespace-pre-line">
                    {result.reasoning_summary}
                  </p>
                </div>

                <div className="bg-[#020b1f]/60 border border-amber-900/40 p-5 rounded-2xl backdrop-blur-sm">
                  <h4 className="text-xs font-bold text-amber-400 uppercase tracking-widest mb-3 flex items-center gap-2">
                    <AlertCircle className="w-4 h-4" /> Safety Protocols
                  </h4>
                  <ul className="space-y-3 mt-4">
                    {result.safety_notes?.map((note: string, i: number) => (
                      <li key={i} className="text-sm text-slate-300 flex items-start gap-3 bg-amber-500/5 p-3 rounded-lg border border-amber-500/10">
                        <span className="text-amber-500 mt-0.5">⚠️</span>
                        <span>{note}</span>
                      </li>
                    ))}
                    {result.next_steps?.map((step: string, i: number) => (
                      <li key={`step-${i}`} className="text-sm text-slate-300 flex items-start gap-3 bg-teal-500/5 p-3 rounded-lg border border-teal-500/10">
                        <span className="text-teal-500 mt-0.5">👉</span>
                        <span>{step}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Doctor Recommendations */}
                {result.recommended_doctors && result.recommended_doctors.length > 0 && (
                  <div className="bg-[#020b1f]/60 border border-teal-900/40 p-5 rounded-2xl backdrop-blur-sm col-span-1 md:col-span-2 mt-2">
                    <h4 className="text-xs font-bold text-teal-400 uppercase tracking-widest mb-4 flex items-center gap-2">
                      <Users className="w-4 h-4" /> Recommended Specialists
                    </h4>
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                      {result.recommended_doctors.map((doc: any) => (
                        <div key={doc.id} className="bg-slate-900/50 border border-slate-800 rounded-lg p-4 hover:border-teal-500/30 transition-colors">
                          <div className="flex justify-between items-start">
                            <div>
                              <h5 className="font-bold text-slate-200">{doc.name}</h5>
                              <p className="text-xs text-teal-500 font-medium mb-1">{doc.specialty}</p>
                              <p className="text-xs text-slate-400">{doc.hospital}</p>
                            </div>
                            <div className={`w-2 h-2 rounded-full ${doc.availability === 'On Call' ? 'bg-amber-500 animate-pulse' :
                                doc.availability === 'Available' ? 'bg-green-500' : 'bg-slate-600'
                              }`} title={doc.availability} />
                          </div>
                          <div className="mt-3 pt-3 border-t border-slate-800/50 space-y-1">
                            <p className="text-xs text-slate-400 flex items-center gap-2">
                              <span className="text-slate-600">📞</span> {doc.contact}
                            </p>
                            <p className="text-xs text-slate-400 flex items-center gap-2">
                              <span className="text-slate-600">✉️</span> {doc.email}
                            </p>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ) : (
              // Empty State Placeholder
              <div className="h-full bg-[#020b1f]/20 border border-slate-800/50 rounded-2xl border-dashed flex flex-col items-center justify-center p-12 text-center">
                <div className="w-16 h-16 bg-slate-800/50 rounded-full flex items-center justify-center mb-4">
                  <Activity className="w-8 h-8 text-slate-600" />
                </div>
                <h3 className="text-slate-400 font-semibold">Triage System Standby</h3>
                <p className="text-slate-600 text-sm mt-2 max-w-sm">
                  Enter patient vitals and symptoms to initiate the multi-agent deliberation network.
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Bottom Section: Active Agents */}
        <div className="space-y-4">
          <h3 className="text-xs font-bold text-teal-500 uppercase tracking-widest flex items-center gap-2">
            <Users className="w-4 h-4" /> Active Neural Agents
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              { name: 'DIAGNO-7', role: 'Respiratory Triage', load: 84, status: 'Processing' },
              { name: 'NEURO-X', role: 'Trauma Assessment', load: 32, status: 'Idle' },
              { name: 'CARDI-2', role: 'Vitals Monitoring', load: 92, status: 'Alerting' },
              { name: 'PHARMA-V', role: 'Dosage Calculation', load: 12, status: 'Optimal' },
            ].map((agent) => (
              <div key={agent.name} className="bg-[#020b1f]/60 border border-teal-900/20 p-4 rounded-xl backdrop-blur-sm group hover:border-teal-500/40 transition-all">
                <div className="flex justify-between items-start mb-3">
                  <div>
                    <h4 className="font-bold text-slate-200">{agent.name}</h4>
                    <p className="text-xs text-slate-500">{agent.role}</p>
                  </div>
                  <span className={`text-[10px] px-2 py-0.5 rounded-full border ${agent.status === 'Alerting' ? 'border-red-500/50 text-red-400 bg-red-500/10' :
                    agent.status === 'Processing' ? 'border-teal-500/50 text-teal-400 bg-teal-500/10' :
                      'border-slate-500/50 text-slate-400 bg-slate-500/10'
                    }`}>
                    {agent.status}
                  </span>
                </div>
                <div className="space-y-1">
                  <div className="flex justify-between text-[10px] font-mono text-slate-400">
                    <span>COMPUTE LOAD</span>
                    <span>{agent.load}%</span>
                  </div>
                  <div className="h-1 bg-slate-800 rounded-full overflow-hidden">
                    <div
                      className={`h-full transition-all duration-1000 ${agent.load > 80 ? 'bg-amber-500' : 'bg-teal-500'
                        }`}
                      style={{ width: `${agent.load}%` }}
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

      </main>

      <footer className="fixed bottom-0 left-0 right-0 bg-[#020617]/90 border-t border-teal-900/30 py-3 px-6 z-40">
        <div className="max-w-7xl mx-auto flex justify-between items-center text-[10px] text-slate-500 font-mono tracking-wider">
          <div className="flex gap-4">
            <span>UPTIME: 124:12:09</span>
            <span>NODES: 14/14 ACTIVE</span>
            <span>LATENCY: 12ms</span>
          </div>
          <div className="flex items-center gap-2">
            <Settings className="w-3 h-3 hover:text-teal-400 cursor-pointer" />
            <span>VERSION 4.2.1-CLINICAL</span>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default App;
