import React, { useState, useEffect } from 'react';
import { 
  CalendarDays, PlusCircle, CheckCircle2, XCircle, 
  Clock, AlertCircle, Search, UserCheck, ShieldCheck 
} from 'lucide-react';
import { employeeService } from '../../api/services';

const LEAVE_TYPES = ['Paid Time Off (PTO)', 'Sick Leave', 'Casual Leave', 'Maternity/Paternity', 'Unpaid Leave'];

export default function LeaveManagement() {
  const [employees, setEmployees] = useState([]);
  const [leaves, setLeaves] = useState([
    {
      id: 'LV-101',
      employee_id: 10,
      employee_name: 'Anand Kasinathan',
      leave_type: 'Paid Time Off (PTO)',
      start_date: '2026-09-15',
      end_date: '2026-09-17',
      days: 3,
      reason: 'Family function & personal commitments',
      status: 'PENDING',
      applied_on: '2026-09-10'
    },
    {
      id: 'LV-102',
      employee_id: 9,
      employee_name: 'Divya Priyan',
      leave_type: 'Sick Leave',
      start_date: '2026-09-08',
      end_date: '2026-09-09',
      days: 2,
      reason: 'Viral fever and recovery',
      status: 'APPROVED',
      applied_on: '2026-09-07'
    },
    {
      id: 'LV-103',
      employee_id: 11,
      employee_name: 'Surya Prakash',
      leave_type: 'Casual Leave',
      start_date: '2026-09-01',
      end_date: '2026-09-01',
      days: 1,
      reason: 'Personal documentation work',
      status: 'REJECTED',
      applied_on: '2026-08-30'
    }
  ]);

  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('ALL');
  const [showModal, setShowModal] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  const [formData, setFormData] = useState({
    employee_id: '',
    leave_type: 'Paid Time Off (PTO)',
    start_date: '',
    end_date: '',
    reason: ''
  });

  useEffect(() => {
    loadEmployees();
  }, []);

  const loadEmployees = async () => {
    try {
      const data = await employeeService.list();
      if (Array.isArray(data) && data.length > 0) {
        setEmployees(data);
        setFormData(prev => ({ ...prev, employee_id: data[0].id }));
      }
    } catch (err) {
      console.error('Failed to load employee list:', err);
    }
  };

  const handleApplyLeave = (e) => {
    e.preventDefault();
    setSubmitting(true);

    const selectedEmp = employees.find(emp => String(emp.id) === String(formData.employee_id));
    const start = new Date(formData.start_date);
    const end = new Date(formData.end_date);
    const diffTime = Math.abs(end - start);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1;

    const newLeave = {
      id: `LV-${Date.now().toString().slice(-4)}`,
      employee_id: formData.employee_id,
      employee_name: selectedEmp ? `${selectedEmp.first_name} ${selectedEmp.last_name}` : 'Staff Member',
      leave_type: formData.leave_type,
      start_date: formData.start_date,
      end_date: formData.end_date,
      days: diffDays > 0 ? diffDays : 1,
      reason: formData.reason,
      status: 'PENDING',
      applied_on: new Date().toISOString().split('T')[0]
    };

    setLeaves([newLeave, ...leaves]);
    setShowModal(false);
    setSubmitting(false);
    setFormData({
      employee_id: employees[0]?.id || '',
      leave_type: 'Paid Time Off (PTO)',
      start_date: '',
      end_date: '',
      reason: ''
    });
  };

  const updateStatus = (id, newStatus) => {
    setLeaves(leaves.map(item => item.id === id ? { ...item, status: newStatus } : item));
  };

  const filteredLeaves = leaves.filter(item => {
    const matchesSearch = item.employee_name.toLowerCase().includes(search.toLowerCase()) ||
                          item.id.toLowerCase().includes(search.toLowerCase()) ||
                          item.reason.toLowerCase().includes(search.toLowerCase());
    const matchesStatus = statusFilter === 'ALL' || item.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  const stats = {
    pending: leaves.filter(l => l.status === 'PENDING').length,
    approved: leaves.filter(l => l.status === 'APPROVED').length,
    rejected: leaves.filter(l => l.status === 'REJECTED').length,
    totalDays: leaves.filter(l => l.status === 'APPROVED').reduce((acc, curr) => acc + curr.days, 0)
  };

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-[#0B0F19] border border-white/10 p-6 rounded-2xl shadow-xl">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <CalendarDays className="h-4 w-4 text-indigo-400" />
            <span className="text-[10px] uppercase tracking-widest font-mono text-indigo-400 font-bold">Attendance & Operations</span>
          </div>
          <h1 className="text-xl font-bold text-white tracking-tight">Leave & Time-Off Management</h1>
          <p className="text-xs text-slate-400 mt-0.5">Track personnel availability, sanction employee requests, and monitor time-off balances</p>
        </div>
        <button
          onClick={() => setShowModal(true)}
          className="px-4 py-2.5 rounded-xl bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-500 text-white text-xs font-semibold flex items-center gap-2 shadow-lg shadow-indigo-600/25 transition cursor-pointer"
        >
          <PlusCircle className="h-4 w-4" /> File Leave Request
        </button>
      </div>

      {/* KPI Balance Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { label: 'Pending Approvals', val: stats.pending, icon: Clock, color: 'text-amber-400', badge: 'Requires Action' },
          { label: 'Sanctioned Requests', val: stats.approved, icon: CheckCircle2, color: 'text-emerald-400', badge: 'Active Cycle' },
          { label: 'Declined Applications', val: stats.rejected, icon: XCircle, color: 'text-rose-400', badge: 'Archived' },
          { label: 'Approved Leave Days', val: `${stats.totalDays} Days`, icon: UserCheck, color: 'text-indigo-400', badge: 'Monthly Utilization' },
        ].map((kpi, idx) => (
          <div key={idx} className="bg-[#0B0F19] border border-white/10 p-5 rounded-2xl">
            <div className="flex justify-between items-start">
              <span className="text-xs font-medium text-slate-400">{kpi.label}</span>
              <kpi.icon className={`h-4 w-4 ${kpi.color}`} />
            </div>
            <div className="text-2xl font-bold text-white mt-2 tracking-tight">{kpi.val}</div>
            <span className="text-[10px] text-slate-500 mt-1 block">{kpi.badge}</span>
          </div>
        ))}
      </div>

      {/* Search and Filters */}
      <div className="flex flex-col sm:flex-row gap-3 justify-between items-center bg-[#0B0F19] border border-white/10 p-4 rounded-xl">
        <div className="relative w-full sm:w-80">
          <Search className="h-4 w-4 absolute left-3 top-2.5 text-slate-500" />
          <input
            type="text"
            placeholder="Search request by employee, ID, or reason..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-9 pr-4 py-2 bg-[#06080F] border border-white/10 rounded-lg text-xs text-white placeholder-slate-500 outline-none focus:border-indigo-500"
          />
        </div>

        <div className="flex items-center gap-2 w-full sm:w-auto">
          <span className="text-xs text-slate-400">Status:</span>
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="bg-[#06080F] border border-white/10 rounded-lg text-xs text-slate-200 px-3 py-2 outline-none cursor-pointer"
          >
            {['ALL', 'PENDING', 'APPROVED', 'REJECTED'].map((st) => (
              <option key={st} value={st}>{st}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Leave Ledger Table */}
      <div className="bg-[#0B0F19] border border-white/10 rounded-2xl overflow-hidden shadow-xl">
        <table className="w-full text-left text-xs">
          <thead className="bg-[#06080F] border-b border-white/10 text-slate-400">
            <tr>
              <th className="p-4">Reference & Personnel</th>
              <th className="p-4">Leave Category</th>
              <th className="p-4">Duration & Dates</th>
              <th className="p-4">Reason / Notes</th>
              <th className="p-4">Status</th>
              <th className="p-4 text-right">Sanction Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-white/5">
            {filteredLeaves.length > 0 ? (
              filteredLeaves.map((item) => (
                <tr key={item.id} className="hover:bg-white/[0.02] transition">
                  <td className="p-4">
                    <div className="font-semibold text-white">{item.employee_name}</div>
                    <span className="text-[10px] font-mono text-slate-500">{item.id} • Applied: {item.applied_on}</span>
                  </td>
                  <td className="p-4">
                    <span className="text-slate-200 font-medium">{item.leave_type}</span>
                  </td>
                  <td className="p-4">
                    <div className="text-slate-200">{item.start_date} → {item.end_date}</div>
                    <span className="text-[10px] font-mono text-indigo-400 font-semibold">{item.days} {item.days > 1 ? 'Days' : 'Day'}</span>
                  </td>
                  <td className="p-4 text-slate-400 max-w-xs truncate" title={item.reason}>
                    {item.reason}
                  </td>
                  <td className="p-4">
                    <span className={`px-2.5 py-1 rounded-full text-[10px] font-bold tracking-wider ${
                      item.status === 'APPROVED' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' :
                      item.status === 'REJECTED' ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20' :
                      'bg-amber-500/10 text-amber-400 border border-amber-500/20 animate-pulse'
                    }`}>
                      {item.status}
                    </span>
                  </td>
                  <td className="p-4 text-right">
                    {item.status === 'PENDING' ? (
                      <div className="flex items-center justify-end gap-2">
                        <button
                          onClick={() => updateStatus(item.id, 'APPROVED')}
                          className="px-2.5 py-1 rounded-lg bg-emerald-600/20 text-emerald-400 hover:bg-emerald-600 hover:text-white border border-emerald-500/30 transition text-[11px] font-medium cursor-pointer"
                        >
                          Approve
                        </button>
                        <button
                          onClick={() => updateStatus(item.id, 'REJECTED')}
                          className="px-2.5 py-1 rounded-lg bg-rose-600/20 text-rose-400 hover:bg-rose-600 hover:text-white border border-rose-500/30 transition text-[11px] font-medium cursor-pointer"
                        >
                          Decline
                        </button>
                      </div>
                    ) : (
                      <span className="text-[11px] text-slate-500">Completed</span>
                    )}
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={6} className="text-center py-12 text-xs text-slate-500">
                  No leave applications match the selected criteria.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* File Leave Request Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-[#0B0F19] border border-white/10 max-w-md w-full rounded-2xl p-6 shadow-2xl space-y-4">
            <div className="flex justify-between items-center border-b border-white/10 pb-3">
              <h3 className="text-sm font-bold text-white flex items-center gap-2">
                <CalendarDays className="h-4 w-4 text-indigo-400" /> Apply Time-Off Request
              </h3>
              <button onClick={() => setShowModal(false)} className="text-slate-400 hover:text-white text-xs cursor-pointer">✕</button>
            </div>

            <form onSubmit={handleApplyLeave} className="space-y-3 text-xs">
              <div>
                <label className="text-slate-300 block mb-1">Select Employee</label>
                <select
                  value={formData.employee_id}
                  onChange={(e) => setFormData({ ...formData, employee_id: e.target.value })}
                  className="w-full bg-[#06080F] border border-white/10 rounded-lg p-2 text-slate-200 outline-none focus:border-indigo-500"
                >
                  {employees.map(emp => (
                    <option key={emp.id} value={emp.id}>
                      {emp.first_name} {emp.last_name} ({emp.designation || 'Staff'})
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="text-slate-300 block mb-1">Leave Classification</label>
                <select
                  value={formData.leave_type}
                  onChange={(e) => setFormData({ ...formData, leave_type: e.target.value })}
                  className="w-full bg-[#06080F] border border-white/10 rounded-lg p-2 text-slate-200 outline-none focus:border-indigo-500"
                >
                  {LEAVE_TYPES.map(type => (
                    <option key={type} value={type}>{type}</option>
                  ))}
                </select>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-slate-300 block mb-1">Commencement Date</label>
                  <input
                    type="date"
                    required
                    value={formData.start_date}
                    onChange={(e) => setFormData({ ...formData, start_date: e.target.value })}
                    className="w-full bg-[#06080F] border border-white/10 rounded-lg p-2 text-slate-200 outline-none focus:border-indigo-500"
                  />
                </div>
                <div>
                  <label className="text-slate-300 block mb-1">Conclusion Date</label>
                  <input
                    type="date"
                    required
                    value={formData.end_date}
                    onChange={(e) => setFormData({ ...formData, end_date: e.target.value })}
                    className="w-full bg-[#06080F] border border-white/10 rounded-lg p-2 text-slate-200 outline-none focus:border-indigo-500"
                  />
                </div>
              </div>

              <div>
                <label className="text-slate-300 block mb-1">Reason / Operational Justification</label>
                <textarea
                  required
                  rows={3}
                  placeholder="Provide brief context for approval lead..."
                  value={formData.reason}
                  onChange={(e) => setFormData({ ...formData, reason: e.target.value })}
                  className="w-full bg-[#06080F] border border-white/10 rounded-lg p-2 text-slate-200 outline-none focus:border-indigo-500 resize-none"
                />
              </div>

              <button
                type="submit"
                disabled={submitting}
                className="w-full mt-2 py-2.5 rounded-xl font-semibold bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-500 text-white transition flex items-center justify-center gap-2 cursor-pointer shadow-lg shadow-indigo-600/25"
              >
                {submitting ? 'Submitting Application...' : 'Submit Leave Request'}
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}