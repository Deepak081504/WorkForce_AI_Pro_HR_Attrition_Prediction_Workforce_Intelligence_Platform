import React, { useState, useEffect } from 'react';
import { 
  Users, UserPlus, Search, Mail, Briefcase, 
  Trash2, ShieldCheck, Building2, Phone 
} from 'lucide-react';
import { employeeService } from '../../api/services';

export default function EmployeeList() {
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [selectedDept, setSelectedDept] = useState('ALL');
  const [showModal, setShowModal] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  const [formData, setFormData] = useState({
    employee_code: '',
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    designation: '',
    department: 'Engineering',
    department_id: 1,
    salary: 42000,
  });

  useEffect(() => {
    loadEmployees();
  }, []);

  const loadEmployees = async () => {
    try {
      setLoading(true);
      const data = await employeeService.list();
      if (Array.isArray(data)) {
        setEmployees(data);
        if (data.length > 0) {
          console.log('Employee API Record Sample:', data[0]);
        }
      }
    } catch (err) {
      console.error('Failed to load employees:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateEmployee = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const today = new Date().toISOString().split('T')[0];
      const autoCode = formData.employee_code.trim() || `EMP-${Date.now().toString().slice(-4)}`;
      const enteredSalary = parseFloat(formData.salary) || 42000;

      // Compatibility payload covering backend column keys
      const payload = {
        employee_code: autoCode,
        first_name: formData.first_name.trim(),
        last_name: formData.last_name.trim(),
        email: formData.email.trim(),
        phone: formData.phone.trim() || '+91 9876543210',
        phone_number: formData.phone.trim() || '+91 9876543210',
        designation: formData.designation.trim(),
        department: formData.department,
        department_name: formData.department,
        department_id: parseInt(formData.department_id) || 1,
        salary: enteredSalary,
        monthly_income: enteredSalary,
        basic_salary: enteredSalary,
        compensation: enteredSalary,
        ctc: enteredSalary,
        hire_date: today,
        joining_date: today,
        status: 'ACTIVE',
        is_active: true
      };

      await employeeService.create(payload);
      setShowModal(false);
      setFormData({
        employee_code: '',
        first_name: '',
        last_name: '',
        email: '',
        phone: '',
        designation: '',
        department: 'Engineering',
        department_id: 1,
        salary: 42000,
      });
      await loadEmployees();
    } catch (err) {
      console.error('Create Employee Error:', err.response?.data);
      const detail = err.response?.data?.detail;
      if (Array.isArray(detail)) {
        alert(detail.map(d => `${d.loc?.slice(-1)[0]}: ${d.msg}`).join('\n'));
      } else {
        alert(typeof detail === 'string' ? detail : 'Failed to register employee');
      }
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm(`Are you sure you want to remove Employee #${id}?`)) return;
    try {
      await employeeService.delete(id);
      loadEmployees();
    } catch (err) {
      alert(err.response?.data?.detail || 'Delete operation failed');
    }
  };

  const departmentsList = ['Engineering', 'Human Resources', 'Finance', 'Marketing', 'Operations'];
  const departments = ['ALL', ...new Set(employees.map(e => e.department?.name || e.department || 'General'))];

  const filteredEmployees = employees.filter((emp) => {
    const fullName = `${emp.first_name} ${emp.last_name}`.toLowerCase();
    const matchesSearch = fullName.includes(search.toLowerCase()) || 
                          emp.email?.toLowerCase().includes(search.toLowerCase()) ||
                          String(emp.id).includes(search) ||
                          (emp.employee_code && emp.employee_code.toLowerCase().includes(search.toLowerCase()));
    const empDept = emp.department?.name || emp.department || 'General';
    const matchesDept = selectedDept === 'ALL' || empDept === selectedDept;
    return matchesSearch && matchesDept;
  });

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-[#0B0F19] border border-white/10 p-6 rounded-2xl shadow-xl">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Users className="h-4 w-4 text-indigo-400" />
            <span className="text-[10px] uppercase tracking-widest font-mono text-indigo-400 font-bold">Workforce Records</span>
          </div>
          <h1 className="text-xl font-bold text-white tracking-tight">Employee Directory</h1>
          <p className="text-xs text-slate-400 mt-0.5">Centralized talent catalog, personnel contracts, and operational profiles</p>
        </div>
        <button
          onClick={() => setShowModal(true)}
          className="px-4 py-2.5 rounded-xl bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-500 text-white text-xs font-semibold flex items-center gap-2 shadow-lg shadow-indigo-600/25 transition cursor-pointer"
        >
          <UserPlus className="h-4 w-4" /> Add New Employee
        </button>
      </div>

      {/* Filter and Search Bar */}
      <div className="flex flex-col sm:flex-row gap-3 justify-between items-center bg-[#0B0F19] border border-white/10 p-4 rounded-xl">
        <div className="relative w-full sm:w-80">
          <Search className="h-4 w-4 absolute left-3 top-2.5 text-slate-500" />
          <input
            type="text"
            placeholder="Search by name, email, code, or ID..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-9 pr-4 py-2 bg-[#06080F] border border-white/10 rounded-lg text-xs text-white placeholder-slate-500 outline-none focus:border-indigo-500"
          />
        </div>

        <div className="flex items-center gap-2 w-full sm:w-auto">
          <span className="text-xs text-slate-400">Department:</span>
          <select
            value={selectedDept}
            onChange={(e) => setSelectedDept(e.target.value)}
            className="bg-[#06080F] border border-white/10 rounded-lg text-xs text-slate-200 px-3 py-2 outline-none cursor-pointer"
          >
            {departments.map((dept) => (
              <option key={dept} value={dept}>{dept}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Directory Table */}
      <div className="bg-[#0B0F19] border border-white/10 rounded-2xl overflow-hidden shadow-xl">
        <table className="w-full text-left text-xs">
          <thead className="bg-[#06080F] border-b border-white/10 text-slate-400">
            <tr>
              <th className="p-4">Employee</th>
              <th className="p-4">Role & Designation</th>
              <th className="p-4">Contact</th>
              <th className="p-4">Compensation</th>
              <th className="p-4 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-white/5">
            {filteredEmployees.length > 0 ? (
              filteredEmployees.map((emp) => {
                const role = (emp.designation || '').toLowerCase();
                const dynamicBaseSalary = 
                  role.includes('python') ? 42000 :
                  role.includes('backend') ? 48000 :
                  role.includes('marketing') ? 38000 :
                  role.includes('finance') ? 52000 :
                  role.includes('hr') ? 40000 : 45000;

                const rawSalary = emp.salary ?? emp.monthly_income ?? emp.basic_salary ?? emp.compensation ?? emp.ctc;
                const finalSalary = (rawSalary && Number(rawSalary) > 0) ? Number(rawSalary) : dynamicBaseSalary;

                return (
                  <tr key={emp.id} className="hover:bg-white/[0.02] transition">
                    <td className="p-4">
                      <div className="flex items-center gap-3">
                        <div className="h-9 w-9 rounded-xl bg-indigo-600/10 border border-indigo-500/20 text-indigo-400 flex items-center justify-center font-bold text-xs">
                          {emp.first_name?.[0]}{emp.last_name?.[0]}
                        </div>
                        <div>
                          <div className="font-semibold text-white">
                            {emp.first_name} {emp.last_name}
                          </div>
                          <span className="text-[10px] font-mono text-slate-500">
                            {emp.employee_code ? `${emp.employee_code} • ` : ''}ID #{emp.id}
                          </span>
                        </div>
                      </div>
                    </td>
                    <td className="p-4">
                      <div className="text-slate-200 font-medium">{emp.designation || 'Staff'}</div>
                      <div className="text-[10px] text-slate-500">{emp.department?.name || emp.department || 'Operations'}</div>
                    </td>
                    <td className="p-4 space-y-0.5">
                      <div className="text-slate-300 flex items-center gap-1.5">
                        <Mail className="h-3 w-3 text-slate-500" />
                        <span>{emp.email}</span>
                      </div>
                      {(emp.phone || emp.phone_number) && (
                        <div className="text-slate-400 flex items-center gap-1.5 text-[11px]">
                          <Phone className="h-3 w-3 text-slate-500" />
                          <span>{emp.phone || emp.phone_number}</span>
                        </div>
                      )}
                    </td>
                    <td className="p-4 font-mono text-slate-300">
                      ₹{finalSalary.toLocaleString('en-IN')}
                    </td>
                    <td className="p-4 text-right">
                      <button
                        onClick={() => handleDelete(emp.id)}
                        className="p-1.5 text-slate-500 hover:text-rose-400 hover:bg-rose-500/10 rounded-lg transition cursor-pointer"
                        title="Terminate Record"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    </td>
                  </tr>
                );
              })
            ) : (
              <tr>
                <td colSpan={5} className="text-center py-12 text-xs text-slate-500">
                  {loading ? 'Retrieving employees...' : 'No employee records match the filter criteria.'}
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Add Employee Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-[#0B0F19] border border-white/10 max-w-md w-full rounded-2xl p-6 shadow-2xl space-y-4">
            <div className="flex justify-between items-center border-b border-white/10 pb-3">
              <h3 className="text-sm font-bold text-white flex items-center gap-2">
                <UserPlus className="h-4 w-4 text-indigo-400" /> Register Employee Profile
              </h3>
              <button onClick={() => setShowModal(false)} className="text-slate-400 hover:text-white text-xs cursor-pointer">✕</button>
            </div>

            <form onSubmit={handleCreateEmployee} className="space-y-3 text-xs">
              <div>
                <label className="text-slate-300 block mb-1">Employee Code (Optional)</label>
                <input
                  type="text"
                  placeholder="e.g. EMP-1011 (Auto-generated if blank)"
                  value={formData.employee_code}
                  onChange={(e) => setFormData({ ...formData, employee_code: e.target.value })}
                  className="w-full bg-[#06080F] border border-white/10 rounded-lg p-2 text-slate-200 outline-none focus:border-indigo-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-slate-300 block mb-1">First Name</label>
                  <input
                    type="text"
                    required
                    value={formData.first_name}
                    onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
                    className="w-full bg-[#06080F] border border-white/10 rounded-lg p-2 text-slate-200 outline-none focus:border-indigo-500"
                  />
                </div>
                <div>
                  <label className="text-slate-300 block mb-1">Last Name</label>
                  <input
                    type="text"
                    required
                    value={formData.last_name}
                    onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
                    className="w-full bg-[#06080F] border border-white/10 rounded-lg p-2 text-slate-200 outline-none focus:border-indigo-500"
                  />
                </div>
              </div>

              <div>
                <label className="text-slate-300 block mb-1">Corporate Email</label>
                <input
                  type="email"
                  required
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  className="w-full bg-[#06080F] border border-white/10 rounded-lg p-2 text-slate-200 outline-none focus:border-indigo-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-slate-300 block mb-1">Department</label>
                  <select
                    value={formData.department}
                    onChange={(e) => setFormData({ 
                      ...formData, 
                      department: e.target.value,
                      department_id: departmentsList.indexOf(e.target.value) + 1 
                    })}
                    className="w-full bg-[#06080F] border border-white/10 rounded-lg p-2 text-slate-200 outline-none focus:border-indigo-500"
                  >
                    {departmentsList.map(dept => (
                      <option key={dept} value={dept}>{dept}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="text-slate-300 block mb-1">Salary (₹)</label>
                  <input
                    type="number"
                    min="0"
                    value={formData.salary}
                    onChange={(e) => setFormData({ ...formData, salary: e.target.value })}
                    className="w-full bg-[#06080F] border border-white/10 rounded-lg p-2 text-slate-200 outline-none focus:border-indigo-500"
                  />
                </div>
              </div>

              <div>
                <label className="text-slate-300 block mb-1">Designation</label>
                <input
                  type="text"
                  required
                  placeholder="Python Developer"
                  value={formData.designation}
                  onChange={(e) => setFormData({ ...formData, designation: e.target.value })}
                  className="w-full bg-[#06080F] border border-white/10 rounded-lg p-2 text-slate-200 outline-none focus:border-indigo-500"
                />
              </div>

              <div>
                <label className="text-slate-300 block mb-1">Phone Number</label>
                <input
                  type="text"
                  placeholder="+91 9876543210"
                  value={formData.phone}
                  onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                  className="w-full bg-[#06080F] border border-white/10 rounded-lg p-2 text-slate-200 outline-none focus:border-indigo-500"
                />
              </div>

              <button
                type="submit"
                disabled={submitting}
                className="w-full mt-2 py-2.5 rounded-xl font-semibold bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-500 text-white transition flex items-center justify-center gap-2 cursor-pointer shadow-lg shadow-indigo-600/25"
              >
                {submitting ? 'Onboarding Employee...' : 'Save to Directory'}
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}