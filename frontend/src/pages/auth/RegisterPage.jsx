import React, { useState } from 'react';

import { Shield, Lock, Mail, User, Building, ArrowRight, AlertCircle, CheckCircle2 } from 'lucide-react';

import { useAuth } from '../../contexts/AuthContext';



export const RegisterPage = ({ onNavigateToLogin, onRegisterSuccess }) => {

  const { register } = useAuth();

  const [formData, setFormData] = useState({

    full_name: '',

    email: '',

    password: '',

    role: 'researcher',

    institution_id: '',

  });

  const [error, setError] = useState(null);

  const [success, setSuccess] = useState(false);

  const [loading, setLoading] = useState(false);



  const handleSubmit = async (e) => {

    e.preventDefault();

    setError(null);

    setLoading(true);



    try {

      const payload = {

        full_name: formData.full_name,

        email: formData.email,

        password: formData.password,

        role: formData.role,

        institution_id: formData.institution_id || null,

      };



      await register(payload);

      setSuccess(true);

      setTimeout(() => {

        if (onRegisterSuccess) onRegisterSuccess();

      }, 1500);

    } catch (err) {

      setError(

        err.response?.data?.detail || 'Failed to register account. Please check your information.'

      );

    } finally {

      setLoading(false);

    }

  };



  return (

    <div className="min-h-screen bg-slate-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">

      <div className="sm:mx-auto sm:w-full sm:max-w-md text-center">

        <div className="inline-flex w-12 h-12 rounded-2xl bg-gradient-to-tr from-teal-600 to-blue-700 items-center justify-center shadow-lg shadow-teal-600/20 text-white mb-3">

          <Shield className="w-6 h-6" />

        </div>

        <h2 className="text-2xl font-bold tracking-tight text-slate-900">

          Create Healthcare Account

        </h2>

        <p className="mt-1 text-xs text-slate-500">

          Register to participate in privacy-preserving clinical research

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



          {success && (

            <div className="mb-5 p-3.5 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-700 text-xs flex items-center space-x-2">

              <CheckCircle2 className="w-4 h-4 shrink-0 text-emerald-600" />

              <span>Registration successful! Redirecting to login...</span>

            </div>

          )}



          <form className="space-y-4" onSubmit={handleSubmit}>

            {/* Role Selection */}

            <div>

              <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1.5">

                Select Your Role

              </label>

              <div className="grid grid-cols-3 gap-2">

                {[

                  { id: 'researcher', label: 'Researcher' },

                  { id: 'hospital_admin', label: 'Hospital' },

                  { id: 'admin', label: 'Admin' },

                ].map((r) => (

                  <button

                    key={r.id}

                    type="button"

                    onClick={() => setFormData({ ...formData, role: r.id })}

                    className={`py-2 px-1 text-center rounded-xl text-xs font-semibold border transition ${

                      formData.role === r.id

                        ? 'border-teal-600 bg-teal-50 text-teal-800'

                        : 'border-slate-200 bg-white text-slate-600 hover:bg-slate-50'

                    }`}

                  >

                    {r.label}

                  </button>

                ))}

              </div>

            </div>



            {/* Full Name */}

            <div>

              <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">

                Full Name & Title

              </label>

              <div className="relative rounded-xl border border-slate-200 focus-within:border-teal-600 focus-within:ring-1 focus-within:ring-teal-600 bg-white">

                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">

                  <User className="w-4 h-4" />

                </div>

                <input

                  type="text"

                  required

                  value={formData.full_name}

                  onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}

                  placeholder="Dr. John Doe, MD"

                  className="block w-full pl-10 pr-3.5 py-2.5 text-xs text-slate-900 placeholder:text-slate-400 bg-transparent focus:outline-none"

                />

              </div>

            </div>



            {/* Email */}

            <div>

              <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">

                Institutional Email

              </label>

              <div className="relative rounded-xl border border-slate-200 focus-within:border-teal-600 focus-within:ring-1 focus-within:ring-teal-600 bg-white">

                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">

                  <Mail className="w-4 h-4" />

                </div>

                <input

                  type="email"

                  required

                  value={formData.email}

                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}

                  placeholder="doctor@hospital.org"

                  className="block w-full pl-10 pr-3.5 py-2.5 text-xs text-slate-900 placeholder:text-slate-400 bg-transparent focus:outline-none"

                />

              </div>

            </div>



            {/* Password */}

            <div>

              <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">

                Password (min. 8 characters)

              </label>

              <div className="relative rounded-xl border border-slate-200 focus-within:border-teal-600 focus-within:ring-1 focus-within:ring-teal-600 bg-white">

                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">

                  <Lock className="w-4 h-4" />

                </div>

                <input

                  type="password"

                  required

                  minLength={8}

                  value={formData.password}

                  onChange={(e) => setFormData({ ...formData, password: e.target.value })}

                  placeholder="••••••••••••"

                  className="block w-full pl-10 pr-3.5 py-2.5 text-xs text-slate-900 placeholder:text-slate-400 bg-transparent focus:outline-none"

                />

              </div>

            </div>



            <button

              type="submit"

              disabled={loading || success}

              className="w-full mt-2 flex justify-center items-center space-x-2 py-3 px-4 rounded-xl text-xs font-semibold text-white bg-teal-600 hover:bg-teal-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-500 shadow-md shadow-teal-600/20 transition disabled:opacity-60"

            >

              {loading ? (

                <span>Registering Account...</span>

              ) : (

                <>

                  <span>Create Account</span>

                  <ArrowRight className="w-4 h-4" />

                </>

              )}

            </button>

          </form>



          <div className="mt-6 text-center">

            <button

              type="button"

              onClick={onNavigateToLogin}

              className="text-xs text-slate-600 hover:text-teal-700 font-medium transition"

            >

              Already have an account? <span className="font-bold underline">Sign in here</span>

            </button>

          </div>

        </div>

      </div>

    </div>

  );

};
