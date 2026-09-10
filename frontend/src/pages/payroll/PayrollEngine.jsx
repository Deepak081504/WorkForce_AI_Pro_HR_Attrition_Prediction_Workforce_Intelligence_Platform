import React, { useState, useEffect } from 'react';
import { 
  CreditCard, DollarSign, PlusCircle, CheckCircle2, 
  Search, FileText, TrendingUp, AlertCircle 
} from 'lucide-react';
import { payrollService, employeeService } from '../../api/services';

export default function PayrollEngine() {
  const [payrolls, setPayrolls] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [search, setSearch] = useState('');

  const now = new Date();
  const currentPeriod = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`;
  const currentDate = now.toISOString().split('T')[0];

  const [formData, setFormData] = useState({
    employee_id: '',
    pay_period: currentPeriod,
    pay_date: currentDate,
    basic_salary: 45000,
    allowances: 10000,
    deductions: 5000,
    bonus: 2000,
    status: 'PAID',
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [payrollRes, empRes] = await Promise.allSettled([
        payrollService.list(),
        employeeService.list(),
      ]);

      if (payrollRes.status === 'fulfilled' && Array.isArray(payrollRes.value)) {
        // Deduplicate records: latest record per employee for a clean ledger
        const seen = new Set();
        const uniquePayrolls = payrollRes.value.filter((item) => {
          const key = `${item.employee_id}`;
          if (seen.has(key)) {
            return false;
          }
          seen.add(key);
          return true;
        });

        setPayrolls(uniquePayrolls);
      }

      if (empRes.status === 'fulfilled' && Array.isArray(empRes.value)) {
        setEmployees(empRes.value);
        if (empRes.value.length > 0 && !formData.employee_id) {
          setFormData(prev => ({ ...prev, employee_id: empRes.value[0].id }));
        }
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleGeneratePayroll = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const payload = {
        employee_id: parseInt(formData.employee_id),
        pay_period: formData.pay_period,
        pay_date: formData.pay_date,
        basic_salary: parseFloat(formData.basic_salary),
        allowances: parseFloat(formData.allowances || 0),
        deductions: parseFloat(formData.deductions || 0),
        bonus: parseFloat(formData.bonus || 0),
        status: formData.status,
      };

      await payrollService.create(payload);
      setShowModal(false);
      loadData();
    } catch (err) {
      const detail = err.response?.data?.detail;
      alert(typeof detail === 'string' ? detail : 'Failed to generate payroll slip.');
    } finally {
      setSubmitting(false);
    }
  };

  const totalDisbursed = payrolls.reduce((acc, curr) => {
    const net = (curr.basic_salary || 0) + (curr.allowances || 0) + (curr.bonus || 0) - (curr.deductions || 0);
    return acc + (curr.net_salary || net);
  }, 0);

  const averageSalary = payrolls.length > 0 ? Math.round(totalDisbursed / payrolls.length) : 0;

  const getEmployeeInfo = (empId) => {
    const emp = employees.find(e => String(e.id) === String(empId));
    if (emp) {
      return {
        name: `${emp.first_name} ${emp.last_name}`,
        role: emp.designation || 'Staff Member'
      };
    }
    return {
      name: `Employee #${empId}`,
      role: 'Operations'
    };
  };

  const filteredPayrolls = payrolls.filter(p => {
    const empInfo = getEmployeeInfo(p.employee_id);
    const searchLower = search.toLowerCase();
    return (
      String(p.employee_id).includes(searchLower) ||
      empInfo.name.toLowerCase().includes(searchLower) ||
      (p.pay_period && p.pay_period.toLowerCase().includes(searchLower)) ||
      (p.status && p.status.toLowerCase().includes(searchLower))
    );
  });

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-[#0B0F19] border border-white/10 p-6 rounded-2xl shadow-xl">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <CreditCard className="h-4 w-4 text-indigo-400" />
            <span className="text-[10px] uppercase tracking-widest font-mono text-indigo-400 font-bold">Compensation & Finance Ops</span>
          </div>
          <h1 className="text-xl font-bold text-white tracking-tight">Payroll Engine</h1>
          <p className="text-xs text-slate-400 mt-0.5">Automated statutory computations, disbursements, and pay-ledger registers</p>
        </div>
        <button
          onClick={() => setShowModal(true)}
          className="px-4 py-2.5 rounded-xl bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-500 text-white text-xs font-semibold flex items-center gap-2 shadow-lg shadow-indigo-600/25 transition cursor-pointer"
        >
          <PlusCircle className="h-4 w-4" /> Run Payroll Batch
        </button>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {[
          { label: 'Total Compensation Disbursed', val: `₹${totalDisbursed.toLocaleString('en-IN')}`, icon: DollarSign, color: 'text-emerald-400' },
          { label: 'Processed Pay Slips', val: payrolls.length, icon: FileText, color: 'text-indigo-400' },
          { label: 'Average Department Net Pay', val: `₹${averageSalary.toLocaleString('en-IN')}`, icon: TrendingUp, color: 'text-violet-400' },
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

      {/* Ledger Table */}
      <div className="bg-[#0B0F19] border border-white/10 rounded-2xl overflow-hidden shadow-xl">
        <div className="p-4 border-b border-white/10 flex justify-between items-center">
          <div>
            <h2 className="text-sm font-semibold text-white">Salary Ledger & Slips</h2>
            <p className="text-xs text-slate-400">Employee monthly gross, statutory deductions, bonus, and net pay</p>
          </div>
          <div className="relative">
            <Search className="h-3.5 w-3.5 absolute left-3 top-2.5 text-slate-500" />
            <input
              type="text"
              placeholder="Search Employee / Period..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="pl-8 pr-3 py-1.5 bg-[#06080F] border border-white/10 rounded-lg text-xs text-white placeholder-slate-500 outline-none w-56"
            />
          </div>
        </div>

        <table className="w-full text-left text-xs">
          <thead className="bg-[#06080F] border-b border-white/10 text-slate-400">
            <tr>
              <th className="p-4">Pay Slip #</th>
              <th className="p-4">Employee</th>
              <th className="p-4">Period</th>
              <th className="p-4">Basic Pay</th>
              <th className="p-4">Allowances + Bonus</th>
              <th className="p-4">Deductions</th>
              <th className="p-4">Net Payable</th>
              <th className="p-4">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-white/5">
            {filteredPayrolls.length > 0 ? (
              filteredPayrolls.map((p) => {
                const add = (p.allowances || 0) + (p.bonus || 0);
                const net = p.net_salary || ((p.basic_salary || 0) + add - (p.deductions || 0));
                const empInfo = getEmployeeInfo(p.employee_id);

                return (
                  <tr key={p.id} className="hover:bg-white/[0.02] transition">
                    <td className="p-4 font-mono text-slate-400">#PAY-{p.id}</td>
                    <td className="p-4">
                      <div className="text-white font-medium">{empInfo.name}</div>
                      <span className="text-[10px] text-slate-500 font-mono">ID: #{p.employee_id} • {empInfo.role}</span>
                    </td>
                    <td className="p-4 font-mono text-slate-300">{p.pay_period || p.pay_date}</td>
                    <td className="p-4 text-slate-300 font-mono">₹{Number(p.basic_salary).toLocaleString('en-IN')}</td>
                    <td className="p-4 text-emerald-400 font-mono">+₹{Number(add).toLocaleString('en-IN')}</td>
                    <td className="p-4 text-rose-400 font-mono">-₹{Number(p.deductions || 0).toLocaleString('en-IN')}</td>
                    <td className="p-4 font-bold text-white font-mono">₹{Number(net).toLocaleString('en-IN')}</td>
                    <td className="p-4">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                        p.status === 'PAID'
                          ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                          : 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                      }`}>
                        {p.status || 'PAID'}
                      </span>
                    </td>
                  </tr>
                );
              })
            ) : (
              <tr>
                <td colSpan={8} className="text-center py-10 text-xs text-slate-500">
                  {loading ? 'Fetching salary ledger...' : 'No payroll records found.'}
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Process Payroll Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-[#0B0F19] border border-white/10 max-w-md w-full rounded-2xl p-6 shadow-2xl space-y-4">
            <div className="flex justify-between items-center border-b border-white/10 pb-3">
              <h3 className="text-sm font-bold text-white flex items-center gap-2">
                <CreditCard className="h-4 w-4 text-indigo-400" /> Process Salary Slip
              </h3>
              <button onClick={() => setShowModal(false)} className="text-slate-400 hover:text-white text-xs cursor-pointer">✕</button>
            </div>

            <form onSubmit={handleGeneratePayroll} className="space-y-3 text-xs">
              <div>
                <label className="text-slate-300 block mb-1">Target Employee</label>
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
                    placeholder="Employee ID"
                    value={formData.employee_id}
                    onChange={(e) => setFormData({ ...formData, employee_id: e.target.value })}
                    className="w-full bg-[#06080F] border border-white/10 rounded-lg p-2 text-slate-200 outline-none"
                  />
                )}
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-slate-300 block mb-1">Pay Period</label>
                  <input
                    type="text"
                    placeholder="2026-09"
                    value={formData.pay_period}
                    onChange={(e) => setFormData({ ...formData, pay_period: e.target.value })}
                    className="w-full bg-[#06080F] border border-white/10 rounded-lg p-2 text-slate-200 outline-none"
                    required
                  />
                </div>
                <div>
                  <label className="text-slate-300 block mb-1">Disbursement Date</label>
                  <input
                    type="date"
                    value={formData.pay_date}
                    onChange={(e) => setFormData({ ...formData, pay_date: e.target.value })}
                    className="w-full bg-[#06080F] border border-white/10 rounded-lg p-2 text-slate-200 outline-none"
                    required
                  />
                </div>
              </div>

              <div>
                <label className="text-slate-300 block mb-1">Basic Salary (₹)</label>
                <input
                  type="number"
                  min="0"
                  value={formData.basic_salary}
                  onChange={(e) => setFormData({ ...formData, basic_salary: e.target.value })}
                  className="w-full bg-[#06080F] border border-white/10 rounded-lg p-2 text-slate-200 outline-none"
                  required
                />
              </div>

              <div className="grid grid-cols-3 gap-2">
                <div>
                  <label className="text-slate-300 block mb-1">Allowances (₹)</label>
                  <input
                    type="number"
                    min="0"
                    value={formData.allowances}
                    onChange={(e) => setFormData({ ...formData, allowances: e.target.value })}
                    className="w-full bg-[#06080F] border border-white/10 rounded-lg p-2 text-slate-200 outline-none"
                  />
                </div>
                <div>
                  <label className="text-slate-300 block mb-1">Bonus (₹)</label>
                  <input
                    type="number"
                    min="0"
                    value={formData.bonus}
                    onChange={(e) => setFormData({ ...formData, bonus: e.target.value })}
                    className="w-full bg-[#06080F] border border-white/10 rounded-lg p-2 text-slate-200 outline-none"
                  />
                </div>
                <div>
                  <label className="text-slate-300 block mb-1">Deductions (₹)</label>
                  <input
                    type="number"
                    min="0"
                    value={formData.deductions}
                    onChange={(e) => setFormData({ ...formData, deductions: e.target.value })}
                    className="w-full bg-[#06080F] border border-white/10 rounded-lg p-2 text-slate-200 outline-none"
                  />
                </div>
              </div>

              <div className="p-3 bg-[#06080F] border border-white/5 rounded-xl flex justify-between items-center text-xs">
                <span className="text-slate-400">Net Payable:</span>
                <span className="font-bold text-white font-mono text-sm">
                  ₹{(parseFloat(formData.basic_salary || 0) + parseFloat(formData.allowances || 0) + parseFloat(formData.bonus || 0) - parseFloat(formData.deductions || 0)).toLocaleString('en-IN')}
                </span>
              </div>

              <button
                type="submit"
                disabled={submitting}
                className="w-full py-2.5 rounded-xl font-semibold bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-500 text-white transition flex items-center justify-center gap-2 cursor-pointer shadow-lg shadow-indigo-600/25"
              >
                {submitting ? 'Generating Slip...' : 'Confirm & Disburse'}
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}