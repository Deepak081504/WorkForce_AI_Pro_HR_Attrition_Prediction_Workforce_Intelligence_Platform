import React, { useState, useEffect } from 'react';
import { 
  AlertOctagon, CheckCircle2, Clock, 
  ArrowRight, PlusCircle, ShieldAlert, Sparkles 
} from 'lucide-react';
import { predictionService } from '../../api/services';

export default function RetentionInterventions() {
  // Clean initial state: Each employee gets only one distinct active strategy
  const [interventions, setInterventions] = useState([
    { 
      id: 1, 
      action_id: 'INTV-1', 
      employee_id: 9, 
      intervention_type: 'RETENTION', 
      proposed_strategy: 'Compensation benchmark review + Managerial 1-on-1 alignment', 
      status: 'IN_PROGRESS' 
    },
    { 
      id: 2, 
      action_id: 'INTV-2', 
      employee_id: 6, 
      intervention_type: 'MONITORING', 
      proposed_strategy: 'Bi-weekly workload monitoring and burnout check', 
      status: 'PENDING' 
    },
    { 
      id: 3, 
      action_id: 'INTV-3', 
      employee_id: 7, 
      intervention_type: 'ROLE ALIGNMENT', 
      proposed_strategy: 'Internal role rotation feasibility assessment & positive check-in', 
      status: 'RESOLVED' 
    },
  ]);

  const [highRiskStaff, setHighRiskStaff] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadAlerts();
  }, []);

  const loadAlerts = async () => {
    try {
      setLoading(true);
      const res = await predictionService.getHighRisk();
      if (res && Array.isArray(res)) {
        setHighRiskStaff(res);
      }
    } catch (err) {
      console.error('Failed to load high risk staff', err);
    } finally {
      setLoading(false);
    }
  };

  // Cycle status between PENDING -> IN_PROGRESS -> RESOLVED
  const cycleStatus = (id) => {
    setInterventions(prev => prev.map(item => {
      if (item.id === id) {
        let nextStatus = 'PENDING';
        if (item.status === 'PENDING') nextStatus = 'IN_PROGRESS';
        else if (item.status === 'IN_PROGRESS') nextStatus = 'RESOLVED';
        else nextStatus = 'PENDING';
        return { ...item, status: nextStatus };
      }
      return item;
    }));
  };

  // Intelligent handler: Prevents duplicate rows for the same employee
  const handleTriggerRetention = (targetEmpId = 9, customStrategy = null) => {
    setInterventions(prev => {
      const existingIndex = prev.findIndex(item => item.employee_id === targetEmpId);
      
      if (existingIndex !== -1) {
        // If employee already exists, update their record directly instead of creating duplicate
        const updated = [...prev];
        updated[existingIndex] = {
          ...updated[existingIndex],
          status: 'IN_PROGRESS',
          proposed_strategy: customStrategy || 'Immediate retention package escalation + Executive 1-on-1 scheduled'
        };
        return updated;
      }

      // Add a fresh unique intervention if not present
      const nextId = prev.length + 1;
      return [
        {
          id: Date.now(),
          action_id: `INTV-${nextId}`,
          employee_id: targetEmpId,
          intervention_type: 'RETENTION',
          proposed_strategy: customStrategy || 'Immediate retention package & salary review',
          status: 'IN_PROGRESS'
        },
        ...prev
      ];
    });
  };

  return (
    <div className="space-y-6">
      {/* Banner */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-[#0B0F19] border border-white/10 p-6 rounded-2xl shadow-xl">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <AlertOctagon className="h-4 w-4 text-rose-400" />
            <span className="text-[10px] uppercase tracking-widest font-mono text-rose-400 font-bold">Retention Ops</span>
          </div>
          <h1 className="text-xl font-bold text-white tracking-tight">Retention Interventions & Alerts</h1>
          <p className="text-xs text-slate-400 mt-0.5">Automated mitigation triggers and 1-on-1 actions for critical flight risks</p>
        </div>

        <button 
          onClick={() => handleTriggerRetention(9, 'Executive 1-on-1 scheduled; Career progression review')}
          className="px-4 py-2.5 rounded-xl bg-gradient-to-r from-rose-600 to-pink-600 hover:from-rose-500 text-white text-xs font-semibold flex items-center gap-2 shadow-lg shadow-rose-600/25 transition cursor-pointer"
        >
          <PlusCircle className="h-4 w-4" /> Trigger Retention Action
        </button>
      </div>

      {/* Active Flight Alerts */}
      <div>
        <h2 className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-3 flex items-center gap-2">
          <Sparkles className="h-3.5 w-3.5 text-amber-400" /> Active Flight Risk Alerts
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {(highRiskStaff.length > 0 ? highRiskStaff : [{ id: 9, employee_id: 9, attrition_probability: 0.99 }]).map((risk) => (
            <div key={risk.id} className="bg-[#0B0F19] border border-white/10 rounded-2xl p-5 relative overflow-hidden">
              <div className="flex justify-between items-start mb-3">
                <div>
                  <h3 className="text-sm font-bold text-white">Employee #{risk.employee_id}</h3>
                  <p className="text-[11px] text-slate-500 font-mono">Telemetry Alert ID #{risk.id}</p>
                </div>
                <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-rose-500/10 text-rose-400 border border-rose-500/20">
                  {((risk.attrition_probability || 0.99) * 100).toFixed(1)}% RISK
                </span>
              </div>
              
              <div className="flex justify-between items-center pt-2 border-t border-white/5 text-xs">
                <span className="text-slate-400 text-[11px]">Intervention: <b className="text-amber-400">Required</b></span>
                <button 
                  onClick={() => handleTriggerRetention(risk.employee_id, 'Immediate retention package & salary review')}
                  className="text-indigo-400 hover:text-indigo-300 font-medium flex items-center gap-1 cursor-pointer text-[11px]"
                >
                  Mitigate <ArrowRight className="h-3 w-3" />
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Strategies Table */}
      <div className="bg-[#0B0F19] border border-white/10 rounded-2xl p-6">
        <div className="mb-4">
          <h2 className="text-sm font-semibold text-white">Active Retention Strategies</h2>
          <p className="text-xs text-slate-400">Audit trace of proposed compensations, reassignments, and leadership 1-on-1s</p>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-white/[0.02] uppercase tracking-wider text-[10px] text-slate-500 border-b border-white/5 font-mono">
              <tr>
                <th className="py-3 px-4">Action ID</th>
                <th className="py-3 px-4">Target Employee</th>
                <th className="py-3 px-4">Intervention Type</th>
                <th className="py-3 px-4">Proposed Strategy</th>
                <th className="py-3 px-4 text-right">Status (Click to Change)</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5">
              {interventions.map((row) => (
                <tr key={row.id} className="hover:bg-white/[0.02] transition">
                  <td className="py-3.5 px-4 font-mono text-slate-400 font-semibold">#{row.action_id}</td>
                  <td className="py-3.5 px-4 font-bold text-white">Employee #{row.employee_id}</td>
                  <td className="py-3.5 px-4">
                    <span className="px-2 py-0.5 rounded text-[10px] font-mono font-medium bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                      {row.intervention_type}
                    </span>
                  </td>
                  <td className="py-3.5 px-4 text-slate-300 max-w-md">
                    {row.proposed_strategy}
                  </td>
                  <td className="py-3.5 px-4 text-right">
                    <button
                      onClick={() => cycleStatus(row.id)}
                      className={`px-2.5 py-1 rounded text-[10px] font-bold tracking-wider cursor-pointer border transition ${
                        row.status === 'RESOLVED'
                          ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30 hover:bg-emerald-500/20'
                          : row.status === 'IN_PROGRESS'
                          ? 'bg-cyan-500/10 text-cyan-400 border-cyan-500/30 hover:bg-cyan-500/20'
                          : 'bg-amber-500/10 text-amber-400 border-amber-500/30 hover:bg-amber-500/20'
                      }`}
                    >
                      {row.status}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}