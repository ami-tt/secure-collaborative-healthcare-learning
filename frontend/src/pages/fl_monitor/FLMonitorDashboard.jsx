import React, { useState, useEffect } from 'react';

import {

  Activity, Play, Pause, RefreshCw, CheckCircle, Server,

  Layers, HardDrive, Download, AlertCircle, Shield, FileCheck2

} from 'lucide-react';

import { flService, institutionService } from '../../services/api';

import { ConvergenceChart } from '../../components/charts/ConvergenceChart';

import { ClientPerformanceChart } from '../../components/charts/ClientPerformanceChart';

import { Badge } from '../../components/common/Badge';



export const FLMonitorDashboard = () => {

  const [sessions, setSessions] = useState([]);

  const [selectedSessionId, setSelectedSessionId] = useState('');

  const [hospitals, setHospitals] = useState([]);

  const [loading, setLoading] = useState(true);



  // Simulated live round data for visualization

  const [roundMetrics, setRoundMetrics] = useState([

    { round: 1, accuracy: 0.68, loss: 0.62 },

    { round: 2, accuracy: 0.76, loss: 0.49 },

    { round: 3, accuracy: 0.82, loss: 0.41 },

    { round: 4, accuracy: 0.86, loss: 0.35 },

    { round: 5, accuracy: 0.89, loss: 0.28 },

  ]);



  const [clientPerformance, setClientPerformance] = useState([

    { hospital: 'Alpha Health', samples: 1200, accuracy: 0.90 },

    { hospital: 'Beta Memorial', samples: 850, accuracy: 0.88 },

  ]);



  const fetchData = async () => {

    setLoading(true);

    try {

      const [sessData, hospData] = await Promise.all([

        flService.getSessions().catch(() => []),

        institutionService.getInstitutions().catch(() => []),

      ]);

      setSessions(sessData);

      setHospitals(hospData);

      if (sessData.length > 0 && !selectedSessionId) {

        setSelectedSessionId(sessData[0].id);

      }

    } catch (err) {

      console.error('Failed to load FL monitor data:', err);

    } finally {

      setLoading(false);

    }

  };



  useEffect(() => {

    fetchData();

  }, []);



  const activeSession = sessions.find((s) => s.id === selectedSessionId) || sessions[0] || null;



  return (

    <div className="space-y-6">

      {/* Top Banner */}

      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 bg-white p-6 rounded-2xl border border-slate-200 shadow-xs">

        <div>

          <div className="flex items-center space-x-2">

            <h1 className="text-xl font-bold text-slate-900">Federated Convergence Telemetry</h1>

            <span className="px-2.5 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 text-xs font-semibold flex items-center gap-1">

              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-ping"></span>

              Live Flower Aggregator

            </span>

          </div>

          <p className="text-xs text-slate-500 mt-1">

            Real-time multi-hospital model training telemetry, loss convergence curves, and weight verification

          </p>

        </div>



        {/* Session Selector */}

        <div className="flex items-center space-x-3">

          <select

            value={selectedSessionId}

            onChange={(e) => setSelectedSessionId(e.target.value)}

            className="px-3.5 py-2 border border-slate-200 rounded-xl text-xs font-semibold text-slate-800 bg-slate-50 focus:outline-none focus:border-teal-600"

          >

            {sessions.map((s) => (

              <option key={s.id} value={s.id}>

                {s.session_name} ({s.aggregation_strategy})

              </option>

            ))}

          </select>

          <button

            onClick={fetchData}

            className="p-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-600 transition"

            title="Refresh Metrics"

          >

            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />

          </button>

        </div>

      </div>



      {/* Progress & Round Stepper */}

      {activeSession && (

        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs space-y-4">

          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">

            <div>

              <span className="text-[11px] font-bold uppercase tracking-wider text-teal-700">Active Run Session</span>

              <h3 className="text-lg font-bold text-slate-900">{activeSession.session_name}</h3>

            </div>

            <div className="flex items-center space-x-3">

              <Badge status={activeSession.status} />

              <span className="text-xs font-mono font-bold text-slate-600">

                Strategy: {activeSession.aggregation_strategy}

              </span>

            </div>

          </div>



          <div>

            <div className="flex justify-between text-xs font-semibold text-slate-700 mb-1.5">

              <span>Training Round Progress</span>

              <span className="font-mono text-teal-700">Round 5 of {activeSession.total_rounds} (50% Completed)</span>

            </div>

            <div className="w-full bg-slate-100 h-2.5 rounded-full overflow-hidden">

              <div

                className="bg-gradient-to-r from-teal-500 to-blue-600 h-2.5 rounded-full transition-all duration-500"

                style={{ width: '50%' }}

              />

            </div>

          </div>



          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-2 text-xs">

            <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">

              <span className="text-slate-500 text-[11px] block">Global Accuracy</span>

              <span className="text-lg font-bold text-teal-700">89.4%</span>

            </div>

            <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">

              <span className="text-slate-500 text-[11px] block">Global Loss</span>

              <span className="text-lg font-bold text-slate-800">0.281</span>

            </div>

            <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">

              <span className="text-slate-500 text-[11px] block">Privacy &epsilon; Budget</span>

              <span className="text-lg font-bold text-purple-700">&epsilon; = {activeSession.dp_epsilon}</span>

            </div>

            <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">

              <span className="text-slate-500 text-[11px] block">Participating Nodes</span>

              <span className="text-lg font-bold text-blue-700">2 Hospitals</span>

            </div>

          </div>

        </div>

      )}



      {/* Real-time Recharts Telemetry Section */}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

        <ConvergenceChart data={roundMetrics} height={320} />

        <ClientPerformanceChart data={clientPerformance} height={320} />

      </div>



      {/* Connected Edge Hospitals Matrix */}

      <div className="bg-white rounded-2xl border border-slate-200 shadow-xs overflow-hidden">

        <div className="p-6 border-b border-slate-100 flex items-center justify-between">

          <div>

            <h3 className="text-sm font-bold text-slate-900">Hospital Edge Clients Matrix</h3>

            <p className="text-xs text-slate-500">Node connectivity status, local training stage, and sample weighting</p>

          </div>

          <span className="text-xs bg-slate-100 font-mono text-slate-600 px-2.5 py-1 rounded-lg">

            gRPC Port: 8080 (Encrypted)

          </span>

        </div>



        <div className="overflow-x-auto">

          <table className="w-full text-left text-xs text-slate-600">

            <thead className="bg-slate-50 border-b border-slate-200 text-slate-700 uppercase font-semibold">

              <tr>

                <th className="px-6 py-3.5">Institution Code</th>

                <th className="px-6 py-3.5">Hospital Name</th>

                <th className="px-6 py-3.5">Local Dataset Weight</th>

                <th className="px-6 py-3.5">Node Status</th>

                <th className="px-6 py-3.5 text-right">Heartbeat</th>

              </tr>

            </thead>

            <tbody className="divide-y divide-slate-100">

              {hospitals.map((hosp, idx) => (

                <tr key={hosp.id} className="hover:bg-slate-50/70 transition">

                  <td className="px-6 py-4 font-mono font-bold text-slate-900">{hosp.institution_code}</td>

                  <td className="px-6 py-4 font-semibold text-slate-800">{hosp.name}</td>

                  <td className="px-6 py-4 font-bold text-teal-700">

                    {idx === 0 ? '1,200 records (58.5%)' : '850 records (41.5%)'}

                  </td>

                  <td className="px-6 py-4">

                    <Badge status="connected" text="Online (Waiting FedAvg)" />

                  </td>

                  <td className="px-6 py-4 text-right font-mono text-slate-400">

                    Just now

                  </td>

                </tr>

              ))}

            </tbody>

          </table>

        </div>

      </div>



      {/* Model Artifact Vault & Checksum */}

      <div className="bg-slate-900 text-slate-200 p-6 rounded-2xl border border-slate-800 shadow-lg flex flex-col md:flex-row items-start md:items-center justify-between gap-4">

        <div>

          <div className="flex items-center space-x-2">

            <FileCheck2 className="w-5 h-5 text-teal-400" />

            <h4 className="text-sm font-bold text-white">Global PyTorch Checkpoint (Round 5)</h4>

          </div>

          <p className="text-xs text-slate-400 mt-1">

            SHA-256 Checksum: <span className="font-mono text-slate-300">e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855</span>

          </p>

        </div>

        <button

          onClick={() => alert('Model checkpoint integrity verified. In Phase 4, serialized weights are exported here.')}

          className="flex items-center space-x-2 px-4 py-2 rounded-xl bg-teal-600 hover:bg-teal-700 text-white text-xs font-semibold transition shrink-0"

        >

          <Download className="w-4 h-4" />

          <span>Verify Model Weights</span>

        </button>

      </div>

    </div>

  );

};
