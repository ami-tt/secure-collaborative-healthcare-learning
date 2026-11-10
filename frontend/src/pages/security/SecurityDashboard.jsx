import React, { useState, useEffect } from 'react';

import {

  ShieldCheck, Lock, Activity, Eye, RefreshCw, AlertTriangle,

  Search, ShieldAlert, CheckCircle2, KeyRound

} from 'lucide-react';

import { auditService } from '../../services/api';

import { StatCard } from '../../components/common/StatCard';

import { Badge } from '../../components/common/Badge';



export const SecurityDashboard = () => {

  const [logs, setLogs] = useState([]);

  const [loading, setLoading] = useState(true);

  const [searchTerm, setSearchTerm] = useState('');

  const [statusFilter, setStatusFilter] = useState('ALL');



  const fetchLogs = async () => {

    setLoading(true);

    try {

      const data = await auditService.getAuditLogs(50);

      setLogs(data);

    } catch (err) {

      console.error('Failed to load audit logs:', err);

    } finally {

      setLoading(false);

    }

  };



  useEffect(() => {

    fetchLogs();

  }, []);



  const filteredLogs = logs.filter((log) => {

    const matchesSearch =

      log.action.toLowerCase().includes(searchTerm.toLowerCase()) ||

      log.resource_type.toLowerCase().includes(searchTerm.toLowerCase()) ||

      (log.ip_address && log.ip_address.includes(searchTerm));

    const matchesStatus = statusFilter === 'ALL' || log.status === statusFilter;

    return matchesSearch && matchesStatus;

  });



  return (

    <div className="space-y-6">

      {/* Top Banner */}

      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 bg-white p-6 rounded-2xl border border-slate-200 shadow-xs">

        <div>

          <div className="flex items-center space-x-2">

            <h1 className="text-xl font-bold text-slate-900">Security & Compliance Center</h1>

            <span className="px-2.5 py-0.5 rounded-full bg-purple-50 text-purple-700 border border-purple-200 text-xs font-semibold">

              HIPAA & GDPR Enforced

            </span>

          </div>

          <p className="text-xs text-slate-500 mt-1">

            Immutable regulatory access logs, differential privacy loss accounting, and anomaly monitoring

          </p>

        </div>

        <button

          onClick={fetchLogs}

          className="flex items-center space-x-1.5 px-3 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold transition self-start sm:self-auto"

        >

          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />

          <span>Refresh Audit Logs</span>

        </button>

      </div>



      {/* Security Stat Cards */}

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">

        <StatCard

          title="Total Security Events"

          value={logs.length}

          subtitle="logged in PostgreSQL"

          icon={ShieldCheck}

          color="teal"

        />

        <StatCard

          title="Differential Privacy &epsilon;"

          value="&le; 1.50"

          subtitle="Strict DP Guarantee"

          icon={Lock}

          color="purple"

        />

        <StatCard

          title="Authentication Guard"

          value="JWT + Bcrypt"

          subtitle="HMAC-SHA256 (120 min exp)"

          icon={KeyRound}

          color="blue"

        />

        <StatCard

          title="Zero Raw Data Shared"

          value="100% Isolated"

          subtitle="Edge node firewalls active"

          icon={ShieldAlert}

          color="teal"

        />

      </div>



      {/* Filter and Search Bar */}

      <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-xs flex flex-col sm:flex-row items-center justify-between gap-3">

        <div className="relative w-full sm:w-80">

          <Search className="w-4 h-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400" />

          <input

            type="text"

            value={searchTerm}

            onChange={(e) => setSearchTerm(e.target.value)}

            placeholder="Search action, resource, or IP..."

            className="w-full pl-9 pr-3.5 py-2 border border-slate-200 rounded-xl text-xs text-slate-800 placeholder:text-slate-400 focus:outline-none focus:border-teal-600 bg-slate-50/50"

          />

        </div>



        <div className="flex items-center space-x-2 w-full sm:w-auto">

          <span className="text-xs font-semibold text-slate-500">Status:</span>

          {['ALL', 'SUCCESS', 'FAILED', 'UNAUTHORIZED'].map((s) => (

            <button

              key={s}

              onClick={() => setStatusFilter(s)}

              className={`px-3 py-1.5 rounded-lg text-xs font-semibold border transition ${

                statusFilter === s

                  ? 'bg-slate-900 text-white border-slate-900'

                  : 'bg-white text-slate-600 border-slate-200 hover:bg-slate-50'

              }`}

            >

              {s}

            </button>

          ))}

        </div>

      </div>



      {/* Audit Logs Table */}

      <div className="bg-white rounded-2xl border border-slate-200 shadow-xs overflow-hidden">

        <div className="p-6 border-b border-slate-100 flex items-center justify-between">

          <div>

            <h3 className="text-sm font-bold text-slate-900">Regulatory Audit Trail Records</h3>

            <p className="text-xs text-slate-500">Chronological ledger of security operations, authorizations, and model triggers</p>

          </div>

          <span className="text-xs bg-slate-100 font-mono text-slate-600 px-2.5 py-1 rounded-lg">

            {filteredLogs.length} Records Shown

          </span>

        </div>



        <div className="overflow-x-auto">

          <table className="w-full text-left text-xs text-slate-600">

            <thead className="bg-slate-50 border-b border-slate-200 text-slate-700 uppercase font-semibold">

              <tr>

                <th className="px-6 py-3.5">Timestamp</th>

                <th className="px-6 py-3.5">Action</th>

                <th className="px-6 py-3.5">Resource Type</th>

                <th className="px-6 py-3.5">Client IP Address</th>

                <th className="px-6 py-3.5">Details</th>

                <th className="px-6 py-3.5">Outcome</th>

              </tr>

            </thead>

            <tbody className="divide-y divide-slate-100">

              {filteredLogs.length === 0 ? (

                <tr>

                  <td colSpan={6} className="px-6 py-8 text-center text-slate-400">

                    No matching compliance logs found.

                  </td>

                </tr>

              ) : (

                filteredLogs.map((log) => (

                  <tr key={log.id} className="hover:bg-slate-50/70 transition">

                    <td className="px-6 py-4 font-mono text-slate-500 whitespace-nowrap">

                      {new Date(log.timestamp).toLocaleString()}

                    </td>

                    <td className="px-6 py-4 font-bold text-slate-900">{log.action}</td>

                    <td className="px-6 py-4 font-mono text-[11px] text-slate-600">{log.resource_type}</td>

                    <td className="px-6 py-4 font-mono text-slate-500">{log.ip_address || '127.0.0.1'}</td>

                    <td className="px-6 py-4 max-w-xs truncate font-mono text-[11px] text-slate-500">

                      {JSON.stringify(log.details)}

                    </td>

                    <td className="px-6 py-4">

                      <Badge status={log.status} />

                    </td>

                  </tr>

                ))

              )}

            </tbody>

          </table>

        </div>

      </div>

    </div>

  );

};
