import React, { useState, useEffect } from 'react';

import {

  Building2, Users, Activity, ShieldCheck, Plus, CheckCircle,

  XCircle, Search, RefreshCw, AlertCircle, FileText

} from 'lucide-react';

import { institutionService, userService, auditService, flService } from '../../services/api';

import { StatCard } from '../../components/common/StatCard';

import { Badge } from '../../components/common/Badge';

import { Modal } from '../../components/common/Modal';



export const AdminDashboard = () => {

  const [hospitals, setHospitals] = useState([]);

  const [users, setUsers] = useState([]);

  const [auditLogs, setAuditLogs] = useState([]);

  const [flSessions, setFlSessions] = useState([]);

  const [loading, setLoading] = useState(true);

  const [activeTab, setActiveTab] = useState('hospitals');



  // Modal State for new institution

  const [isModalOpen, setIsModalOpen] = useState(false);

  const [newHospital, setNewHospital] = useState({

    name: '',

    institution_code: '',

    contact_email: '',

    phone: '',

    address: '',

  });

  const [modalError, setModalError] = useState(null);

  const [modalLoading, setModalLoading] = useState(false);



  const fetchData = async () => {

    setLoading(true);

    try {

      const [hospData, userData, auditData, sessionData] = await Promise.all([

        institutionService.getInstitutions().catch(() => []),

        userService.getUsers().catch(() => []),

        auditService.getAuditLogs(20).catch(() => []),

        flService.getSessions().catch(() => []),

      ]);

      setHospitals(hospData);

      setUsers(userData);

      setAuditLogs(auditData);

      setFlSessions(sessionData);

    } catch (err) {

      console.error('Error fetching admin data:', err);

    } finally {

      setLoading(false);

    }

  };



  useEffect(() => {

    fetchData();

  }, []);



  const handleUpdateStatus = async (id, newStatus) => {

    try {

      await institutionService.updateStatus(id, newStatus);

      fetchData();

    } catch (err) {

      alert(err.response?.data?.detail || 'Failed to update institution status.');

    }

  };



  const handleCreateHospital = async (e) => {

    e.preventDefault();

    setModalLoading(true);

    setModalError(null);

    try {

      await institutionService.createInstitution(newHospital);

      setIsModalOpen(false);

      setNewHospital({ name: '', institution_code: '', contact_email: '', phone: '', address: '' });

      fetchData();

    } catch (err) {

      setModalError(err.response?.data?.detail || 'Failed to create hospital.');

    } finally {

      setModalLoading(false);

    }

  };



  return (

    <div className="space-y-6">

      {/* Top Banner */}

      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 bg-white p-6 rounded-2xl border border-slate-200 shadow-xs">

        <div>

          <div className="flex items-center space-x-2">

            <h1 className="text-xl font-bold text-slate-900">System Administration Portal</h1>

            <span className="px-2.5 py-0.5 rounded-full bg-purple-50 text-purple-700 border border-purple-200 text-xs font-semibold">

              Root Authority

            </span>

          </div>

          <p className="text-xs text-slate-500 mt-1">

            Global network oversight, healthcare institution onboarding, and regulatory compliance

          </p>

        </div>

        <div className="flex items-center space-x-3">

          <button

            onClick={fetchData}

            className="flex items-center space-x-1.5 px-3 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold transition"

          >

            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />

            <span>Refresh</span>

          </button>

          <button

            onClick={() => setIsModalOpen(true)}

            className="flex items-center space-x-1.5 px-4 py-2 rounded-xl bg-teal-600 hover:bg-teal-700 text-white text-xs font-semibold shadow-sm transition"

          >

            <Plus className="w-3.5 h-3.5" />

            <span>Onboard Hospital</span>

          </button>

        </div>

      </div>



      {/* Metric Cards Grid */}

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">

        <StatCard

          title="Registered Hospitals"

          value={hospitals.length}

          subtitle="clinical network partners"

          icon={Building2}

          color="teal"

        />

        <StatCard

          title="Platform Users"

          value={users.length}

          subtitle="authorized accounts"

          icon={Users}

          color="blue"

        />

        <StatCard

          title="FL Training Runs"

          value={flSessions.length}

          subtitle="collaborative studies"

          icon={Activity}

          color="purple"

        />

        <StatCard

          title="HIPAA Audit Logs"

          value={auditLogs.length}

          subtitle="immutable security events"

          icon={ShieldCheck}

          color="amber"

        />

      </div>



      {/* Main Tab Navigation */}

      <div className="bg-white rounded-2xl border border-slate-200 shadow-xs overflow-hidden">

        <div className="flex border-b border-slate-200 px-6 pt-4 bg-slate-50/50">

          <button

            onClick={() => setActiveTab('hospitals')}

            className={`pb-3 px-4 text-xs font-bold border-b-2 transition flex items-center space-x-2 ${

              activeTab === 'hospitals'

                ? 'border-teal-600 text-teal-800'

                : 'border-transparent text-slate-500 hover:text-slate-700'

            }`}

          >

            <Building2 className="w-4 h-4" />

            <span>Hospital Partners ({hospitals.length})</span>

          </button>

          <button

            onClick={() => setActiveTab('users')}

            className={`pb-3 px-4 text-xs font-bold border-b-2 transition flex items-center space-x-2 ${

              activeTab === 'users'

                ? 'border-teal-600 text-teal-800'

                : 'border-transparent text-slate-500 hover:text-slate-700'

            }`}

          >

            <Users className="w-4 h-4" />

            <span>User Directory ({users.length})</span>

          </button>

          <button

            onClick={() => setActiveTab('audits')}

            className={`pb-3 px-4 text-xs font-bold border-b-2 transition flex items-center space-x-2 ${

              activeTab === 'audits'

                ? 'border-teal-600 text-teal-800'

                : 'border-transparent text-slate-500 hover:text-slate-700'

            }`}

          >

            <ShieldCheck className="w-4 h-4" />

            <span>Audit Trail ({auditLogs.length})</span>

          </button>

        </div>



        {/* Tab 1: Hospital Management */}

        {activeTab === 'hospitals' && (

          <div className="overflow-x-auto">

            <table className="w-full text-left text-xs text-slate-600">

              <thead className="bg-slate-50 border-b border-slate-200 text-slate-700 uppercase font-semibold">

                <tr>

                  <th className="px-6 py-3.5">Institution Code</th>

                  <th className="px-6 py-3.5">Name</th>

                  <th className="px-6 py-3.5">Contact Email</th>

                  <th className="px-6 py-3.5">Status</th>

                  <th className="px-6 py-3.5 text-right">Actions</th>

                </tr>

              </thead>

              <tbody className="divide-y divide-slate-100">

                {hospitals.length === 0 ? (

                  <tr>

                    <td colSpan={5} className="px-6 py-8 text-center text-slate-400">

                      No hospitals registered yet. Click &quot;Onboard Hospital&quot; to add one.

                    </td>

                  </tr>

                ) : (

                  hospitals.map((hosp) => (

                    <tr key={hosp.id} className="hover:bg-slate-50/70 transition">

                      <td className="px-6 py-4 font-mono font-bold text-slate-900">{hosp.institution_code}</td>

                      <td className="px-6 py-4 font-medium text-slate-900">{hosp.name}</td>

                      <td className="px-6 py-4">{hosp.contact_email}</td>

                      <td className="px-6 py-4">

                        <Badge status={hosp.status} />

                      </td>

                      <td className="px-6 py-4 text-right space-x-2">

                        {hosp.status !== 'active' ? (

                          <button

                            onClick={() => handleUpdateStatus(hosp.id, 'active')}

                            className="px-2.5 py-1 rounded-lg bg-emerald-50 hover:bg-emerald-100 text-emerald-700 border border-emerald-200 text-xs font-semibold transition"

                          >

                            Approve

                          </button>

                        ) : (

                          <button

                            onClick={() => handleUpdateStatus(hosp.id, 'suspended')}

                            className="px-2.5 py-1 rounded-lg bg-rose-50 hover:bg-rose-100 text-rose-700 border border-rose-200 text-xs font-semibold transition"

                          >

                            Suspend

                          </button>

                        )}

                      </td>

                    </tr>

                  ))

                )}

              </tbody>

            </table>

          </div>

        )}



        {/* Tab 2: User Directory */}

        {activeTab === 'users' && (

          <div className="overflow-x-auto">

            <table className="w-full text-left text-xs text-slate-600">

              <thead className="bg-slate-50 border-b border-slate-200 text-slate-700 uppercase font-semibold">

                <tr>

                  <th className="px-6 py-3.5">Name</th>

                  <th className="px-6 py-3.5">Email</th>

                  <th className="px-6 py-3.5">Role</th>

                  <th className="px-6 py-3.5">Account Status</th>

                  <th className="px-6 py-3.5">Verified</th>

                </tr>

              </thead>

              <tbody className="divide-y divide-slate-100">

                {users.map((u) => (

                  <tr key={u.id} className="hover:bg-slate-50/70 transition">

                    <td className="px-6 py-4 font-semibold text-slate-900">{u.full_name}</td>

                    <td className="px-6 py-4">{u.email}</td>

                    <td className="px-6 py-4">

                      <Badge status={u.role} />

                    </td>

                    <td className="px-6 py-4">

                      <span className={`px-2 py-0.5 rounded text-[11px] font-semibold ${

                        u.is_active ? 'bg-emerald-50 text-emerald-700' : 'bg-rose-50 text-rose-700'

                      }`}>

                        {u.is_active ? 'Active' : 'Disabled'}

                      </span>

                    </td>

                    <td className="px-6 py-4">

                      {u.is_verified ? (

                        <span className="text-emerald-600 font-semibold flex items-center gap-1">

                          <CheckCircle className="w-3.5 h-3.5" /> Verified

                        </span>

                      ) : (

                        <span className="text-slate-400">Pending</span>

                      )}

                    </td>

                  </tr>

                ))}

              </tbody>

            </table>

          </div>

        )}



        {/* Tab 3: Security & Audit Trail */}

        {activeTab === 'audits' && (

          <div className="overflow-x-auto">

            <table className="w-full text-left text-xs text-slate-600">

              <thead className="bg-slate-50 border-b border-slate-200 text-slate-700 uppercase font-semibold">

                <tr>

                  <th className="px-6 py-3.5">Timestamp</th>

                  <th className="px-6 py-3.5">Action</th>

                  <th className="px-6 py-3.5">Resource</th>

                  <th className="px-6 py-3.5">Client IP</th>

                  <th className="px-6 py-3.5">Status</th>

                </tr>

              </thead>

              <tbody className="divide-y divide-slate-100">

                {auditLogs.map((log) => (

                  <tr key={log.id} className="hover:bg-slate-50/70 transition">

                    <td className="px-6 py-4 font-mono text-slate-500">

                      {new Date(log.timestamp).toLocaleString()}

                    </td>

                    <td className="px-6 py-4 font-bold text-slate-900">{log.action}</td>

                    <td className="px-6 py-4 font-mono text-xs">{log.resource_type}</td>

                    <td className="px-6 py-4 font-mono text-slate-500">{log.ip_address || '127.0.0.1'}</td>

                    <td className="px-6 py-4">

                      <Badge status={log.status} />

                    </td>

                  </tr>

                ))}

              </tbody>

            </table>

          </div>

        )}

      </div>



      {/* Onboard Hospital Modal */}

      <Modal

        isOpen={isModalOpen}

        onClose={() => setIsModalOpen(false)}

        title="Onboard New Healthcare Institution"

      >

        {modalError && (

          <div className="mb-4 p-3 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-xs flex items-center space-x-2">

            <AlertCircle className="w-4 h-4 shrink-0 text-rose-600" />

            <span>{modalError}</span>

          </div>

        )}

        <form onSubmit={handleCreateHospital} className="space-y-3.5">

          <div>

            <label className="block text-xs font-semibold text-slate-700 mb-1">Hospital / Clinic Name</label>

            <input

              type="text"

              required

              value={newHospital.name}

              onChange={(e) => setNewHospital({ ...newHospital, name: e.target.value })}

              placeholder="Memorial Heart & Vascular Institute"

              className="w-full px-3.5 py-2 border border-slate-200 rounded-xl text-xs text-slate-900 focus:outline-none focus:border-teal-600"

            />

          </div>

          <div>

            <label className="block text-xs font-semibold text-slate-700 mb-1">Institution Code (Unique Identifier)</label>

            <input

              type="text"

              required

              value={newHospital.institution_code}

              onChange={(e) => setNewHospital({ ...newHospital, institution_code: e.target.value.toUpperCase() })}

              placeholder="HOSP-MEMORIAL-03"

              className="w-full px-3.5 py-2 border border-slate-200 rounded-xl text-xs text-slate-900 font-mono focus:outline-none focus:border-teal-600"

            />

          </div>

          <div>

            <label className="block text-xs font-semibold text-slate-700 mb-1">Official Contact Email</label>

            <input

              type="email"

              required

              value={newHospital.contact_email}

              onChange={(e) => setNewHospital({ ...newHospital, contact_email: e.target.value })}

              placeholder="clinical-ai@memorial.org"

              className="w-full px-3.5 py-2 border border-slate-200 rounded-xl text-xs text-slate-900 focus:outline-none focus:border-teal-600"

            />

          </div>

          <div>

            <label className="block text-xs font-semibold text-slate-700 mb-1">Address & Location</label>

            <input

              type="text"

              value={newHospital.address}

              onChange={(e) => setNewHospital({ ...newHospital, address: e.target.value })}

              placeholder="742 Medical Center Way, Building B"

              className="w-full px-3.5 py-2 border border-slate-200 rounded-xl text-xs text-slate-900 focus:outline-none focus:border-teal-600"

            />

          </div>

          <div className="pt-3 flex justify-end space-x-2">

            <button

              type="button"

              onClick={() => setIsModalOpen(false)}

              className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-600 hover:bg-slate-100"

            >

              Cancel

            </button>

            <button

              type="submit"

              disabled={modalLoading}

              className="px-4 py-2 rounded-xl text-xs font-semibold bg-teal-600 hover:bg-teal-700 text-white shadow-xs"

            >

              {modalLoading ? 'Registering...' : 'Register Institution'}

            </button>

          </div>

        </form>

      </Modal>

    </div>

  );

};
