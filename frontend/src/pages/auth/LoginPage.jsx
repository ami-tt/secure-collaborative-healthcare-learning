import React, { useState } from 'react';

import { Shield, Lock, Mail, ArrowRight, AlertCircle, CheckCircle2 } from 'lucide-react';

import { useAuth } from '../../contexts/AuthContext';



export const LoginPage = ({ onNavigateToRegister, onLoginSuccess }) => {

  const { login } = useAuth();

  const [email, setEmail] = useState('');

  const [password, setPassword] = useState('');

  const [error, setError] = useState(null);

  const [loading, setLoading] = useState(false);



  const handleSubmit = async (e) => {

    e.preventDefault();

    setError(null);

    setLoading(true);



    try {

      await login(email, password);

      if (onLoginSuccess) onLoginSuccess();

    } catch (err) {

      setError(

        err.response?.data?.detail || 'Invalid email or password. Please verify credentials.'

      );

    } finally {

      setLoading(false);

    }

  };



  const fillQuickCredentials = (demoEmail, demoPassword) => {

    setEmail(demoEmail);

    setPassword(demoPassword);

    setError(null);

  };



  return (

    <div className="min-h-screen bg-slate-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">

      <div className="sm:mx-auto sm:w-full sm:max-w-md text-center">

        <div className="inline-flex w-12 h-12 rounded-2xl bg-gradient-to-tr from-teal-600 to-blue-700 items-center justify-center shadow-lg shadow-teal-600/20 text-white mb-3">

          <Shield className="w-6 h-6" />

        </div>

        <h2 className="text-2xl font-bold tracking-tight text-slate-900">

          Sign In to SecureFL Health

        </h2>

        <p className="mt-1 text-xs text-slate-500">

          Access your federated learning portal and institutional controls

        </p>

      </div>



      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">

        <div className="bg-white py-8 px-6 sm:px-10 shadow-sm border border-slate-200/90 rounded-2xl">

          {error && (

            <div className="mb-5 p-3.5 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-xs flex items-center space-x-2">

              <AlertCircle className="w-4 h-4 shrink-0 text-rose-600" />

              <span>{error}</span>

            </div>

          )}



          <form className="space-y-4" onSubmit={handleSubmit}>

            <div>

              <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">

                Email Address

              </label>

              <div className="relative rounded-xl border border-slate-200 focus-within:border-teal-600 focus-within:ring-1 focus-within:ring-teal-600 bg-white">

                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">

                  <Mail className="w-4 h-4" />

                </div>

                <input

                  type="email"

                  required

                  value={email}

                  onChange={(e) => setEmail(e.target.value)}

                  placeholder="doctor@hospital.org"

                  className="block w-full pl-10 pr-3.5 py-2.5 text-xs text-slate-900 placeholder:text-slate-400 bg-transparent focus:outline-none"

                />

              </div>

            </div>



            <div>

              <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">

                Password

              </label>

              <div className="relative rounded-xl border border-slate-200 focus-within:border-teal-600 focus-within:ring-1 focus-within:ring-teal-600 bg-white">

                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">

                  <Lock className="w-4 h-4" />

                </div>

                <input

                  type="password"

                  required

                  value={password}

                  onChange={(e) => setPassword(e.target.value)}

                  placeholder="••••••••••••"

                  className="block w-full pl-10 pr-3.5 py-2.5 text-xs text-slate-900 placeholder:text-slate-400 bg-transparent focus:outline-none"

                />

              </div>

            </div>



            <button

              type="submit"

              disabled={loading}

              className="w-full mt-2 flex justify-center items-center space-x-2 py-3 px-4 rounded-xl text-xs font-semibold text-white bg-teal-600 hover:bg-teal-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-500 shadow-md shadow-teal-600/20 transition disabled:opacity-60"

            >

              {loading ? (

                <span>Authenticating...</span>

              ) : (

                <>

                  <span>Sign In</span>

                  <ArrowRight className="w-4 h-4" />

                </>

              )}

            </button>

          </form>



          {/* Quick Demo Fill Buttons for Testing */}

          <div className="mt-6 pt-5 border-t border-slate-100">

            <p className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider text-center mb-2.5">

              Instant Demo Credentials

            </p>

            <div className="grid grid-cols-3 gap-2">

              <button

                type="button"

                onClick={() => fillQuickCredentials('admin@securefl.health', 'AdminSecurePassword123!')}

                className="p-2 text-center rounded-lg border border-purple-200 bg-purple-50 hover:bg-purple-100 text-purple-700 text-[11px] font-medium transition"

              >

                Super Admin

              </button>

              <button

                type="button"

                onClick={() => fillQuickCredentials('hospadmin@hospital-alpha.org', 'HospAdmin123!')}

                className="p-2 text-center rounded-lg border border-teal-200 bg-teal-50 hover:bg-teal-100 text-teal-700 text-[11px] font-medium transition"

              >

                Hospital Admin

              </button>

              <button

                type="button"

                onClick={() => fillQuickCredentials('researcher@fl-research.org', 'Researcher123!')}

                className="p-2 text-center rounded-lg border border-blue-200 bg-blue-50 hover:bg-blue-100 text-blue-700 text-[11px] font-medium transition"

              >

                Researcher

              </button>

            </div>

          </div>



          <div className="mt-6 text-center">

            <button

              type="button"

              onClick={onNavigateToRegister}

              className="text-xs text-slate-600 hover:text-teal-700 font-medium transition"

            >

              Need a new account? <span className="font-bold underline">Register here</span>

            </button>

          </div>

        </div>

      </div>

    </div>

  );

};
