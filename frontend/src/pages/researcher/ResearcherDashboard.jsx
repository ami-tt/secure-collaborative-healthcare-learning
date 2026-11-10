import React, { useState, useEffect } from 'react';

import {

  FolderPlus, Play, Activity, Sliders, Layers, RefreshCw,

  Plus, CheckCircle, Clock, Eye, AlertCircle, FileCode2, ChevronRight

} from 'lucide-react';

import { flService } from '../../services/api';

import { StatCard } from '../../components/common/StatCard';

import { Badge } from '../../components/common/Badge';

import { Modal } from '../../components/common/Modal';



export const ResearcherDashboard = ({ onOpenMonitor }) => {

  const [projects, setProjects] = useState([]);

  const [sessions, setSessions] = useState([]);

  const [loading, setLoading] = useState(true);



  // Modal 1: Create Project

  const [isProjectModalOpen, setIsProjectModalOpen] = useState(false);

  const [newProject, setNewProject] = useState({

    title: '',

    description: '',

    target_condition: '',

    model_architecture: 'TabularMLP',

    modality: 'tabular_ehr',

  });



  // Modal 2: Create Session

  const [isSessionModalOpen, setIsSessionModalOpen] = useState(false);

  const [newSession, setNewSession] = useState({

    project_id: '',

    session_name: '',

    total_rounds: 10,

    min_participating_clients: 2,

    aggregation_strategy: 'FedAvg',

    dp_enabled: true,

    dp_epsilon: 1.5,

    dp_delta: 0.00001,

    dp_max_grad_norm: 1.0,

    learning_rate: 0.001,

    local_epochs: 3,

    batch_size: 32,

  });



  const [modalLoading, setModalLoading] = useState(false);

  const [modalError, setModalError] = useState(null);



  const fetchData = async () => {

    setLoading(true);

    try {

      const [projData, sessData] = await Promise.all([

        flService.getProjects().catch(() => []),

        flService.getSessions().catch(() => []),

      ]);

      setProjects(projData);

      setSessions(sessData);

      if (projData.length > 0 && !newSession.project_id) {

        setNewSession((prev) => ({ ...prev, project_id: projData[0].id }));

      }

    } catch (err) {

      console.error('Failed to load researcher data:', err);

    } finally {

      setLoading(false);

    }

  };



  useEffect(() => {

    fetchData();

  }, []);



  const handleCreateProject = async (e) => {

    e.preventDefault();

    setModalLoading(true);

    setModalError(null);

    try {

      await flService.createProject(newProject);

      setIsProjectModalOpen(false);

      setNewProject({

        title: '',

        description: '',

        target_condition: '',

        model_architecture: 'TabularMLP',

        modality: 'tabular_ehr',

      });

      fetchData();

    } catch (err) {

      setModalError(err.response?.data?.detail || 'Failed to create research study.');

    } finally {

      setModalLoading(false);

    }

  };



  const handleCreateSession = async (e) => {

    e.preventDefault();

    setModalLoading(true);

    setModalError(null);

    try {

      await flService.createSession({

        ...newSession,

        total_rounds: parseInt(newSession.total_rounds, 10),

        min_participating_clients: parseInt(newSession.min_participating_clients, 10),

        local_epochs: parseInt(newSession.local_epochs, 10),

        batch_size: parseInt(newSession.batch_size, 10),

        dp_epsilon: parseFloat(newSession.dp_epsilon),

        dp_delta: parseFloat(newSession.dp_delta),

        dp_max_grad_norm: parseFloat(newSession.dp_max_grad_norm),

        learning_rate: parseFloat(newSession.learning_rate),

      });

      setIsSessionModalOpen(false);

      fetchData();

    } catch (err) {

      setModalError(err.response?.data?.detail || 'Failed to create training run.');

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

            <h1 className="text-xl font-bold text-slate-900">Clinical Research Studio</h1>

            <span className="px-2.5 py-0.5 rounded-full bg-blue-50 text-blue-700 border border-blue-200 text-xs font-semibold">

              Researcher Authority

            </span>

          </div>

          <p className="text-xs text-slate-500 mt-1">

            Configure multi-institutional federated studies, set privacy budgets, and launch training runs

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

            onClick={() => setIsProjectModalOpen(true)}

            className="flex items-center space-x-1.5 px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-900 text-white text-xs font-semibold shadow-xs transition"

          >

            <FolderPlus className="w-3.5 h-3.5" />

            <span>New Study</span>

          </button>

          <button

            onClick={() => setIsSessionModalOpen(true)}

            className="flex items-center space-x-1.5 px-4 py-2 rounded-xl bg-teal-600 hover:bg-teal-700 text-white text-xs font-semibold shadow-xs transition"

          >

            <Plus className="w-3.5 h-3.5" />

            <span>Launch FL Run</span>

          </button>

        </div>

      </div>



      {/* Stats Grid */}

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">

        <StatCard

          title="Active Research Studies"

          value={projects.length}

          subtitle="clinical target conditions"

          icon={FolderPlus}

          color="teal"

        />

        <StatCard

          title="Federated Sessions"

          value={sessions.length}

          subtitle="configured FL runs"

          icon={Activity}

          color="blue"

        />

        <StatCard

          title="PyTorch Neural Models"

          value="TabularMLP"

          subtitle="Clinical Risk Classifier"

          icon={FileCode2}

          color="purple"

        />

        <StatCard

          title="Privacy Guard"

          value="(&epsilon;, &delta;)-DP"

          subtitle="Gaussian gradient clipping"

          icon={Sliders}

          color="amber"

        />

      </div>



      {/* Projects & Study List */}

      <div className="bg-white rounded-2xl border border-slate-200 shadow-xs overflow-hidden">

        <div className="p-6 border-b border-slate-100 flex items-center justify-between">

          <div>

            <h3 className="text-sm font-bold text-slate-900">Collaborative Clinical Research Initiatives</h3>

            <p className="text-xs text-slate-500">Multicenter clinical target conditions and neural model architectures</p>

          </div>

          <button

            onClick={() => setIsProjectModalOpen(true)}

            className="text-xs font-bold text-teal-700 hover:text-teal-800 flex items-center gap-1"

          >

            <Plus className="w-3.5 h-3.5" /> Add Project

          </button>

        </div>



        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 p-6 bg-slate-50/50">

          {projects.length === 0 ? (

            <div className="col-span-2 text-center py-8 text-slate-400 text-xs">

              No research studies created yet. Click &quot;New Study&quot; to begin.

            </div>

          ) : (

            projects.map((proj) => (

              <div key={proj.id} className="bg-white p-5 rounded-xl border border-slate-200/80 shadow-xs hover:shadow-md transition">

                <div className="flex items-center justify-between">

                  <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-blue-50 text-blue-700 border border-blue-200 font-mono">

                    {proj.model_architecture}

                  </span>

                  <span className="text-xs text-slate-400">Target: <strong className="text-slate-700">{proj.target_condition}</strong></span>

                </div>

                <h4 className="text-sm font-bold text-slate-900 mt-2">{proj.title}</h4>

                <p className="text-xs text-slate-600 mt-1 line-clamp-2">{proj.description || 'Collaborative federated machine learning study across hospital partner datasets.'}</p>

                <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between">

                  <span className="text-[11px] text-slate-500 font-mono">Modality: {proj.modality}</span>

                  <button

                    onClick={() => {

                      setNewSession((prev) => ({ ...prev, project_id: proj.id }));

                      setIsSessionModalOpen(true);

                    }}

                    className="text-xs font-semibold text-teal-700 hover:text-teal-800 flex items-center gap-1"

                  >

                    <span>Configure FL Run</span>

                    <ChevronRight className="w-3.5 h-3.5" />

                  </button>

                </div>

              </div>

            ))

          )}

        </div>

      </div>



      {/* Configured FL Training Sessions Table */}

      <div className="bg-white rounded-2xl border border-slate-200 shadow-xs overflow-hidden">

        <div className="p-6 border-b border-slate-100 flex items-center justify-between">

          <div>

            <h3 className="text-sm font-bold text-slate-900">Federated Training Runs & Convergence States</h3>

            <p className="text-xs text-slate-500">Monitor round execution, privacy budgets, and convergence telemetry</p>

          </div>

          {onOpenMonitor && (

            <button

              onClick={onOpenMonitor}

              className="text-xs font-bold bg-teal-50 text-teal-700 px-3 py-1.5 rounded-lg border border-teal-200 hover:bg-teal-100 flex items-center gap-1.5 transition"

            >

              <Activity className="w-3.5 h-3.5" />

              <span>Open Live Telemetry Room</span>

            </button>

          )}

        </div>



        <div className="overflow-x-auto">

          <table className="w-full text-left text-xs text-slate-600">

            <thead className="bg-slate-50 border-b border-slate-200 text-slate-700 uppercase font-semibold">

              <tr>

                <th className="px-6 py-3.5">Run Name</th>

                <th className="px-6 py-3.5">Rounds</th>

                <th className="px-6 py-3.5">Strategy</th>

                <th className="px-6 py-3.5">Privacy &epsilon;</th>

                <th className="px-6 py-3.5">Status</th>

                <th className="px-6 py-3.5 text-right">Actions</th>

              </tr>

            </thead>

            <tbody className="divide-y divide-slate-100">

              {sessions.length === 0 ? (

                <tr>

                  <td colSpan={6} className="px-6 py-8 text-center text-slate-400">

                    No federated training sessions configured yet. Click &quot;Launch FL Run&quot; to configure parameters.

                  </td>

                </tr>

              ) : (

                sessions.map((sess) => (

                  <tr key={sess.id} className="hover:bg-slate-50/70 transition">

                    <td className="px-6 py-4 font-bold text-slate-900">{sess.session_name}</td>

                    <td className="px-6 py-4 font-mono">{sess.current_round} / {sess.total_rounds}</td>

                    <td className="px-6 py-4 font-mono">{sess.aggregation_strategy}</td>

                    <td className="px-6 py-4 font-bold text-purple-700">&epsilon; = {sess.dp_epsilon}</td>

                    <td className="px-6 py-4">

                      <Badge status={sess.status} />

                    </td>

                    <td className="px-6 py-4 text-right">

                      <button

                        onClick={onOpenMonitor}

                        className="px-2.5 py-1 rounded-lg bg-teal-50 hover:bg-teal-100 text-teal-700 border border-teal-200 text-xs font-semibold inline-flex items-center gap-1 transition"

                      >

                        <Eye className="w-3 h-3" />

                        <span>Monitor</span>

                      </button>

                    </td>

                  </tr>

                ))

              )}

            </tbody>

          </table>

        </div>

      </div>



      {/* Modal 1: New Study */}

      <Modal

        isOpen={isProjectModalOpen}

        onClose={() => setIsProjectModalOpen(false)}

        title="Create Collaborative Clinical Research Project"

      >

        {modalError && (

          <div className="mb-4 p-3 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-xs flex items-center space-x-2">

            <AlertCircle className="w-4 h-4 shrink-0 text-rose-600" />

            <span>{modalError}</span>

          </div>

        )}

        <form onSubmit={handleCreateProject} className="space-y-3.5">

          <div>

            <label className="block text-xs font-semibold text-slate-700 mb-1">Study / Project Title</label>

            <input

              type="text"

              required

              value={newProject.title}

              onChange={(e) => setNewProject({ ...newProject, title: e.target.value })}

              placeholder="e.g., Federated Diabetic Retinopathy Risk Stratification"

              className="w-full px-3.5 py-2 border border-slate-200 rounded-xl text-xs text-slate-900 focus:outline-none focus:border-teal-600"

            />

          </div>

          <div>

            <label className="block text-xs font-semibold text-slate-700 mb-1">Target Clinical Condition</label>

            <input

              type="text"

              required

              value={newProject.target_condition}

              onChange={(e) => setNewProject({ ...newProject, target_condition: e.target.value })}

              placeholder="Cardiovascular Event / Sepsis Risk"

              className="w-full px-3.5 py-2 border border-slate-200 rounded-xl text-xs text-slate-900 focus:outline-none focus:border-teal-600"

            />

          </div>

          <div>

            <label className="block text-xs font-semibold text-slate-700 mb-1">Deep Learning Architecture</label>

            <select

              value={newProject.model_architecture}

              onChange={(e) => setNewProject({ ...newProject, model_architecture: e.target.value })}

              className="w-full px-3.5 py-2 border border-slate-200 rounded-xl text-xs text-slate-900 focus:outline-none focus:border-teal-600"

            >

              <option value="TabularMLP">Tabular MLP (Clinical Risk Prediction on EHR)</option>

              <option value="ClinicalCNN">Convolutional Neural Network (Chest X-Ray / Medical Imaging)</option>

            </select>

          </div>

          <div>

            <label className="block text-xs font-semibold text-slate-700 mb-1">Clinical Hypothesis / Description</label>

            <textarea

              rows={3}

              value={newProject.description}

              onChange={(e) => setNewProject({ ...newProject, description: e.target.value })}

              placeholder="Collaborative study objective, cohort inclusion criteria..."

              className="w-full px-3.5 py-2 border border-slate-200 rounded-xl text-xs text-slate-900 focus:outline-none focus:border-teal-600"

            />

          </div>

          <div className="pt-3 flex justify-end space-x-2">

            <button

              type="button"

              onClick={() => setIsProjectModalOpen(false)}

              className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-600 hover:bg-slate-100"

            >

              Cancel

            </button>

            <button

              type="submit"

              disabled={modalLoading}

              className="px-4 py-2 rounded-xl text-xs font-semibold bg-teal-600 hover:bg-teal-700 text-white shadow-xs"

            >

              {modalLoading ? 'Creating Study...' : 'Create Study'}

            </button>

          </div>

        </form>

      </Modal>



      {/* Modal 2: Configure Session */}

      <Modal

        isOpen={isSessionModalOpen}

        onClose={() => setIsSessionModalOpen(false)}

        title="Configure Federated Learning Training Run"

        maxWidth="max-w-xl"

      >

        {modalError && (

          <div className="mb-4 p-3 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-xs flex items-center space-x-2">

            <AlertCircle className="w-4 h-4 shrink-0 text-rose-600" />

            <span>{modalError}</span>

          </div>

        )}

        <form onSubmit={handleCreateSession} className="space-y-4">

          <div className="grid grid-cols-2 gap-3">

            <div>

              <label className="block text-xs font-semibold text-slate-700 mb-1">Parent Project</label>

              <select

                value={newSession.project_id}

                onChange={(e) => setNewSession({ ...newSession, project_id: e.target.value })}

                className="w-full px-3 py-2 border border-slate-200 rounded-xl text-xs text-slate-900 focus:outline-none focus:border-teal-600"

              >

                {projects.map((p) => (

                  <option key={p.id} value={p.id}>{p.title}</option>

                ))}

              </select>

            </div>

            <div>

              <label className="block text-xs font-semibold text-slate-700 mb-1">Session Identifier</label>

              <input

                type="text"

                required

                value={newSession.session_name}

                onChange={(e) => setNewSession({ ...newSession, session_name: e.target.value })}

                placeholder="Exp-01-FedAvg-DP"

                className="w-full px-3 py-2 border border-slate-200 rounded-xl text-xs text-slate-900 focus:outline-none focus:border-teal-600"

              >

              </input>

            </div>

          </div>



          <div className="grid grid-cols-3 gap-3">

            <div>

              <label className="block text-xs font-semibold text-slate-700 mb-1">Total Rounds (T)</label>

              <input

                type="number"

                min={1}

                max={50}

                required

                value={newSession.total_rounds}

                onChange={(e) => setNewSession({ ...newSession, total_rounds: e.target.value })}

                className="w-full px-3 py-2 border border-slate-200 rounded-xl text-xs text-slate-900"

              />

            </div>

            <div>

              <label className="block text-xs font-semibold text-slate-700 mb-1">Min Hospitals</label>

              <input

                type="number"

                min={1}

                required

                value={newSession.min_participating_clients}

                onChange={(e) => setNewSession({ ...newSession, min_participating_clients: e.target.value })}

                className="w-full px-3 py-2 border border-slate-200 rounded-xl text-xs text-slate-900"

              />

            </div>

            <div>

              <label className="block text-xs font-semibold text-slate-700 mb-1">Strategy</label>

              <select

                value={newSession.aggregation_strategy}

                onChange={(e) => setNewSession({ ...newSession, aggregation_strategy: e.target.value })}

                className="w-full px-3 py-2 border border-slate-200 rounded-xl text-xs text-slate-900"

              >

                <option value="FedAvg">FedAvg (Weighted)</option>

                <option value="FedProx">FedProx (Proximal)</option>

              </select>

            </div>

          </div>



          <div className="p-3.5 bg-slate-50 border border-slate-200 rounded-xl space-y-2">

            <h5 className="text-xs font-bold text-slate-800 flex items-center gap-1.5">

              <Sliders className="w-3.5 h-3.5 text-teal-600" />

              <span>Differential Privacy & Hyperparameters</span>

            </h5>

            <div className="grid grid-cols-3 gap-3 text-xs">

              <div>

                <label className="block text-[11px] text-slate-600 mb-0.5">Privacy Epsilon (&epsilon;)</label>

                <input

                  type="number"

                  step="0.1"

                  min="0.1"

                  required

                  value={newSession.dp_epsilon}

                  onChange={(e) => setNewSession({ ...newSession, dp_epsilon: e.target.value })}

                  className="w-full px-2.5 py-1.5 border border-slate-200 rounded-lg text-xs"

                />

              </div>

              <div>

                <label className="block text-[11px] text-slate-600 mb-0.5">L2 Clip Norm (C)</label>

                <input

                  type="number"

                  step="0.1"

                  min="0.1"

                  required

                  value={newSession.dp_max_grad_norm}

                  onChange={(e) => setNewSession({ ...newSession, dp_max_grad_norm: e.target.value })}

                  className="w-full px-2.5 py-1.5 border border-slate-200 rounded-lg text-xs"

                />

              </div>

              <div>

                <label className="block text-[11px] text-slate-600 mb-0.5">Learning Rate</label>

                <input

                  type="number"

                  step="0.0001"

                  min="0.0001"

                  required

                  value={newSession.learning_rate}

                  onChange={(e) => setNewSession({ ...newSession, learning_rate: e.target.value })}

                  className="w-full px-2.5 py-1.5 border border-slate-200 rounded-lg text-xs"

                />

              </div>

            </div>

          </div>



          <div className="pt-2 flex justify-end space-x-2">

            <button

              type="button"

              onClick={() => setIsSessionModalOpen(false)}

              className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-600 hover:bg-slate-100"

            >

              Cancel

            </button>

            <button

              type="submit"

              disabled={modalLoading}

              className="px-4 py-2 rounded-xl text-xs font-semibold bg-teal-600 hover:bg-teal-700 text-white shadow-xs"

            >

              {modalLoading ? 'Configuring...' : 'Initialize FL Session'}

            </button>

          </div>

        </form>

      </Modal>

    </div>

  );

};
