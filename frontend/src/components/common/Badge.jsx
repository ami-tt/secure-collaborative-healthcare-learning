import React from 'react';



export const Badge = ({ status, text, variant = 'default' }) => {

  const getBadgeStyle = (val) => {

    switch (val?.toLowerCase()) {

      case 'active':

      case 'connected':

      case 'completed':

      case 'success':

        return 'bg-emerald-50 text-emerald-700 border-emerald-200';

      case 'in_progress':

      case 'training':

      case 'running':

        return 'bg-blue-50 text-blue-700 border-blue-200 animate-pulse';

      case 'pending':

      case 'pending_verification':

      case 'waiting_for_clients':

      case 'idle':

      case 'created':

        return 'bg-amber-50 text-amber-700 border-amber-200';

      case 'suspended':

      case 'failed':

      case 'decommissioned':

      case 'disconnected':

      case 'error':

        return 'bg-rose-50 text-rose-700 border-rose-200';

      case 'admin':

        return 'bg-purple-50 text-purple-700 border-purple-200';

      case 'hospital_admin':

        return 'bg-teal-50 text-teal-700 border-teal-200';

      case 'researcher':

        return 'bg-sky-50 text-sky-700 border-sky-200';

      default:

        return 'bg-slate-100 text-slate-700 border-slate-200';

    }

  };



  const displayText = text || status?.replace(/_/g, ' ') || 'Unknown';



  return (

    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${getBadgeStyle(status || variant)}`}>

      <span className="w-1.5 h-1.5 rounded-full mr-1.5 bg-current opacity-70"></span>

      <span className="capitalize">{displayText}</span>

    </span>

  );

};
