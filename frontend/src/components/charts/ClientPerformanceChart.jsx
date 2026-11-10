import React from 'react';

import {

  BarChart,

  Bar,

  XAxis,

  YAxis,

  CartesianGrid,

  Tooltip,

  Legend,

  ResponsiveContainer

} from 'recharts';



export const ClientPerformanceChart = ({ data = [], height = 280 }) => {

  if (!data || data.length === 0) {

    return (

      <div

        style={{ height }}

        className="w-full flex flex-col items-center justify-center bg-slate-50 border border-dashed border-slate-200 rounded-xl p-6 text-center"

      >

        <p className="text-sm font-semibold text-slate-700">No client performance data recorded</p>

        <p className="text-xs text-slate-500 mt-1">Participating hospital client nodes will report metrics upon round completion.</p>

      </div>

    );

  }



  return (

    <div className="w-full bg-white p-4 rounded-xl border border-slate-200/80 shadow-xs">

      <div className="flex items-center justify-between mb-4">

        <div>

          <h4 className="text-sm font-bold text-slate-900">Hospital Node Performance Distribution</h4>

          <p className="text-xs text-slate-500">Local dataset weight vs validation accuracy across edge clients</p>

        </div>

      </div>



      <div style={{ width: '100%', height }}>

        <ResponsiveContainer>

          <BarChart data={data} margin={{ top: 10, right: 20, left: -10, bottom: 0 }}>

            <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />

            <XAxis dataKey="hospital" stroke="#94a3b8" tick={{ fontSize: 11 }} />

            <YAxis yAxisId="samples" orientation="left" stroke="#3b82f6" tick={{ fontSize: 11 }} />

            <YAxis yAxisId="acc" orientation="right" stroke="#10b981" domain={[0, 1]} tick={{ fontSize: 11 }} />

            <Tooltip

              contentStyle={{

                backgroundColor: '#ffffff',

                borderColor: '#e2e8f0',

                borderRadius: '0.75rem',

                fontSize: '12px'

              }}

            />

            <Legend wrapperStyle={{ fontSize: '12px' }} />

            <Bar yAxisId="samples" dataKey="samples" name="Local Samples" fill="#3b82f6" radius={[4, 4, 0, 0]} />

            <Bar yAxisId="acc" dataKey="accuracy" name="Local Accuracy" fill="#10b981" radius={[4, 4, 0, 0]} />

          </BarChart>

        </ResponsiveContainer>

      </div>

    </div>

  );

};
