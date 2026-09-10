import React, { useState } from 'react';
import { 
  Briefcase, Users, UserCheck, Clock, 
  PlusCircle, Filter, Search, ArrowRight, ShieldAlert, CheckCircle2 
} from 'lucide-react';

const STAGES = ['Applied', 'Screening', 'Technical Interview', 'HR Offer'];

export default function RecruitmentPipeline() {
  const [candidates, setCandidates] = useState([
    { id: 1, name: 'Sanjay Krishnan', role: 'Full Stack Developer', stage: 'Applied', exp: '3 yrs', flightRisk: 'Low Risk (12%)', score: '88%' },
    { id: 2, name: 'Meera Nambiar', role: 'Data Scientist', stage: 'Screening', exp: '4.5 yrs', flightRisk: 'Moderate Risk (28%)', score: '92%' },
    { id: 3, name: 'Karthik Raja', role: 'DevOps Engineer', stage: 'Technical Interview', exp: '5 yrs', flightRisk: 'Low Risk (9%)', score: '95%' },
    { id: 4, name: 'Ananya Deshmukh', role: 'UI/UX Designer', stage: 'HR Offer', exp: '2.5 yrs', flightRisk: 'High Risk (41%)', score: '81%' },
    { id: 5, name: 'Gokulnath P', role: 'Backend Engineer', stage: 'Technical Interview', exp: '3 yrs', flightRisk: 'Low Risk (15%)', score: '89%' },
  ]);

  const [showModal, setShowModal] = useState(false);
  const [filterRole, setFilterRole] = useState('All');
  const [newCandidate, setNewCandidate] = useState({
    name: '',
    role: 'Backend Engineer',
    exp: '2 yrs',
    stage: 'Applied',
    score: '85%',
  });

  const handleAddCandidate = (e) => {
    e.preventDefault();
    const risk = parseFloat(newCandidate.score) > 85 ? 'Low Risk (14%)' : 'Moderate Risk (32%)';
    setCandidates(prev => [
      { id: Date.now(), ...newCandidate, flightRisk: risk },
      ...prev
    ]);
    setNewCandidate({ name: '', role: 'Backend Engineer', exp: '2 yrs', stage: 'Applied', score: '85%' });
    setShowModal(false);
  };

  const moveStage = (id, currentStage) => {
    const currentIndex = STAGES.indexOf(currentStage);
    if (currentIndex < STAGES.length - 1) {
      const nextStage = STAGES[currentIndex + 1];
      setCandidates(prev => prev.map(c => c.id === id ? { ...c, stage: nextStage } : c));
    }
  };

  const filteredCandidates = filterRole === 'All' 
    ? candidates 
    : candidates.filter(c => c.role === filterRole);

  return (
    <div className="space-y-6">
      {/* Banner */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-[#0B0F19] border border-white/10 p-6 rounded-2xl shadow-xl">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Briefcase className="h-4 w-4 text-cyan-400" />
            <span className="text-[10px] uppercase tracking-widest font-mono text-cyan-400 font-bold">Talent Acquisition</span>
          </div>
          <h1 className="text-xl font-bold text-white tracking-tight">Recruitment & ATS Intelligence</h1>
          <p className="text-xs text-slate-400 mt-0.5">Pipeline screening, ATS tracking, and pre-hire attrition risk inference</p>
        </div>

        <button
          onClick={() => setShowModal(true)}
          className="px-4 py-2.5 rounded-xl bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 text-white text-xs font-semibold flex items-center gap-2 shadow-lg shadow-cyan-600/25 transition cursor-pointer"
        >
          <PlusCircle className="h-4 w-4" /> Add Candidate
        </button>
      </div>

      {/* Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {[
          { label: 'Active Pipeline Candidates', val: candidates.length, icon: Users, color: 'text-cyan-400' },
          { label: 'Technical Screening', val: candidates.filter(c => c.stage === 'Technical Interview').length, icon: Clock, color: 'text-amber-400' },
          { label: 'Offers Dispatched', val: candidates.filter(c => c.stage === 'HR Offer').length, icon: UserCheck, color: 'text-emerald-400' },
          { label: 'Pre-Hire Risk Alerts', val: candidates.filter(c => c.flightRisk.includes('High')).length, icon: ShieldAlert, color: 'text-rose-400' },
        ].map((m, idx) => (
          <div key={idx} className="bg-[#0B0F19] border border-white/10 p-5 rounded-2xl">
            <div className="flex justify-between items-start">
              <span className="text-xs font-medium text-slate-400">{m.label}</span>
              <m.icon className={`h-4 w-4 ${m.color}`} />
            </div>
            <div className="text-xl font-bold text-white mt-2 tracking-tight">{m.val}</div>
          </div>
        ))}
      </div>

      {/* Kanban Board by Hiring Stage */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {STAGES.map((stage) => {
          const stageList = filteredCandidates.filter(c => c.stage === stage);
          return (
            <div key={stage} className="bg-[#0B0F19] border border-white/10 rounded-2xl p-4 flex flex-col min-h-[420px]">
              <div className="flex justify-between items-center mb-3 pb-2 border-b border-white/5">
                <span className="text-xs font-bold text-slate-200 uppercase tracking-wider">{stage}</span>
                <span className="text-[11px] font-mono px-2 py-0.5 rounded-full bg-white/5 text-slate-400">
                  {stageList.length}
                </span>
              </div>

              <div className="space-y-3 flex-1 overflow-y-auto">
                {stageList.map(cand => (
                  <div key={cand.id} className="p-3.5 bg-[#06080F] border border-white/5 hover:border-cyan-500/30 rounded-xl transition space-y-2.5">
                    <div className="flex justify-between items-start">
                      <div>
                        <h2 className="text-xs font-bold text-white">{cand.name}</h2>
                        <span className="text-[11px] text-slate-400">{cand.role}</span>
                      </div>
                      <span className="text-[10px] font-mono text-cyan-400 bg-cyan-500/10 px-1.5 py-0.5 rounded">
                        {cand.exp}
                      </span>
                    </div>

                    <div className="flex justify-between items-center pt-1 border-t border-white/5 text-[10px]">
                      <span className="text-slate-400">Match: <b className="text-emerald-400">{cand.score}</b></span>
                      <span className={`px-1.5 py-0.5 rounded font-semibold ${
                        cand.flightRisk.includes('High') 
                          ? 'bg-rose-500/10 text-rose-400' 
                          : 'bg-emerald-500/10 text-emerald-400'
                      }`}>
                        {cand.flightRisk}
                      </span>
                    </div>

                    {stage !== 'HR Offer' && (
                      <button
                        onClick={() => moveStage(cand.id, cand.stage)}
                        className="w-full mt-2 py-1 bg-white/5 hover:bg-cyan-500/20 text-cyan-300 hover:text-white rounded text-[11px] font-medium flex items-center justify-center gap-1 transition cursor-pointer"
                      >
                        Advance Stage <ArrowRight className="h-3 w-3" />
                      </button>
                    )}
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>

      {/* Modal for Adding Candidate */}
      {showModal && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-[#0B0F19] border border-white/10 max-w-md w-full rounded-2xl p-6 shadow-2xl space-y-4">
            <div className="flex justify-between items-center border-b border-white/10 pb-3">
              <h2 className="text-sm font-bold text-white flex items-center gap-2">
                <Briefcase className="h-4 w-4 text-cyan-400" /> New Candidate Application
              </h2>
              <button onClick={() => setShowModal(false)} className="text-slate-400 hover:text-white text-xs cursor-pointer">✕</button>
            </div>

            <form onSubmit={handleAddCandidate} className="space-y-3 text-xs">
              <div>
                <label className="text-slate-300 block mb-1">Candidate Full Name</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Ramesh Varma"
                  value={newCandidate.name}
                  onChange={(e) => setNewCandidate({ ...newCandidate, name: e.target.value })}
                  className="w-full bg-[#06080F] border border-white/10 rounded-lg p-2.5 text-slate-200 outline-none focus:border-cyan-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-slate-300 block mb-1">Role</label>
                  <select
                    value={newCandidate.role}
                    onChange={(e) => setNewCandidate({ ...newCandidate, role: e.target.value })}
                    className="w-full bg-[#06080F] border border-white/10 rounded-lg p-2.5 text-slate-200 outline-none"
                  >
                    <option value="Backend Engineer">Backend Engineer</option>
                    <option value="Full Stack Developer">Full Stack Developer</option>
                    <option value="Data Scientist">Data Scientist</option>
                    <option value="DevOps Engineer">DevOps Engineer</option>
                    <option value="UI/UX Designer">UI/UX Designer</option>
                  </select>
                </div>
                <div>
                  <label className="text-slate-300 block mb-1">Experience</label>
                  <input
                    type="text"
                    required
                    placeholder="e.g. 3.5 yrs"
                    value={newCandidate.exp}
                    onChange={(e) => setNewCandidate({ ...newCandidate, exp: e.target.value })}
                    className="w-full bg-[#06080F] border border-white/10 rounded-lg p-2.5 text-slate-200 outline-none focus:border-cyan-500"
                  />
                </div>
              </div>

              <div>
                <label className="text-slate-300 block mb-1">Resume Screening Score (%)</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. 90%"
                  value={newCandidate.score}
                  onChange={(e) => setNewCandidate({ ...newCandidate, score: e.target.value })}
                  className="w-full bg-[#06080F] border border-white/10 rounded-lg p-2.5 text-slate-200 outline-none focus:border-cyan-500"
                />
              </div>

              <button
                type="submit"
                className="w-full py-2.5 rounded-xl font-semibold bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 text-white transition cursor-pointer shadow-lg shadow-cyan-600/25 mt-2"
              >
                Register into Pipeline
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}