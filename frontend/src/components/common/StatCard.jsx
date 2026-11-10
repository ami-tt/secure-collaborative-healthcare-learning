import React from 'react';



export const StatCard = ({ title, value, subtitle, icon: Icon, trend, color = 'teal' }) => {

  const colorStyles = {

    teal: {

      iconBg: 'bg-teal-50 text-teal-600 border-teal-100',

      badge: 'text-teal-700 bg-teal-50',

    },

    blue: {

      iconBg: 'bg-blue-50 text-blue-600 border-blue-100',

      badge: 'text-blue-700 bg-blue-50',

    },

    purple: {

      iconBg: 'bg-purple-50 text-purple-600 border-purple-100',

      badge: 'text-purple-700 bg-purple-50',

    },

    amber: {

      iconBg: 'bg-amber-50 text-amber-600 border-amber-100',

      badge: 'text-amber-700 bg-amber-50',

    },

  };



  const style = colorStyles[color] || colorStyles.teal;



  return (

    <div className="bg-white rounded-xl border border-slate-200/90 p-5 shadow-sm hover:shadow-md transition-all duration-200">

      <div className="flex items-center justify-between">

        <div>

          <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">{title}</p>

          <h3 className="text-2xl font-bold text-slate-900 mt-1">{value}</h3>

          {subtitle && (

            <p className="text-xs text-slate-500 mt-1 flex items-center gap-1">

              {trend && (

                <span className={`font-semibold px-1.5 py-0.5 rounded text-[11px] ${style.badge}`}>

                  {trend}

                </span>

              )}

              <span>{subtitle}</span>

            </p>

          )}

        </div>

        {Icon && (

          <div className={`w-12 h-12 rounded-xl border flex items-center justify-center shrink-0 ${style.iconBg}`}>

            <Icon className="w-6 h-6" />

          </div>

        )}

      </div>

    </div>

  );

};
