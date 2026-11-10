import React from 'react';

import { Shield, Activity, User, LogOut, LayoutDashboard, Database, Sliders, Bell } from 'lucide-react';

import { useAuth } from '../../contexts/AuthContext';

import { Badge } from './Badge';



export const Navbar = ({ activeTab, setActiveTab }) => {

  const { user, logout } = useAuth();



  return (

    <nav className="bg-white border-b border-slate-200/90 sticky top-0 z-40 shadow-xs">

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

        <div className="flex items-center justify-between h-16">

          {/* Brand Logo & Title */}

          <div

            className="flex items-center space-x-3 cursor-pointer group"

            onClick={() => setActiveTab(user ? 'dashboard' : 'landing')}

          >

            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-teal-600 to-blue-700 flex items-center justify-center shadow-md shadow-teal-700/15 group-hover:scale-105 transition-transform">

              <Shield className="w-5 h-5 text-white" />

            </div>

            <div>

              <div className="flex items-center space-x-2">

                <span className="text-lg font-bold text-slate-900 tracking-tight">

                  Secure<span className="text-teal-600">FL</span> Health

                </span>

                <span className="hidden sm:inline-block text-[10px] font-semibold tracking-wide uppercase px-2 py-0.5 rounded bg-teal-50 text-teal-700 border border-teal-200">

                  FedAvg Platform

                </span>

              </div>

              <p className="text-[11px] text-slate-500 font-medium hidden sm:block">Privacy-Preserving Clinical AI Network</p>

            </div>

          </div>



          {/* Navigation Links & Action Buttons */}

          <div className="flex items-center space-x-3">

            {user ? (

              <>

                {/* Navigation Pills for Quick Context Switching */}

                <div className="hidden md:flex items-center bg-slate-100/90 p-1 rounded-xl border border-slate-200">

                  <button

                    onClick={() => setActiveTab('dashboard')}

                    className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition ${

                      activeTab === 'dashboard'

                        ? 'bg-white text-slate-900 shadow-xs'

                        : 'text-slate-600 hover:text-slate-900'

                    }`}

                  >

                    Dashboard

                  </button>

                  <button

                    onClick={() => setActiveTab('monitor')}

                    className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center space-x-1.5 transition ${

                      activeTab === 'monitor'

                        ? 'bg-white text-teal-700 shadow-xs'

                        : 'text-slate-600 hover:text-slate-900'

                    }`}

                  >

                    <Activity className="w-3.5 h-3.5 text-teal-600" />

                    <span>FL Monitor</span>

                  </button>

                  <button

                    onClick={() => setActiveTab('security')}

                    className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition ${

                      activeTab === 'security'

                        ? 'bg-white text-purple-700 shadow-xs'

                        : 'text-slate-600 hover:text-slate-900'

                    }`}

                  >

                    Security & Audits

                  </button>

                </div>



                {/* User Identity Chip */}

                <div className="flex items-center space-x-2 pl-2 border-l border-slate-200">

                  <Badge status={user.role} />

                  <div className="hidden sm:flex flex-col text-right">

                    <span className="text-xs font-bold text-slate-900 leading-tight">{user.full_name || 'Authorized User'}</span>

                    <span className="text-[11px] text-slate-500 leading-tight">{user.email}</span>

                  </div>

                  <button

                    onClick={logout}

                    className="p-2 text-slate-400 hover:text-rose-600 rounded-lg hover:bg-rose-50 transition"

                    title="Sign Out"

                  >

                    <LogOut className="w-4 h-4" />

                  </button>

                </div>

              </>

            ) : (

              <div className="flex items-center space-x-3">

                <button

                  onClick={() => setActiveTab('landing')}

                  className={`text-sm font-semibold px-3 py-2 rounded-lg transition ${

                    activeTab === 'landing' ? 'text-teal-700 font-bold' : 'text-slate-600 hover:text-slate-900'

                  }`}

                >

                  Overview

                </button>

                <button

                  onClick={() => setActiveTab('login')}

                  className="text-sm font-semibold text-slate-700 hover:text-slate-900 px-3.5 py-2 rounded-lg hover:bg-slate-100 transition"

                >

                  Sign In

                </button>

                <button

                  onClick={() => setActiveTab('register')}

                  className="text-sm font-semibold bg-teal-600 hover:bg-teal-700 text-white px-4 py-2 rounded-xl shadow-xs transition shadow-teal-600/20"

                >

                  Get Started

                </button>

              </div>

            )}

          </div>

        </div>

      </div>

    </nav>

  );

};
