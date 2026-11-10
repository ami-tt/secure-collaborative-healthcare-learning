import React from 'react';

import {

  LineChart,

  Line,

  XAxis,

  YAxis,

  CartesianGrid,

  Tooltip,

  Legend,

  ResponsiveContainer

} from 'recharts';



export const ConvergenceChart = ({ data = [], height = 300 }) => {

  if (!data || data.length === 0) {

    return (

      <div

        style={{ height }}

        className="w-full flex flex-col items-center justify-center bg-slate-50 border border-dashed border-slate-200 rounded-xl p-6 text-center"

      >

        <div className="w-10 h-10 rounded-full bg-slate-100 flex items-center justify-center text-slate-400 mb-2">

          📈

        </div>

        <p className="text-sm font-semibold text-slate-700">No round convergence data yet</p>

        <p className="text-xs text-slate-500 mt-1">Metrics will stream in real-time as Federated Averaging rounds execute.</p>

      </div>

    );

  }



  return (

    <div className="w-full bg-white p-4 rounded-xl border border-slate-200/80 shadow-xs">

      <div className="flex items-center justify-between mb-4">

        <div>

          <h4 className="text-sm font-bold text-slate-900">Federated Model Convergence Curve</h4>

          <p className="text-xs text-slate-500">Global FedAvg Accuracy & Loss per training round</p>

        </div>

        <span className="text-xs bg-teal-50 text-teal-700 font-semibold px-2 py-0.5 rounded border border-teal-200">

          Live Telemetry

        </span>

      </div>



      <div style={{ width: '100%', height }}>

        <ResponsiveContainer>

          <LineChart data={data} margin={{ top: 10, right: 20, left: -10, bottom: 0 }}>

            <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />

            <XAxis

              dataKey="round"

              stroke="#94a3b8"

              tick={{ fontSize: 12 }}

              label={{ value: 'Round', position: 'insideBottomRight', offset: -5, fontSize: 11, fill: '#64748b' }}

            />

            <YAxis

              yAxisId="left"

              stroke="#0d9488"

              tick={{ fontSize: 12 }}

              domain={[0, 1]}

              label={{ value: 'Accuracy', angle: -90, position: 'insideLeft', fontSize: 11, fill: '#0d9488' }}

            />

            <YAxis

              yAxisId="right"

              orientation="right"

              stroke="#64748b"

              tick={{ fontSize: 12 }}

              domain={[0, 'auto']}

              label={{ value: 'Loss', angle: 90, position: 'insideRight', fontSize: 11, fill: '#64748b' }}

            />

            <Tooltip

              contentStyle={{

                backgroundColor: '#ffffff',

                borderColor: '#e2e8f0',

                borderRadius: '0.75rem',

                boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)',

                fontSize: '12px'

              }}

            />

            <Legend wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }} />

            <Line

              yAxisId="left"

              type="monotone"

              dataKey="accuracy"

              name="Global Accuracy"

              stroke="#0d9488"

              strokeWidth={2.5}

              dot={{ r: 4, strokeWidth: 2, fill: '#ffffff' }}

              activeDot={{ r: 6 }}

            />

            <Line

              yAxisId="right"

              type="monotone"

              dataKey="loss"

              name="Global Loss"

              stroke="#64748b"

              strokeWidth={2}

              strokeDasharray="4 4"

              dot={{ r: 3 }}

            />

          </LineChart>

        </ResponsiveContainer>

      </div>

    </div>

  );

};
