import React, { useState } from 'react';
import { 
  SlidersHorizontal, Shield, Key, Bell, 
  Save, RefreshCw, CheckCircle2, Lock, Terminal 
} from 'lucide-react';

export default function SystemSettings() {
  const [highRiskThreshold, setHighRiskThreshold] = useState(65);
  const [moderateRiskThreshold, setModerateRiskThreshold] = useState(35);
  const [emailAlerts, setEmailAlerts] = useState(true);
  const [autoRetrain, setAutoRetrain] = useState(false);
  const [saved, setSaved] = useState(false);

  const [auditLogs] = useState([
    { id: 1, action: 'ML_RETRAIN_TRIGGER', user: 'swe123@gmail.com', time: '10 mins ago', status: 'SUCCESS' },
    { id: 2, action: 'DATASET_CSV_UPLOAD', user: 'swe123@gmail.com', time: '25 mins ago', status: 'SUCCESS' },
    { id: 3, action: 'INTERVENTION_LOGGED', user: 'swe123@gmail.com', time: '1 hour ago', status: 'SUCCESS' },
    { id: 4, action: 'APPRAISAL_OVERWRITE', user: 'swe123@gmail.com', time: '2 hours ago', status: 'SUCCESS' },
    { id: 5, action: 'JWT_TOKEN_REFRESH', user: 'swe123@gmail.com', time: '3 hours ago', status: 'SUCCESS' },
  ]);

  const handleSave = (e) => {
    e.preventDefault();
    setSaved(true);
    setTimeout(() => setSaved(false), 2500);
  };

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-[#0B0F19] border border-white/10 p-6 rounded-2xl shadow-xl">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <SlidersHorizontal className="h-4 w-4 text-violet-400" />
            <span className="text-[10px] uppercase tracking-widest font-mono text-violet-400 font-bold">Governance & Config</span>
          </div>
          <h1 className="text-xl font-bold text-white tracking-tight">System & Security Settings</h1>
          <p className="text-xs text-slate-400 mt-0.5">Model thresholds, automated intervention triggers, and telemetry audit trail</p>
        </div>

        <button
          onClick={handleSave}
          className="px-4 py-2 bg-gradient-to-r from-violet-600 to-indigo-600 hover:from-violet-500 text-white text-xs font-semibold rounded-xl flex items-center gap-2 shadow-lg shadow-violet-600/25 transition cursor-pointer"
        >
          {saved ? <CheckCircle2 className="h-4 w-4 text-emerald-300" /> : <Save className="h-4 w-4" />}
          <span>{saved ? 'Configurations Saved' : 'Save Changes'}</span>
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* ML Calibration */}
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-[#0B0F19] border border-white/10 rounded-2xl p-6 space-y-6">
            <h2 className="text-sm font-semibold text-white flex items-center gap-2">
              <SlidersHorizontal className="h-4 w-4 text-indigo-400" /> Attrition Heuristic Thresholds
            </h2>

            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-xs text-slate-300 mb-1.5">
                  <span>Critical High Risk Cutoff</span>
                  <span className="font-mono text-rose-400 font-bold">&gt; {highRiskThreshold}%</span>
                </div>
                <input 
                  type="range" 
                  min="50" 
                  max="90" 
                  value={highRiskThreshold} 
                  onChange={(e) => setHighRiskThreshold(e.target.value)}
                  className="w-full accent-rose-500 cursor-pointer h-1.5 bg-slate-800 rounded-lg"
                />
                <p className="text-[11px] text-slate-500 mt-1">Employees scoring above this value trigger instant Retention Intervention alerts.</p>
              </div>

              <div>
                <div className="flex justify-between text-xs text-slate-300 mb-1.5">
                  <span>Moderate Flight Risk Cutoff</span>
                  <span className="font-mono text-amber-400 font-bold">&gt; {moderateRiskThreshold}%</span>
                </div>
                <input 
                  type="range" 
                  min="20" 
                  max="49" 
                  value={moderateRiskThreshold} 
                  onChange={(e) => setModerateRiskThreshold(e.target.value)}
                  className="w-full accent-amber-500 cursor-pointer h-1.5 bg-slate-800 rounded-lg"
                />
                <p className="text-[11px] text-slate-500 mt-1">Personnel flagged for managerial 1-on-1 check-ins and pulse monitoring.</p>
              </div>
            </div>
          </div>

          <div className="bg-[#0B0F19] border border-white/10 rounded-2xl p-6 space-y-4">
            <h2 className="text-sm font-semibold text-white flex items-center gap-2">
              <Shield className="h-4 w-4 text-emerald-400" /> Automated Pipeline Triggers
            </h2>

            <div className="divide-y divide-white/5 text-xs">
              <div className="py-3 flex justify-between items-center">
                <div>
                  <span className="text-slate-200 font-medium block">Executive Alert Dispatch</span>
                  <span className="text-slate-500 text-[11px]">Forward high-risk flight notifications automatically to HR Leads</span>
                </div>
                <input 
                  type="checkbox" 
                  checked={emailAlerts} 
                  onChange={() => setEmailAlerts(!emailAlerts)} 
                  className="h-4 w-4 accent-indigo-500 cursor-pointer"
                />
              </div>

              <div className="py-3 flex justify-between items-center">
                <div>
                  <span className="text-slate-200 font-medium block">Autonomous Model Fine-Tuning</span>
                  <span className="text-slate-500 text-[11px]">Trigger background retraining when dataset records expand by &gt;20%</span>
                </div>
                <input 
                  type="checkbox" 
                  checked={autoRetrain} 
                  onChange={() => setAutoRetrain(!autoRetrain)} 
                  className="h-4 w-4 accent-indigo-500 cursor-pointer"
                />
              </div>
            </div>
          </div>
        </div>

        {/* Audit Log Box */}
        <div className="bg-[#0B0F19] border border-white/10 rounded-2xl p-6 flex flex-col justify-between">
          <div>
            <h2 className="text-sm font-semibold text-white mb-1 flex items-center gap-2">
              <Terminal className="h-4 w-4 text-cyan-400" /> Security Audit Stream
            </h2>
            <p className="text-xs text-slate-400 mb-4">Real-time immutable telemetry ledger</p>

            <div className="space-y-3">
              {auditLogs.map((log) => (
                <div key={log.id} className="p-3 bg-[#06080F] border border-white/5 rounded-xl text-xs space-y-1">
                  <div className="flex justify-between items-center">
                    <span className="font-mono text-cyan-300 font-bold text-[10px]">{log.action}</span>
                    <span className="text-emerald-400 font-mono text-[9px] bg-emerald-500/10 px-1.5 py-0.5 rounded">{log.status}</span>
                  </div>
                  <div className="flex justify-between text-slate-400 text-[11px] pt-1">
                    <span>{log.user}</span>
                    <span className="text-slate-500 font-mono">{log.time}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="p-3 rounded-xl bg-indigo-500/10 border border-indigo-500/20 text-[11px] text-indigo-300 mt-6 flex items-center gap-2">
            <Lock className="h-4 w-4 shrink-0 text-indigo-400" />
            <span>AES-256 Encrypted Session Active</span>
          </div>
        </div>
      </div>
    </div>
  );
}