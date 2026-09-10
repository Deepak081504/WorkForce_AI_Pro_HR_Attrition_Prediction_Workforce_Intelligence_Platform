import React from 'react';
import { Outlet, NavLink, useNavigate } from 'react-router-dom';
import { 
  ShieldAlert, 
  Sparkles, 
  Cpu, 
  Users, 
  BarChart3, 
  CalendarCheck, 
  CalendarDays,
  CreditCard, 
  Award, 
  Briefcase, 
  Settings, 
  LogOut 
} from 'lucide-react';

const NAVIGATION = [
  { name: 'AI Attrition Cockpit', path: '/attrition', icon: ShieldAlert, highlight: true },
  { name: 'Retention Interventions', path: '/interventions', icon: Sparkles },
  { name: 'Model Retraining Hub', path: '/model-training', icon: Cpu },
  { name: 'Employee Directory', path: '/employees', icon: Users },
  { name: 'Workforce Analytics', path: '/analytics', icon: BarChart3 },
  { name: 'Leave & Time-Off', path: '/leaves', icon: CalendarDays },
  { name: 'Performance Hub', path: '/performance', icon: Award },
  { name: 'Recruitment & ATS', path: '/recruitment', icon: Briefcase },
  { name: 'Attendance & Shifts', path: '/attendance', icon: CalendarCheck },
  { name: 'Payroll Engine', path: '/payroll', icon: CreditCard },
  { name: 'System Settings', path: '/settings', icon: Settings },
];

export default function EnterpriseLayout() {
  const navigate = useNavigate();

  let user = { email: 'Admin', role: 'ADMIN' };
  try {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      user = JSON.parse(storedUser);
    }
  } catch (e) {
    console.error('Failed to parse user session', e);
  }

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/login');
  };

  return (
    <div className="flex h-screen bg-[#06080F] text-slate-200 overflow-hidden select-none">
      {/* Sidebar */}
      <aside className="w-72 border-r border-white/10 bg-[#090D17] flex flex-col justify-between p-4 shrink-0">
        <div>
          {/* Logo & Platform Badge */}
          <div className="flex items-center gap-3 px-2 py-4 mb-6">
            <div className="h-9 w-9 rounded-xl bg-gradient-to-tr from-indigo-600 to-violet-500 flex items-center justify-center shadow-lg shadow-indigo-600/30">
              <Cpu className="h-5 w-5 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-1.5">
                <span className="font-bold text-sm tracking-tight text-white">WorkForce</span>
                <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/30">AI Pro</span>
              </div>
              <span className="text-[10px] text-slate-500 tracking-wide uppercase font-semibold">Intelligence Hub</span>
            </div>
          </div>

          {/* Navigation Links */}
          <nav className="space-y-1">
            {NAVIGATION.map((item) => {
              const Icon = item.icon;
              return (
                <NavLink
                  key={item.path}
                  to={item.path}
                  className={({ isActive }) =>
                    `flex items-center justify-between px-3 py-2.5 rounded-xl text-xs font-medium transition ${
                      isActive
                        ? 'bg-indigo-600/15 text-indigo-400 border border-indigo-500/30 font-semibold shadow-inner'
                        : 'text-slate-400 hover:text-slate-200 hover:bg-white/[0.04]'
                    }`
                  }
                >
                  <div className="flex items-center gap-3">
                    <Icon className="h-4 w-4" />
                    <span>{item.name}</span>
                  </div>
                  {item.highlight && (
                    <span className="flex h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
                  )}
                </NavLink>
              );
            })}
          </nav>
        </div>

        {/* User Session & Sign Out */}
        <div className="border-t border-white/10 pt-4 flex items-center justify-between px-2">
          <div className="flex items-center gap-2.5 overflow-hidden">
            <div className="h-8 w-8 rounded-full bg-gradient-to-tr from-indigo-500 to-pink-500 flex items-center justify-center text-xs font-bold text-white shrink-0 shadow-md">
              {user.email ? user.email.slice(0, 2).toUpperCase() : 'WF'}
            </div>
            <div className="truncate">
              <p className="text-xs font-medium text-white truncate">{user.email || 'Admin Console'}</p>
              <span className="text-[10px] text-slate-500 uppercase font-mono">{user.role || 'ADMIN'}</span>
            </div>
          </div>
          <button 
            onClick={handleLogout} 
            className="p-1.5 text-slate-400 hover:text-rose-400 hover:bg-white/5 rounded-lg transition cursor-pointer"
            title="Sign Out"
          >
            <LogOut className="h-4 w-4" />
          </button>
        </div>
      </aside>

      {/* Main Content Dashboard */}
      <main className="flex-1 flex flex-col min-w-0 overflow-y-auto bg-[#06080F]">
        <div className="p-8 max-w-7xl w-full mx-auto">
          <Outlet />
        </div>
      </main>
    </div>
  );
}