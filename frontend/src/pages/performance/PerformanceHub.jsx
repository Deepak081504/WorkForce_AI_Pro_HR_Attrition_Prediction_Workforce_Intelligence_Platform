import React, { useState, useEffect } from 'react';
import { 
  Award, TrendingUp, AlertCircle, Star, 
  CheckCircle2, PlusCircle, UserCheck, Search 
} from 'lucide-react';
import { employeeService } from '../../api/services';

export default function PerformanceHub() {
  const [employees, setEmployees] = useState([]);
  const [reviews, setReviews] = useState([
    { id: 1, empName: 'Divya Priyan', role: 'Marketing Executive', rating: 2.5, status: 'At Risk', okrScore: '62%', cycle: 'Q3 2026' },
    { id: 2, empName: 'Rahul Kumar', role: 'Finance Analyst', rating: 4.2, status: 'Exceeding', okrScore: '91%', cycle: 'Q3 2026' },
    { id: 3, empName: 'Priya Sharma', role: 'HR Executive', rating: 3.8, status: 'Consistent', okrScore: '84%', cycle: 'Q3 2026' },
    { id: 4, empName: 'Vijay Raj', role: 'Senior Software Developer', rating: 4.6, status: 'Top Performer', okrScore: '96%', cycle: 'Q3 2026' },
    { id: 5, empName: 'Arun Kumar', role: 'Engineering Manager', rating: 4.8, status: 'Top Performer', okrScore: '98%', cycle: 'Q3 2026' },
  ]);
  const [showModal, setShowModal] = useState(false);
  const [newReview, setNewReview] = useState({
    empName: '',
    role: 'Operations',
    rating: '4.0',
    okrScore: '85%',
    cycle: 'Q3 2026',
    status: 'Consistent'
  });

  useEffect(() => {
    const loadEmps = async () => {
      try {
        const res = await employeeService.list();
        if (Array.isArray(res)) setEmployees(res);
      } catch (err) {
        console.error(err);
      }
    };
    loadEmps();
  }, []);

  const handleAddReview = (e) => {
    e.preventDefault();
    const scoreVal = parseFloat(newReview.rating);
    const status = scoreVal < 3.0 ? 'At Risk' : scoreVal >= 4.5 ? 'Top Performer' : 'Consistent';
    
    setReviews(prev => {
      const existingIndex = prev.findIndex(
        r => r.empName.trim().toLowerCase() === newReview.empName.trim().toLowerCase()
      );

      if (existingIndex !== -1) {
        const updated = [...prev];
        updated[existingIndex] = {
          ...updated[existingIndex],
          rating: newReview.rating,
          okrScore: newReview.okrScore,
          cycle: newReview.cycle,
          status
        };
        return updated;
      } else {
        return [{ id: Date.now(), ...newReview, status }, ...prev];
      }
    });

    setNewReview({
      empName: '',
      role: 'Operations',
      rating: '4.0',
      okrScore: '85%',
      cycle: 'Q3 2026',
      status: 'Consistent'
    });
    setShowModal(false);
  };

  const underperformersCount = reviews.filter(r => r.status === 'At Risk').length;
  const avgRating = (reviews.reduce((acc, r) => acc + parseFloat(r.rating || 0), 0) / (reviews.length || 1)).toFixed(1);

  return (
    <div className="space-y-6">
      {/* Banner */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-[#0B0F19] border border-white/10 p-6 rounded-2xl shadow-xl">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Award className="h-4 w-4 text-emerald-400" />
            <span className="text-[10px] uppercase tracking-widest font-mono text-emerald-400 font-bold">Talent Velocity</span>
          </div>
          <h1 className="text-xl font-bold text-white tracking-tight">Performance & Appraisal Hub</h1>
          <p className="text-xs text-slate-400 mt-0.5">Continuous OKR scoring, competency reviews, and attrition correlation analysis</p>
        </div>
        <button
          onClick={() => setShowModal(true)}
          className="px-4 py-2.5 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 text-white text-xs font-semibold flex items-center gap-2 shadow-lg shadow-emerald-600/25 transition cursor-pointer"
        >
          <PlusCircle className="h-4 w-4" /> Conduct Appraisal
        </button>
      </div>

      {/* Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {[
          { label: 'Avg Competency Rating', val: `${avgRating} / 5.0`, icon: Star, color: 'text-amber-400' },
          { label: 'Org OKR Attainment', val: '86.2%', icon: TrendingUp, color: 'text-emerald-400' },
          { label: 'Underperformance Index', val: `${underperformersCount} Staff`, icon: AlertCircle, color: 'text-rose-400' },
          { label: 'Reviews Completed', val: reviews.length, icon: CheckCircle2, color: 'text-indigo-400' },
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

      {/* Table */}
      <div className="bg-[#0B0F19] border border-white/10 rounded-2xl overflow-hidden shadow-xl">
        <div className="p-4 border-b border-white/10 flex justify-between items-center">
          <div>
            <h2 className="text-sm font-semibold text-white">Appraisal Evaluation Roster</h2>
            <p className="text-xs text-slate-400">Quarterly performance grades synced with flight-risk heuristics</p>
          </div>
        </div>

        <table className="w-full text-left text-xs">
          <thead className="bg-[#06080F] border-b border-white/10 text-slate-400 font-medium">
            <tr>
              <th className="p-4">Employee</th>
              <th className="p-4">Designation</th>
              <th className="p-4">Appraisal Cycle</th>
              <th className="p-4">Score Rating</th>
              <th className="p-4">OKR Attainment</th>
              <th className="p-4">Flight Impact</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-white/5">
            {reviews.map((r) => (
              <tr key={r.id} className="hover:bg-white/[0.02] transition">
                <td className="p-4 font-semibold text-white flex items-center gap-2">
                  <div className="h-7 w-7 rounded-lg bg-indigo-500/10 text-indigo-400 flex items-center justify-center font-bold text-[10px]">
                    {r.empName.slice(0, 2).toUpperCase()}
                  </div>
                  {r.empName}
                </td>
                <td className="p-4 text-slate-300">{r.role}</td>
                <td className="p-4 font-mono text-slate-400">{r.cycle}</td>
                <td className="p-4">
                  <span className="font-bold text-amber-400 flex items-center gap-1">
                    <Star className="h-3 w-3 fill-current" /> {r.rating} / 5.0
                  </span>
                </td>
                <td className="p-4 font-mono text-emerald-400 font-semibold">{r.okrScore}</td>
                <td className="p-4">
                  <span className={`px-2 py-0.5 rounded text-[10px] font-bold border ${
                    r.status === 'At Risk' 
                      ? 'bg-rose-500/10 text-rose-400 border-rose-500/30 animate-pulse'
                      : r.status === 'Top Performer'
                      ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
                      : 'bg-indigo-500/10 text-indigo-400 border-indigo-500/30'
                  }`}>
                    {r.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-[#0B0F19] border border-white/10 max-w-md w-full rounded-2xl p-6 shadow-2xl space-y-4">
            <div className="flex justify-between items-center border-b border-white/10 pb-3">
              <h3 className="text-sm font-bold text-white flex items-center gap-2">
                <Award className="h-4 w-4 text-emerald-400" /> Log / Update Performance Review
              </h3>
              <button onClick={() => setShowModal(false)} className="text-slate-400 hover:text-white text-xs cursor-pointer">✕</button>
            </div>

            <form onSubmit={handleAddReview} className="space-y-3.5 text-xs">
              <div>
                <label className="text-slate-300 block mb-1">Employee Name</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Divya Priyan"
                  value={newReview.empName}
                  onChange={(e) => setNewReview({ ...newReview, empName: e.target.value })}
                  className="w-full bg-[#06080F] border border-white/10 rounded-lg p-2.5 text-slate-200 outline-none focus:border-emerald-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-slate-300 block mb-1">Rating (1.0 - 5.0)</label>
                  <input
                    type="number"
                    step="0.1"
                    min="1.0"
                    max="5.0"
                    required
                    value={newReview.rating}
                    onChange={(e) => setNewReview({ ...newReview, rating: e.target.value })}
                    className="w-full bg-[#06080F] border border-white/10 rounded-lg p-2.5 text-slate-200 outline-none focus:border-emerald-500"
                  />
                </div>
                <div>
                  <label className="text-slate-300 block mb-1">OKR Attainment (%)</label>
                  <input
                    type="text"
                    required
                    placeholder="85%"
                    value={newReview.okrScore}
                    onChange={(e) => setNewReview({ ...newReview, okrScore: e.target.value })}
                    className="w-full bg-[#06080F] border border-white/10 rounded-lg p-2.5 text-slate-200 outline-none focus:border-emerald-500"
                  />
                </div>
              </div>

              <button
                type="submit"
                className="w-full py-2.5 rounded-xl font-semibold bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 text-white transition cursor-pointer shadow-lg shadow-emerald-600/25 mt-2"
              >
                Save Appraisal
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}