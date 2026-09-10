import React, { useState, useEffect } from 'react';
import { predictionService, employeeService } from '../../api/services';
import { 
  ShieldAlert, Sparkles, TrendingUp, Users, 
  BarChart2, PlusCircle, AlertTriangle, CheckCircle2 
} from 'lucide-react';
import { 
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid 
} from 'recharts';

export default function AttritionCockpit() {
  const [analytics, setAnalytics] = useState(null);
  const [highRisk, setHighRisk] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);

  const [formData, setFormData] = useState({
    employee_id: '',
    age: 30,
    monthly_income: 60000,
    years_at_company: 3,
    years_in_current_role: 2,
    job_satisfaction: 3,
    environment_satisfaction: 3,
    work_life_balance: 3,
    overtime: 0,
    job_level: 2,
    num_companies_worked: 2,
  });

  const [predictionResult, setPredictionResult] = useState(null);
  const [predicting, setPredicting] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [analyticsRes, highRiskRes, empRes] = await Promise.allSettled([
        predictionService.getAnalyticsDashboard(),
        predictionService.getHighRisk(),
        employeeService.list(),
      ]);

      if (analyticsRes.status === 'fulfilled') setAnalytics(analyticsRes.value);
      if (highRiskRes.status === 'fulfilled') setHighRisk(highRiskRes.value || []);
      if (empRes.status === 'fulfilled' && Array.isArray(empRes.value)) {
        setEmployees(empRes.value);
        if (empRes.value.length > 0) {
          setFormData(prev => ({ ...prev, employee_id: empRes.value[0].id }));
        }
      }
    } catch (err) {
      console.error('Data load error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleRunPrediction = async (e) => {
    e.preventDefault();
    setPredicting(true);
    try {
      const payload = {
        ...formData,
        employee_id: parseInt(formData.employee_id),
        age: parseFloat(formData.age),
        monthly_income: parseFloat(formData.monthly_income),
        years_at_company: parseFloat(formData.years_at_company),
        years_in_current_role: parseFloat(formData.years_in_current_role),
        job_satisfaction: parseFloat(formData.job_satisfaction),
        environment_satisfaction: parseFloat(formData.environment_satisfaction),
        work_life_balance: parseFloat(formData.work_life_balance),
        overtime: parseInt(formData.overtime),
        job_level: parseFloat(formData.job_level),
        num_companies_worked: parseFloat(formData.num_companies_worked),
      };
      const res = await predictionService.predict(payload);
      setPredictionResult(res);
      await loadData();
    } catch (err) {
      alert(err.response?.data?.detail || 'Inference failed');
    } finally {
      setPredicting(false);
    }
  };

  // Accurate High Risk & Total Calculations
  const resolvedHighRiskCount = Math.max(
    Number(analytics?.overview?.high_risk || 0),
    highRisk.length
  );

  const resolvedTotalPredictions = Math.max(
    Number(analytics?.overview?.total_predictions || 0),
    resolvedHighRiskCount
  );

  const resolvedMediumRisk = Number(analytics?.overview?.medium_risk || 0);

  // Derive department risk counts directly from high-risk staff & employee registry
  const DEPARTMENTS = ['Engineering', 'Human Resources', 'Finance', 'Marketing', 'Operations'];

  const normalizedDepartmentData = DEPARTMENTS.map(deptName => {
    const highRiskCountInDept = highRisk.filter(hr => {
      const emp = employees.find(e => e.id === hr.employee_id);
      if (!emp) return false;
      const dept = (emp.department || '').toLowerCase();
      const role = (emp.designation || '').toLowerCase();
      const target = deptName.toLowerCase();
      return dept.includes(target) || role.includes(target.split(' ')[0]);
    }).length;

    return {
      department_name: deptName,
      high_risk_count: highRiskCountInDept
    };
  });

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-[#0B0F19] border border-white/10 p-6 rounded-2xl shadow-xl">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Sparkles className="h-4 w-4 text-indigo-400" />
            <span className="text-[10px] uppercase tracking-widest font-mono text-indigo-400 font-bold">Predictive Model v1.0</span>
          </div>
          <h1 className="text-xl font-bold text-white tracking-tight">WorkForce AI Pro — Flight Risk Cockpit</h1>
          <p className="text-xs text-slate-400 mt-0.5">Machine learning powered employee retention analytics</p>
        </div>
        <button
          onClick={() => { setPredictionResult(null); setShowModal(true); }}
          className="px-4 py-2.5 rounded-xl bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-500 hover:to-violet-500 text-white text-xs font-semibold flex items-center gap-2 shadow-lg shadow-indigo-600/30 transition cursor-pointer"
        >
          <PlusCircle className="h-4 w-4" /> Run Prediction
        </button>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {[
          { 
            label: 'Total Predictions', 
            val: resolvedTotalPredictions, 
            icon: BarChart2, 
            color: 'text-indigo-400' 
          },
          { 
            label: 'High Flight Risk', 
            val: resolvedHighRiskCount, 
            icon: AlertTriangle, 
            color: 'text-rose-400' 
          },
          { 
            label: 'Moderate Risk', 
            val: resolvedMediumRisk, 
            icon: Users, 
            color: 'text-amber-400' 
          },
          { 
            label: 'Avg Attrition Score', 
            val: analytics?.overview?.average_attrition_probability 
              ? `${(analytics.overview.average_attrition_probability * 100).toFixed(1)}%` 
              : '0.0%', 
            icon: TrendingUp, 
            color: 'text-emerald-400' 
          },
        ].map((item, idx) => (
          <div key={idx} className="bg-[#0B0F19] border border-white/10 p-5 rounded-2xl">
            <div className="flex justify-between items-start">
              <span className="text-xs font-medium text-slate-400">{item.label}</span>
              <item.icon className={`h-4 w-4 ${item.color}`} />
            </div>
            <div className="text-2xl font-bold text-white mt-2 tracking-tight">{item.val}</div>
          </div>
        ))}
      </div>

      {/* Analytics & High Risk Pool */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Department Analytics Chart */}
        <div className="lg:col-span-2 bg-[#0B0F19] border border-white/10 rounded-2xl p-6">
          <h2 className="text-sm font-semibold text-white mb-1">Department Attrition Vulnerability</h2>
          <p className="text-xs text-slate-400 mb-4">Risk volume mapped by organizational department</p>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={normalizedDepartmentData}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                <XAxis dataKey="department_name" stroke="#64748b" fontSize={11} />
                <YAxis allowDecimals={false} domain={[0, 4]} stroke="#64748b" fontSize={11} />
                <Tooltip 
                  cursor={{ fill: 'rgba(255, 255, 255, 0.03)' }}
                  contentStyle={{ backgroundColor: '#0B0F19', borderColor: 'rgba(255,255,255,0.1)', borderRadius: '8px', fontSize: '12px' }} 
                  formatter={(val) => [`${val} Staff`, 'High Flight Risk']}
                />
                <Bar 
                  dataKey="high_risk_count" 
                  fill="#6366F1" 
                  radius={[4, 4, 0, 0]} 
                  isAnimationActive={false}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* High Risk Employees */}
        <div className="bg-[#0B0F19] border border-white/10 rounded-2xl p-6 flex flex-col justify-between">
          <div>
            <h2 className="text-sm font-semibold text-white mb-1">Critical Flight Risks</h2>
            <p className="text-xs text-slate-400 mb-4">Employees flagged with HIGH risk index</p>
            <div className="space-y-2.5 max-h-60 overflow-y-auto">
              {highRisk.length > 0 ? (
                highRisk.map((risk) => (
                  <div key={risk.id} className="p-3 bg-[#06080F] border border-white/5 rounded-xl flex items-center justify-between text-xs">
                    <div>
                      <span className="font-semibold text-white">Employee #{risk.employee_id}</span>
                      <p className="text-[10px] text-slate-500 font-mono">Model: {risk.model_version}</p>
                    </div>
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-rose-500/10 text-rose-400 border border-rose-500/20">
                      {(risk.attrition_probability * 100).toFixed(1)}% RISK
                    </span>
                  </div>
                ))
              ) : (
                <div className="text-center py-8 text-xs text-slate-500 border border-dashed border-white/5 rounded-xl">
                  No high risk candidates detected.
                </div>
              )}
            </div>
          </div>
          <button 
            onClick={() => { setPredictionResult(null); setShowModal(true); }}
            className="w-full mt-4 py-2 bg-white/5 hover:bg-white/10 text-xs text-slate-300 font-medium rounded-xl border border-white/5 transition cursor-pointer"
          >
            Run New Prediction
          </button>
        </div>
      </div>

      {/* Prediction Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-[#0B0F19] border border-white/10 max-w-lg w-full rounded-2xl p-6 shadow-2xl space-y-4 max-h-[90vh] overflow-y-auto">
            <div className="flex justify-between items-center border-b border-white/10 pb-3">
              <h3 className="text-sm font-bold text-white flex items-center gap-2">
                <Sparkles className="h-4 w-4 text-indigo-400" /> Run AI Attrition Prediction
              </h3>
              <button onClick={() => setShowModal(false)} className="text-slate-400 hover:text-white text-xs cursor-pointer">✕</button>
            </div>

            {predictionResult ? (
              <div className="space-y-4 py-6 text-center">
                <div className={`mx-auto w-16 h-16 rounded-full flex items-center justify-center ${
                  predictionResult.risk_level === 'HIGH' ? 'bg-rose-500/20 text-rose-400 ring-2 ring-rose-500' : 'bg-emerald-500/20 text-emerald-400 ring-2 ring-emerald-500'
                }`}>
                  <ShieldAlert className="h-8 w-8" />
                </div>
                <div>
                  <h4 className="text-lg font-bold text-white">Risk Level: {predictionResult.risk_level}</h4>
                  <p className="text-xs text-slate-400 mt-1">Attrition Probability: <span className="font-bold text-indigo-400">{(predictionResult.attrition_probability * 100).toFixed(1)}%</span></p>
                  <p className="text-[11px] text-slate-500 font-mono mt-1">Model Version: {predictionResult.model_version}</p>
                </div>
                <button
                  onClick={() => setPredictionResult(null)}
                  className="px-4 py-2 bg-white/5 hover:bg-white/10 rounded-xl text-xs font-medium text-slate-300 border border-white/10 cursor-pointer"
                >
                  Run Another Assessment
                </button>
              </div>
            ) : (
              <form onSubmit={handleRunPrediction} className="space-y-3.5 text-xs">
                <div>
                  <label className="text-slate-300 block mb-1">Target Employee ID</label>
                  {employees.length > 0 ? (
                    <select
                      value={formData.employee_id}
                      onChange={(e) => setFormData({ ...formData, employee_id: e.target.value })}
                      className="w-full bg-[#06080F] border border-white/10 rounded-lg p-2 text-slate-200 outline-none focus:border-indigo-500"
                      required
                    >
                      {employees.map(emp => (
                        <option key={emp.id} value={emp.id}>
                          Emp #{emp.id} — {emp.first_name} {emp.last_name} ({emp.designation})
                        </option>
                      ))}
                    </select>
                  ) : (
                    <input
                      type="number"
                      required
                      placeholder="Enter Employee ID (e.g. 1)"
                      value={formData.employee_id}
                      onChange={(e) => setFormData({ ...formData, employee_id: e.target.value })}
                      className="w-full bg-[#06080F] border border-white/10 rounded-lg p-2 text-slate-200 outline-none focus:border-indigo-500"
                    />
                  )}
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="text-slate-300 block mb-1">Age</label>
                    <input type="number" min="18" max="100" value={formData.age} onChange={(e) => setFormData({ ...formData, age: e.target.value })} className="w-full bg-[#06080F] border border-white/10 rounded-lg p-2 text-slate-200 outline-none" required />
                  </div>
                  <div>
                    <label className="text-slate-300 block mb-1">Monthly Income (₹)</label>
                    <input type="number" min="0" value={formData.monthly_income} onChange={(e) => setFormData({ ...formData, monthly_income: e.target.value })} className="w-full bg-[#06080F] border border-white/10 rounded-lg p-2 text-slate-200 outline-none" required />
                  </div>
                </div>

                <div className="grid grid-cols-3 gap-3">
                  <div>
                    <label className="text-slate-300 block mb-1">Tenure (Yrs)</label>
                    <input type="number" min="0" value={formData.years_at_company} onChange={(e) => setFormData({ ...formData, years_at_company: e.target.value })} className="w-full bg-[#06080F] border border-white/10 rounded-lg p-2 text-slate-200 outline-none" required />
                  </div>
                  <div>
                    <label className="text-slate-300 block mb-1">Role Tenure</label>
                    <input type="number" min="0" value={formData.years_in_current_role} onChange={(e) => setFormData({ ...formData, years_in_current_role: e.target.value })} className="w-full bg-[#06080F] border border-white/10 rounded-lg p-2 text-slate-200 outline-none" required />
                  </div>
                  <div>
                    <label className="text-slate-300 block mb-1">Job Level (1-5)</label>
                    <input type="number" min="1" max="5" value={formData.job_level} onChange={(e) => setFormData({ ...formData, job_level: e.target.value })} className="w-full bg-[#06080F] border border-white/10 rounded-lg p-2 text-slate-200 outline-none" required />
                  </div>
                </div>

                <div className="grid grid-cols-3 gap-3">
                  <div>
                    <label className="text-slate-300 block mb-1">Job Sat. (1-5)</label>
                    <input type="number" min="1" max="5" value={formData.job_satisfaction} onChange={(e) => setFormData({ ...formData, job_satisfaction: e.target.value })} className="w-full bg-[#06080F] border border-white/10 rounded-lg p-2 text-slate-200 outline-none" required />
                  </div>
                  <div>
                    <label className="text-slate-300 block mb-1">Env Sat. (1-5)</label>
                    <input type="number" min="1" max="5" value={formData.environment_satisfaction} onChange={(e) => setFormData({ ...formData, environment_satisfaction: e.target.value })} className="w-full bg-[#06080F] border border-white/10 rounded-lg p-2 text-slate-200 outline-none" required />
                  </div>
                  <div>
                    <label className="text-slate-300 block mb-1">Balance (1-5)</label>
                    <input type="number" min="1" max="5" value={formData.work_life_balance} onChange={(e) => setFormData({ ...formData, work_life_balance: e.target.value })} className="w-full bg-[#06080F] border border-white/10 rounded-lg p-2 text-slate-200 outline-none" required />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="text-slate-300 block mb-1">Overtime</label>
                    <select value={formData.overtime} onChange={(e) => setFormData({ ...formData, overtime: e.target.value })} className="w-full bg-[#06080F] border border-white/10 rounded-lg p-2 text-slate-200 outline-none">
                      <option value="0">No (0)</option>
                      <option value="1">Yes (1)</option>
                    </select>
                  </div>
                  <div>
                    <label className="text-slate-300 block mb-1">Prev Companies</label>
                    <input type="number" min="0" value={formData.num_companies_worked} onChange={(e) => setFormData({ ...formData, num_companies_worked: e.target.value })} className="w-full bg-[#06080F] border border-white/10 rounded-lg p-2 text-slate-200 outline-none" required />
                  </div>
                </div>

                <button
                  type="submit"
                  disabled={predicting}
                  className="w-full py-2.5 rounded-xl font-semibold bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-500 text-white transition flex items-center justify-center gap-2 cursor-pointer shadow-lg shadow-indigo-600/25"
                >
                  {predicting ? 'Processing AI Inference...' : 'Calculate Flight Probability'}
                </button>
              </form>
            )}
          </div>
        </div>
      )}
    </div>
  );
}