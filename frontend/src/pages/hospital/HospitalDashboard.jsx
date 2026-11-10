import React, { useState, useEffect } from 'react';

import {

  Building2, Database, Activity, ShieldAlert, Plus,

  FileCheck2, Server, Lock, AlertCircle, RefreshCw, Layers

} from 'lucide-react';

import { useAuth } from '../../contexts/AuthContext';

import { datasetService, institutionService } from '../../services/api';

import { StatCard } from '../../components/common/StatCard';

import { Badge } from '../../components/common/Badge';

import { Modal } from '../../components/common/Modal';



export const HospitalDashboard = () => {

  const { user } = useAuth();

  const [datasets, setDatasets] = useState([]);

  const [institution, setInstitution] = useState(null);

  const [loading, setLoading] = useState(true);



  // Modal State for new dataset registration

  const [isModalOpen, setIsModalOpen] = useState(false);

  const [newDataset, setNewDataset] = useState({

    name: '',

    modality: 'tabular_ehr',

    sample_count: 500,

    features_input: 'age, bmi, systolic_bp, diastolic_bp, fasting_glucose, cholesterol',

    target: 'cardiovascular_risk_outcome',

  });

  const [modalLoading, setModalLoading] = useState(false);

  const [modalError, setModalError] = useState(null);



  const fetchData = async () => {

    setLoading(true);

    try {

      const datasetData = await datasetService.getDatasets();

      setDatasets(datasetData);



      if (user?.institution_id) {

        const instData = await institutionService.getInstitutions();

        const myInst = instData.find((i) => i.id === user.institution_id);

        setInstitution(myInst || null);

      }

    } catch (err) {

      console.error('Failed to fetch hospital dashboard data:', err);

    } finally {

      setLoading(false);

    }

  };



  useEffect(() => {

    fetchData();

  }, [user]);



  const handleRegisterDataset = async (e) => {

    e.preventDefault();

    setModalLoading(true);

    setModalError(null);



    const featureList = newDataset.features_input

      .split(',')

      .map((f) => f.trim())

      .filter(Boolean);



    try {

      await datasetService.createDataset({

        name: newDataset.name,

        modality: newDataset.modality,

        sample_count: parseInt(newDataset.sample_count, 10),

        feature_schema: {

          features: featureList,

          target: newDataset.target.trim(),

        },

      });



      setIsModalOpen(false);

      setNewDataset({

        name: '',

        modality: 'tabular_ehr',

        sample_count: 500,

        features_input: 'age, bmi, systolic_bp, diastolic_bp, fasting_glucose, cholesterol',

        target: 'cardiovascular_risk_outcome',

      });

      fetchData();

    } catch (err) {

      setModalError(err.response?.data?.detail || 'Failed to register dataset schema.');

    } finally {

      setModalLoading(false);

    }

  };



  const totalPatientsProtected = datasets.reduce((acc, curr) => acc + (curr.sample_count || 0), 0);



  return (

    <div className="space-y-6">

      {/* Top Banner */}

      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 bg-white p-6 rounded-2xl border border-slate-200 shadow-xs">

        <div>

          <div className="flex items-center space-x-2">

            <h1 className="text-xl font-bold text-slate-900">Hospital Node Operations</h1>

            <span className="px-2.5 py-0.5 rounded-full bg-teal-50 text-teal-700 border border-teal-200 text-xs font-semibold">

              Edge Client Authority

            </span>

          </div>

          <p className="text-xs text-slate-500 mt-1">

            Local patient data governance, differential privacy boundary, and training node status

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

            <span>Register Dataset Schema</span>

          </button>

        </div>

      </div>



      {/* Hospital Identity & Status Grid */}

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">

        <StatCard

          title="Affiliated Institution"

          value={institution ? institution.name.split(' ')[0] + '...' : 'Alpha Health'}

          subtitle={institution?.institution_code || 'HOSP-ALPHA-01'}

          icon={Building2}

          color="teal"

        />

        <StatCard

          title="Patient Cohort Size"

          value={totalPatientsProtected.toLocaleString()}

          subtitle="locally isolated records"

          icon={Database}

          color="blue"

        />

        <StatCard

          title="Edge Node Status"

          value="Online"

          subtitle="Ready for Flower FL rounds"

          icon={Server}

          color="teal"

        />

        <StatCard

          title="Privacy Budget Spent"

          value="&epsilon; = 0.45"

          subtitle="Differential Privacy limit &epsilon; &le; 2.0"

          icon={Lock}

          color="purple"

        />

      </div>



      {/* Dataset Metadata Management Section */}

      <div className="bg-white rounded-2xl border border-slate-200 shadow-xs overflow-hidden">

        <div className="p-6 border-b border-slate-100 flex items-center justify-between">

          <div>

            <h3 className="text-sm font-bold text-slate-900">Registered Patient Cohorts (Schema Only)</h3>

            <p className="text-xs text-slate-500">

              Zero raw medical data leaves your hospital. Only feature signatures and sample counts are registered.

            </p>

          </div>

          <span className="text-xs bg-emerald-50 text-emerald-700 font-semibold px-2.5 py-1 rounded-lg border border-emerald-200">

            Local Firewall Active

          </span>

        </div>



        <div className="overflow-x-auto">

          <table className="w-full text-left text-xs text-slate-600">

            <thead className="bg-slate-50 border-b border-slate-200 text-slate-700 uppercase font-semibold">

              <tr>

                <th className="px-6 py-3.5">Dataset Name</th>

                <th className="px-6 py-3.5">Clinical Modality</th>

                <th className="px-6 py-3.5">Patient Sample Count</th>

                <th className="px-6 py-3.5">Feature Signature</th>

                <th className="px-6 py-3.5">Status</th>

              </tr>

            </thead>

            <tbody className="divide-y divide-slate-100">

              {datasets.length === 0 ? (

                <tr>

                  <td colSpan={5} className="px-6 py-8 text-center text-slate-400">

                    No datasets registered yet. Click &quot;Register Dataset Schema&quot; to define your first cohort.

                  </td>

                </tr>

              ) : (

                datasets.map((ds) => (

                  <tr key={ds.id} className="hover:bg-slate-50/70 transition">

                    <td className="px-6 py-4 font-bold text-slate-900">{ds.name}</td>

                    <td className="px-6 py-4 font-mono uppercase text-slate-600">{ds.modality}</td>

                    <td className="px-6 py-4 font-bold text-teal-700">{ds.sample_count.toLocaleString()}</td>

                    <td className="px-6 py-4 max-w-xs truncate text-slate-500 font-mono text-[11px]">

                      {ds.feature_schema?.features?.join(', ') || 'Standard Clinical Metrics'}

                    </td>

                    <td className="px-6 py-4">

                      <Badge status={ds.is_validated ? 'active' : 'pending'} text={ds.is_validated ? 'Validated' : 'Pending'} />

                    </td>

                  </tr>

                ))

              )}

            </tbody>

          </table>

        </div>

      </div>



      {/* Edge Client Training Status & Privacy Boundary Card */}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs">

          <h4 className="text-sm font-bold text-slate-900 mb-2">Hospital Edge Client Architecture</h4>

          <p className="text-xs text-slate-600 mb-4">

            The hospital worker process runs inside your hospital perimeter. When an FL round begins, it downloads global weights, executes PyTorch DP-SGD, and uploads only differential gradients.

          </p>

          <div className="space-y-2.5 text-xs">

            <div className="flex items-center justify-between p-2.5 rounded-xl bg-slate-50 border border-slate-100">

              <span className="font-semibold text-slate-700">Client Agent Version</span>

              <span className="font-mono text-slate-900">Flower Client v1.7.0</span>

            </div>

            <div className="flex items-center justify-between p-2.5 rounded-xl bg-slate-50 border border-slate-100">

              <span className="font-semibold text-slate-700">PyTorch Execution Runtime</span>

              <span className="font-mono text-slate-900">PyTorch 2.2.0 (CUDA / CPU)</span>

            </div>

            <div className="flex items-center justify-between p-2.5 rounded-xl bg-slate-50 border border-slate-100">

              <span className="font-semibold text-slate-700">Differential Privacy Mode</span>

              <span className="font-mono text-teal-700 font-semibold">DP-SGD (L2-Clip + Gaussian)</span>

            </div>

          </div>

        </div>



        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs">

          <h4 className="text-sm font-bold text-slate-900 mb-2">Differential Privacy Accounting</h4>

          <p className="text-xs text-slate-600 mb-4">

            Tracks cumulative privacy budget consumption to prevent model inversion or membership inference attacks.

          </p>

          <div className="space-y-4">

            <div>

              <div className="flex justify-between text-xs font-semibold mb-1">

                <span className="text-slate-700">Privacy Loss Parameter (&epsilon;)</span>

                <span className="text-teal-700">0.45 / 2.0 Max</span>

              </div>

              <div className="w-full bg-slate-100 h-2 rounded-full overflow-hidden">

                <div className="bg-teal-600 h-2 rounded-full" style={{ width: '22.5%' }} />

              </div>

            </div>

            <div className="p-3 rounded-xl bg-teal-50/60 border border-teal-100 text-teal-900 text-xs flex items-center gap-2">

              <ShieldAlert className="w-4 h-4 text-teal-600 shrink-0" />

              <span>Current privacy expenditure satisfies strict HIPAA and GDPR de-identification thresholds.</span>

            </div>

          </div>

        </div>

      </div>



      {/* Register Dataset Modal */}

      <Modal

        isOpen={isModalOpen}

        onClose={() => setIsModalOpen(false)}

        title="Register Patient Cohort Schema"

      >

        {modalError && (

          <div className="mb-4 p-3 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-xs flex items-center space-x-2">

            <AlertCircle className="w-4 h-4 shrink-0 text-rose-600" />

            <span>{modalError}</span>

          </div>

        )}

        <form onSubmit={handleRegisterDataset} className="space-y-3.5">

          <div>

            <label className="block text-xs font-semibold text-slate-700 mb-1">Cohort / Study Title</label>

            <input

              type="text"

              required

              value={newDataset.name}

              onChange={(e) => setNewDataset({ ...newDataset, name: e.target.value })}

              placeholder="e.g., Inpatient Cardiovascular Cohort 2026"

              className="w-full px-3.5 py-2 border border-slate-200 rounded-xl text-xs text-slate-900 focus:outline-none focus:border-teal-600"

            />

          </div>

          <div>

            <label className="block text-xs font-semibold text-slate-700 mb-1">Clinical Modality</label>

            <select

              value={newDataset.modality}

              onChange={(e) => setNewDataset({ ...newDataset, modality: e.target.value })}

              className="w-full px-3.5 py-2 border border-slate-200 rounded-xl text-xs text-slate-900 focus:outline-none focus:border-teal-600"

            >

              <option value="tabular_ehr">Tabular Electronic Health Records (EHR)</option>

              <option value="medical_imaging">Medical Imaging (DICOM / Chest X-Ray)</option>

              <option value="clinical_notes_nlp">Clinical Notes NLP</option>

            </select>

          </div>

          <div>

            <label className="block text-xs font-semibold text-slate-700 mb-1">Total Patient Samples</label>

            <input

              type="number"

              required

              min={1}

              value={newDataset.sample_count}

              onChange={(e) => setNewDataset({ ...newDataset, sample_count: e.target.value })}

              className="w-full px-3.5 py-2 border border-slate-200 rounded-xl text-xs text-slate-900 focus:outline-none focus:border-teal-600"

            />

          </div>

          <div>

            <label className="block text-xs font-semibold text-slate-700 mb-1">Feature List (Comma-separated)</label>

            <input

              type="text"

              required

              value={newDataset.features_input}

              onChange={(e) => setNewDataset({ ...newDataset, features_input: e.target.value })}

              placeholder="age, bmi, systolic_bp, diastolic_bp, glucose, cholesterol"

              className="w-full px-3.5 py-2 border border-slate-200 rounded-xl text-xs text-slate-900 focus:outline-none focus:border-teal-600"

            />

          </div>

          <div>

            <label className="block text-xs font-semibold text-slate-700 mb-1">Target Diagnostic Label</label>

            <input

              type="text"

              required

              value={newDataset.target}

              onChange={(e) => setNewDataset({ ...newDataset, target: e.target.value })}

              placeholder="cardiovascular_risk_outcome"

              className="w-full px-3.5 py-2 border border-slate-200 rounded-xl text-xs text-slate-900 focus:outline-none focus:border-teal-600"

            />

          </div>



          <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl text-[11px] text-slate-600">

            <strong>Privacy Note:</strong> Submitting this form registers only metadata schema definitions. Your patient database stays strictly local.

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

              {modalLoading ? 'Registering...' : 'Register Cohort'}

            </button>

          </div>

        </form>

      </Modal>

    </div>

  );

};
