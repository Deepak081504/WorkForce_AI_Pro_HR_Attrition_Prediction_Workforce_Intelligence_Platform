import React, { useState, useEffect } from 'react';
import { 
  CalendarCheck, Clock, CheckCircle2, LogIn, 
  LogOut, Users, Search, AlertCircle 
} from 'lucide-react';
import { attendanceService, employeeService } from '../../api/services';

export default function AttendanceShifts() {
  const [attendanceLogs, setAttendanceLogs] = useState([]);
  const [shifts, setShifts] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [selectedEmpId, setSelectedEmpId] = useState('');
  const [actionLoading, setActionLoading] = useState(false);
  const [search, setSearch] = useState('');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [attRes, shiftRes, empRes] = await Promise.allSettled([
        attendanceService.list(),
        attendanceService.getShifts(),
        employeeService.list(),
      ]);

      if (attRes.status === 'fulfilled' && Array.isArray(attRes.value)) {
        // Sort descending so the most recent punch appears first
        const sorted = [...attRes.value].sort((a, b) => {
          const dateDiff = new Date(b.attendance_date) - new Date(a.attendance_date);
          return dateDiff !== 0 ? dateDiff : b.id - a.id;
        });

        // Deduplicate: Keep only the most recent attendance log per employee
        const seen = new Set();
        const uniqueLogs = sorted.filter((log) => {
          const key = String(log.employee_id);
          if (seen.has(key)) return false;
          seen.add(key);
          return true;
        });

        setAttendanceLogs(uniqueLogs);
      }

      if (shiftRes.status === 'fulfilled' && Array.isArray(shiftRes.value)) {
        setShifts(shiftRes.value);
      }

      if (empRes.status === 'fulfilled' && Array.isArray(empRes.value)) {
        setEmployees(empRes.value);
        if (empRes.value.length > 0 && !selectedEmpId) {
          setSelectedEmpId(empRes.value[0].id);
        }
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleCheckIn = async () => {
    if (!selectedEmpId) return alert('Please select an employee');
    setActionLoading(true);

    try {
      const now = new Date();
      const payload = {
        employee_id: parseInt(selectedEmpId),
        shift_id: shifts.length > 0 ? shifts[0].id : 1,
        attendance_date: now.toISOString().split('T')[0],
        check_in: now.toTimeString().split(' ')[0],
        check_out: null,
        status: 'PRESENT',
        remarks: 'Biometric punch via Console',
      };

      await attendanceService.create(payload);
      await loadData();
    } catch (err) {
      const detail = err.response?.data?.detail;
      alert(typeof detail === 'string' ? detail : 'Check-in failed. Employee may already have attendance today.');
    } finally {
      setActionLoading(false);
    }
  };

  const handleCheckOut = async () => {
    if (!selectedEmpId) return alert('Please select an employee');
    setActionLoading(true);

    try {
      const activeRecord = attendanceLogs.find(
        (log) => log.employee_id === parseInt(selectedEmpId) && 
                 (!log.check_out || log.check_out === null)
      );

      if (!activeRecord) {
        return alert('No active check-in session found for this employee to check out.');
      }

      const now = new Date();
      const updatePayload = {
        ...activeRecord,
        check_out: now.toTimeString().split(' ')[0],
      };

      await attendanceService.update(activeRecord.id, updatePayload);
      await loadData();
    } catch (err) {
      const detail = err.response?.data?.detail;
      alert(typeof detail === 'string' ? detail : 'Check-out update failed.');
    } finally {
      setActionLoading(false);
    }
  };

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

  const filteredLogs = attendanceLogs.filter(log => {
    const empInfo = getEmployeeInfo(log.employee_id);
    const searchLower = search.toLowerCase();
    return (
      String(log.employee_id).includes(searchLower) ||
      empInfo.name.toLowerCase().includes(searchLower) ||
      (log.status && log.status.toLowerCase().includes(searchLower)) ||
      (log.attendance_date && log.attendance_date.includes(searchLower))
    );
  });

  return (
    <div className="space-y-6">
      {/* Top Banner & Live Punch Terminal */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-[#0B0F19] border border-white/10 p-6 rounded-2xl shadow-xl">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <CalendarCheck className="h-4 w-4 text-indigo-400" />
            <span className="text-[10px] uppercase tracking-widest font-mono text-indigo-400 font-bold">Shift & Time Operations</span>
          </div>
          <h1 className="text-xl font-bold text-white tracking-tight">Attendance & Shift Scheduling</h1>
          <p className="text-xs text-slate-400 mt-0.5">Biometric punch simulation, active shifts, and daily work records</p>
        </div>

        {/* Live Punch Actions */}
        <div className="flex items-center gap-2.5 bg-[#06080F] border border-white/10 p-2.5 rounded-xl">
          <select
            value={selectedEmpId}
            onChange={(e) => setSelectedEmpId(e.target.value)}
            className="bg-[#0B0F19] text-xs text-slate-200 border border-white/10 rounded-lg px-2.5 py-1.5 outline-none cursor-pointer"
          >
            {employees.map(emp => (
              <option key={emp.id} value={emp.id}>
                #{emp.id} - {emp.first_name} {emp.last_name}
              </option>
            ))}
          </select>
          <button
            onClick={handleCheckIn}
            disabled={actionLoading}
            className="px-3.5 py-1.5 bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition disabled:opacity-50 cursor-pointer"
          >
            <LogIn className="h-3.5 w-3.5" /> Check In
          </button>
          <button
            onClick={handleCheckOut}
            disabled={actionLoading}
            className="px-3.5 py-1.5 bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 border border-rose-500/30 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition disabled:opacity-50 cursor-pointer"
          >
            <LogOut className="h-3.5 w-3.5" /> Check Out
          </button>
        </div>
      </div>

      {/* Shifts Grid */}
      <div>
        <h2 className="text-sm font-semibold text-white mb-3">Configured Shift Bands</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {shifts.length > 0 ? (
            shifts.map((shift) => (
              <div key={shift.id} className="bg-[#0B0F19] border border-white/10 p-4 rounded-xl">
                <div className="flex justify-between items-center">
                  <span className="font-semibold text-white text-xs">{shift.name || shift.shift_name}</span>
                  <span className="text-[10px] px-2 py-0.5 bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 rounded font-mono">
                    ID #{shift.id}
                  </span>
                </div>
                <div className="flex items-center gap-2 text-xs text-slate-400 mt-2">
                  <Clock className="h-3.5 w-3.5 text-slate-500" />
                  <span>{shift.start_time} - {shift.end_time}</span>
                </div>
              </div>
            ))
          ) : (
            <div className="col-span-3 text-xs text-slate-500 p-4 bg-[#0B0F19] border border-white/5 rounded-xl text-center">
              No shift rosters available.
            </div>
          )}
        </div>
      </div>

      {/* Daily Punch Logs Table */}
      <div className="bg-[#0B0F19] border border-white/10 rounded-2xl overflow-hidden shadow-xl">
        <div className="p-4 border-b border-white/10 flex justify-between items-center">
          <div>
            <h2 className="text-sm font-semibold text-white">Daily Punch Telemetry</h2>
            <p className="text-xs text-slate-400">Live employee check-in and check-out logs</p>
          </div>
          <div className="relative">
            <Search className="h-3.5 w-3.5 absolute left-3 top-2.5 text-slate-500" />
            <input
              type="text"
              placeholder="Search by Employee or Date..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="pl-8 pr-3 py-1.5 bg-[#06080F] border border-white/10 rounded-lg text-xs text-white placeholder-slate-500 outline-none w-56"
            />
          </div>
        </div>

        <table className="w-full text-left text-xs">
          <thead className="bg-[#06080F] border-b border-white/10 text-slate-400">
            <tr>
              <th className="p-4">Record ID</th>
              <th className="p-4">Employee</th>
              <th className="p-4">Date</th>
              <th className="p-4">Check In</th>
              <th className="p-4">Check Out</th>
              <th className="p-4">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-white/5">
            {filteredLogs.length > 0 ? (
              filteredLogs.map((log) => {
                const empInfo = getEmployeeInfo(log.employee_id);
                return (
                  <tr key={log.id} className="hover:bg-white/[0.02] transition">
                    <td className="p-4 text-slate-400 font-mono">#{log.id}</td>
                    <td className="p-4">
                      <div className="text-white font-medium">{empInfo.name}</div>
                      <span className="text-[10px] text-slate-500 font-mono">ID: #{log.employee_id} • {empInfo.role}</span>
                    </td>
                    <td className="p-4 text-slate-300 font-mono">{log.attendance_date}</td>
                    <td className="p-4 text-slate-300 font-mono">{log.check_in || '—'}</td>
                    <td className="p-4 text-slate-300 font-mono">{log.check_out || 'Active Session'}</td>
                    <td className="p-4">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                        log.status === 'PRESENT'
                          ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                          : 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                      }`}>
                        {log.status || 'LOGGED'}
                      </span>
                    </td>
                  </tr>
                );
              })
            ) : (
              <tr>
                <td colSpan={6} className="text-center py-10 text-xs text-slate-500">
                  No attendance records found. Use the terminal above to punch in.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}