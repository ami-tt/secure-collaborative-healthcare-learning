import React from 'react';

import {

  Shield, Activity, Lock, Database, Cpu, ArrowRight,

  CheckCircle2, Network, EyeOff, FileText, Building2, UserCheck

} from 'lucide-react';



export const LandingPage = ({ onGetStarted, onSignIn }) => {

  return (

    <div className="min-h-screen bg-slate-50 text-slate-900">

      {/* Hero Section */}

      <section className="relative overflow-hidden pt-12 pb-20 lg:pt-20 lg:pb-28 border-b border-slate-200/80 bg-white">

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">

          <div className="text-center max-w-3xl mx-auto">

            {/* Badge */}

            <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-teal-50 border border-teal-200 text-teal-800 text-xs font-semibold uppercase tracking-wider mb-6">

              <Shield className="w-3.5 h-3.5 text-teal-600" />

              <span>Decentralized Healthcare AI &bull; HIPAA & GDPR Compliant</span>

            </div>



            {/* Main Headline */}

            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-slate-900 tracking-tight leading-tight sm:leading-none">

              Train Clinical AI Models <br className="hidden sm:inline" />

              <span className="bg-gradient-to-r from-teal-600 to-blue-700 bg-clip-text text-transparent">

                Without Moving Patient Data

              </span>

            </h1>



            {/* Subheading */}

            <p className="mt-6 text-lg sm:text-xl text-slate-600 leading-relaxed font-normal">

              A secure federated learning platform empowering hospitals and medical research centers

              to collaboratively train predictive neural networks using Flower (FedAvg) and Differential Privacy —

              guaranteeing absolute patient data sovereignty.

            </p>



            {/* Call to Action Buttons */}

            <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">

              <button

                onClick={onGetStarted}

                className="w-full sm:w-auto flex items-center justify-center space-x-2 px-8 py-3.5 rounded-xl bg-teal-600 hover:bg-teal-700 text-white font-semibold shadow-lg shadow-teal-600/25 transition-all text-sm"

              >

                <span>Launch Interactive Demo</span>

                <ArrowRight className="w-4 h-4" />

              </button>

              <button

                onClick={onSignIn}

                className="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-800 font-semibold border border-slate-300 transition text-sm"

              >

                Sign In to Dashboard

              </button>

            </div>



            {/* Platform Trust Highlights */}

            <div className="mt-12 grid grid-cols-2 sm:grid-cols-4 gap-6 pt-8 border-t border-slate-100 text-left">

              <div>

                <p className="text-2xl font-bold text-slate-900">0 KB</p>

                <p className="text-xs text-slate-500 font-medium">Raw Patient Data Shared</p>

              </div>

              <div>

                <p className="text-2xl font-bold text-teal-600">FedAvg</p>

                <p className="text-xs text-slate-500 font-medium">Weighted Model Aggregation</p>

              </div>

              <div>

                <p className="text-2xl font-bold text-blue-700">DP-SGD</p>

                <p className="text-xs text-slate-500 font-medium">Calibrated (&epsilon;, &delta;) Noise</p>

              </div>

              <div>

                <p className="text-2xl font-bold text-purple-700">3 Roles</p>

                <p className="text-xs text-slate-500 font-medium">Admin &bull; Hospital &bull; Researcher</p>

              </div>

            </div>

          </div>

        </div>

      </section>



      {/* How Federated Learning Works Section */}

      <section className="py-20 bg-slate-50">

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

          <div className="text-center max-w-2xl mx-auto mb-16">

            <h2 className="text-xs font-bold uppercase tracking-wider text-teal-700">Architecture Pipeline</h2>

            <h3 className="text-3xl font-bold text-slate-900 mt-2">How Collaborative Healthcare Learning Works</h3>

            <p className="text-sm text-slate-600 mt-2">The complete 4-step federated training lifecycle ensuring zero patient data leakage.</p>

          </div>



          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">

            {/* Step 1 */}

            <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs relative">

              <div className="w-10 h-10 rounded-xl bg-blue-50 text-blue-700 font-bold flex items-center justify-center mb-4 text-sm">

                01

              </div>

              <h4 className="text-base font-bold text-slate-900 mb-2">Model Broadcast</h4>

              <p className="text-xs text-slate-600 leading-relaxed">

                The central Flower server broadcasts initial global PyTorch model weights to verified hospital edge clients.

              </p>

            </div>



            {/* Step 2 */}

            <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs relative">

              <div className="w-10 h-10 rounded-xl bg-teal-50 text-teal-700 font-bold flex items-center justify-center mb-4 text-sm">

                02

              </div>

              <h4 className="text-base font-bold text-slate-900 mb-2">Local Edge Training</h4>

              <p className="text-xs text-slate-600 leading-relaxed">

                Each hospital trains the neural network locally on its own private Electronic Health Records (EHR) behind hospital firewalls.

              </p>

            </div>



            {/* Step 3 */}

            <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs relative">

              <div className="w-10 h-10 rounded-xl bg-purple-50 text-purple-700 font-bold flex items-center justify-center mb-4 text-sm">

                03

              </div>

              <h4 className="text-base font-bold text-slate-900 mb-2">Differential Privacy</h4>

              <p className="text-xs text-slate-600 leading-relaxed">

                Local weight gradients are bounded via L2-norm clipping and masked with calibrated Gaussian noise to prevent model inversion attacks.

              </p>

            </div>



            {/* Step 4 */}

            <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs relative">

              <div className="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-700 font-bold flex items-center justify-center mb-4 text-sm">

                04

              </div>

              <h4 className="text-base font-bold text-slate-900 mb-2">Secure Aggregation</h4>

              <p className="text-xs text-slate-600 leading-relaxed">

                The central aggregator combines all encrypted client updates using Federated Averaging (FedAvg), yielding a robust global model.

              </p>

            </div>

          </div>

        </div>

      </section>



      {/* Security & Regulatory Highlights */}

      <section className="py-20 bg-white border-t border-slate-200/80">

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">

            <div>

              <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-purple-50 text-purple-700 text-xs font-semibold uppercase mb-4">

                <Lock className="w-3.5 h-3.5" />

                <span>Defense-in-Depth Security</span>

              </div>

              <h3 className="text-3xl font-extrabold text-slate-900 tracking-tight">

                Enterprise-Grade Privacy Guarantees for Healthcare

              </h3>

              <p className="mt-4 text-sm text-slate-600 leading-relaxed">

                Conventional AI centralization creates catastrophic liability and regulatory risk under HIPAA and GDPR.

                Our platform introduces a verifiable, multi-layered security framework designed specifically for clinical environments.

              </p>



              <div className="mt-8 space-y-4">

                <div className="flex items-start space-x-3">

                  <div className="p-1 rounded-full bg-teal-100 text-teal-700 mt-0.5">

                    <CheckCircle2 className="w-4 h-4" />

                  </div>

                  <div>

                    <h5 className="text-sm font-bold text-slate-900">Zero Data Movement Policy</h5>

                    <p className="text-xs text-slate-500">Electronic Health Records and DICOM images remain strictly on local premises.</p>

                  </div>

                </div>



                <div className="flex items-start space-x-3">

                  <div className="p-1 rounded-full bg-teal-100 text-teal-700 mt-0.5">

                    <CheckCircle2 className="w-4 h-4" />

                  </div>

                  <div>

                    <h5 className="text-sm font-bold text-slate-900">Mathematical Differential Privacy (DP-SGD)</h5>

                    <p className="text-xs text-slate-500">Guarantees that an adversary cannot reconstruct individual patient records from model weights.</p>

                  </div>

                </div>



                <div className="flex items-start space-x-3">

                  <div className="p-1 rounded-full bg-teal-100 text-teal-700 mt-0.5">

                    <CheckCircle2 className="w-4 h-4" />

                  </div>

                  <div>

                    <h5 className="text-sm font-bold text-slate-900">Immutable Compliance Audit Logs</h5>

                    <p className="text-xs text-slate-500">Every training round, weight submission, and authentication event is cryptographically recorded.</p>

                  </div>

                </div>

              </div>

            </div>



            <div className="bg-slate-900 text-slate-200 p-8 rounded-2xl shadow-xl border border-slate-800">

              <div className="flex items-center justify-between pb-4 border-b border-slate-800">

                <span className="text-xs font-mono text-teal-400">FL_SESSION_TELEMETRY.log</span>

                <span className="text-[11px] px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 font-semibold">Active Node</span>

              </div>

              <pre className="mt-4 text-xs font-mono text-slate-300 leading-relaxed overflow-x-auto">

{`[FEDERATED ORCHESTRATOR] Initializing Round 03/10

-> Client Connected: HOSP-ALPHA-01 (1,200 local EHR samples)

-> Client Connected: HOSP-BETA-02  (850 local EHR samples)

-> Local Training Initiated: PyTorch TabularMLP (SGD, lr=0.001)

-> DP-Engine: Norm Clipping (C=1.0), Gaussian Noise Applied (sigma=0.74)

-> Parameter Serialization: SHA-256 Verified

-> Central Aggregation: Weighted FedAvg Complete

[RESULT] Global Accuracy: 89.4% | Global Loss: 0.281

[AUDIT] Round 03 event persisted to PostgreSQL audit trail`}

              </pre>

            </div>

          </div>

        </div>

      </section>



      {/* Footer */}

      <footer className="bg-slate-900 text-slate-400 py-12 border-t border-slate-800">

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center sm:text-left sm:flex sm:items-center sm:justify-between">

          <div className="flex items-center justify-center sm:justify-start space-x-2">

            <div className="w-8 h-8 rounded-lg bg-teal-600 flex items-center justify-center text-white">

              <Shield className="w-4 h-4" />

            </div>

            <span className="text-base font-bold text-white">SecureFL Health</span>

          </div>

          <p className="mt-4 sm:mt-0 text-xs text-slate-500">

            Secure Collaborative Healthcare Learning System &bull; Major Project Implementation &bull; 2026

          </p>

        </div>

      </footer>

    </div>

  );

};
