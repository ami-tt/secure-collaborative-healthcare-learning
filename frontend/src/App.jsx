import React, { useState } from 'react';

import { AuthProvider, useAuth } from './contexts/AuthContext';

import { Navbar } from './components/common/Navbar';

import { LandingPage } from './pages/landing/LandingPage';

import { LoginPage } from './pages/auth/LoginPage';

import { RegisterPage } from './pages/auth/RegisterPage';

import { AdminDashboard } from './pages/admin/AdminDashboard';

import { HospitalDashboard } from './pages/hospital/HospitalDashboard';

import { ResearcherDashboard } from './pages/researcher/ResearcherDashboard';

import { FLMonitorDashboard } from './pages/fl_monitor/FLMonitorDashboard';

import { SecurityDashboard } from './pages/security/SecurityDashboard';



const MainContent = () => {

  const { user, loading } = useAuth();

  const [activeTab, setActiveTab] = useState('landing');



  if (loading) {

    return (

      <div className="min-h-screen bg-slate-50 flex items-center justify-center">

        <div className="flex flex-col items-center space-y-3">

          <div className="w-10 h-10 border-4 border-teal-600 border-t-transparent rounded-full animate-spin"></div>

          <p className="text-xs font-semibold text-slate-500">Connecting to SecureFL Health...</p>

        </div>

      </div>

    );

  }



  // Unauthenticated routing

  if (!user) {

    if (activeTab === 'login') {

      return (

        <div>

          <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />

          <LoginPage

            onNavigateToRegister={() => setActiveTab('register')}

            onLoginSuccess={() => setActiveTab('dashboard')}

          />

        </div>

      );

    }

    if (activeTab === 'register') {

      return (

        <div>

          <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />

          <RegisterPage

            onNavigateToLogin={() => setActiveTab('login')}

            onRegisterSuccess={() => setActiveTab('login')}

          />

        </div>

      );

    }

    return (

      <div>

        <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />

        <LandingPage

          onGetStarted={() => setActiveTab('register')}

          onSignIn={() => setActiveTab('login')}

        />

      </div>

    );

  }



  // Authenticated Dashboard Layout

  const renderRoleDashboard = () => {

    switch (user.role) {

      case 'admin':

        return <AdminDashboard />;

      case 'hospital_admin':

        return <HospitalDashboard />;

      case 'researcher':

        return <ResearcherDashboard onOpenMonitor={() => setActiveTab('monitor')} />;

      default:

        return <ResearcherDashboard onOpenMonitor={() => setActiveTab('monitor')} />;

    }

  };



  return (

    <div className="min-h-screen bg-slate-50 flex flex-col font-sans">

      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">

        {activeTab === 'monitor' && <FLMonitorDashboard />}

        {activeTab === 'security' && <SecurityDashboard />}

        {activeTab === 'dashboard' && renderRoleDashboard()}

        {activeTab === 'landing' && renderRoleDashboard()}

      </main>

    </div>

  );

};



export default function App() {

  return (

    <AuthProvider>

      <MainContent />

    </AuthProvider>

  );

}
