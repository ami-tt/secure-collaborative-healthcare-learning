import React, { useState } from 'react';
import {
    Activity,
    AlertCircle,
    LoaderCircle,
    RotateCcw,
    ShieldCheck,
} from 'lucide-react';

import { predictionService } from '../../services/api';

const initialForm = {
    age: '50.36',
    gender: '2',
    height: '168',
    weight: '62',
    ap_hi: '110',
    ap_lo: '80',
    cholesterol: '1',
    gluc: '1',
    smoke: '0',
    alco: '0',
    active: '1',
};

const inputClass =
    'w-full px-3 py-2.5 rounded-xl border border-slate-200 bg-white text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-teal-500';

const labelClass =
    'block text-xs font-semibold text-slate-700 mb-1.5';

// Validate patient information before sending it to the backend.
const validateForm = (form) => {
    const numericFields = [
        'age', 'gender', 'height', 'weight',
        'ap_hi', 'ap_lo', 'cholesterol',
        'gluc', 'smoke', 'alco', 'active',
    ];

    for (const field of numericFields) {
        if (
            form[field] === '' ||
            !Number.isFinite(Number(form[field]))
        ) {
            return 'Please complete all fields with valid numeric values.';
        }
    }

    const age = Number(form.age);
    const gender = Number(form.gender);
    const height = Number(form.height);
    const weight = Number(form.weight);
    const systolic = Number(form.ap_hi);
    const diastolic = Number(form.ap_lo);
    const cholesterol = Number(form.cholesterol);
    const glucose = Number(form.gluc);
    const smoke = Number(form.smoke);
    const alcohol = Number(form.alco);
    const active = Number(form.active);

    if (age < 1 || age > 150) {
        return 'Age must be between 1 and 150 years.';
    }

    if (![1, 2].includes(gender)) {
        return 'Please select a valid gender.';
    }

    if (height < 120 || height > 220) {
        return 'Height must be between 120 and 220 cm.';
    }

    if (weight < 35 || weight > 200) {
        return 'Weight must be between 35 and 200 kg.';
    }

    if (systolic < 60 || systolic > 240) {
        return 'Systolic blood pressure must be between 60 and 240 mmHg.';
    }

    if (diastolic < 40 || diastolic > 180) {
        return 'Diastolic blood pressure must be between 40 and 180 mmHg.';
    }

    if (systolic <= diastolic) {
        return 'Systolic blood pressure must be greater than diastolic blood pressure. Please check both values.';
    }

    if (![1, 2, 3].includes(cholesterol)) {
        return 'Please select a valid cholesterol level.';
    }

    if (![1, 2, 3].includes(glucose)) {
        return 'Please select a valid glucose level.';
    }

    if (![0, 1].includes(smoke)) {
        return 'Please select a valid smoking value.';
    }

    if (![0, 1].includes(alcohol)) {
        return 'Please select a valid alcohol consumption value.';
    }

    if (![0, 1].includes(active)) {
        return 'Please select a valid physical activity value.';
    }

    return '';
};

export const CardiovascularPrediction = () => {
    const [form, setForm] = useState(initialForm);
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleChange = (e) => {
        const { name, value } = e.target;

        setForm((prev) => ({
            ...prev,
            [name]: value,
        }));

        setResult(null);
        setError('');
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        const validationError = validateForm(form);

        if (validationError) {
            setResult(null);
            setError(validationError);
            return;
        }

        setLoading(true);
        setError('');
        setResult(null);

        try {
            const patientData = {
                age: Number(form.age) * 365.25,
                gender: Number(form.gender),
                height: Number(form.height),
                weight: Number(form.weight),
                ap_hi: Number(form.ap_hi),
                ap_lo: Number(form.ap_lo),
                cholesterol: Number(form.cholesterol),
                gluc: Number(form.gluc),
                smoke: Number(form.smoke),
                alco: Number(form.alco),
                active: Number(form.active),
            };

            const response =
                await predictionService.predict(patientData);

            setResult(response);

        } catch (err) {
            const detail = err.response?.data?.detail;

            setError(
                typeof detail === 'string'
                    ? detail
                    : 'Unable to generate prediction. Please check your entries and connection, then try again.'
            );

        } finally {
            setLoading(false);
        }
    };

    const handleReset = () => {
        setForm(initialForm);
        setResult(null);
        setError('');
    };

    return (
        <div className="space-y-6">

            {/* Header */}
            <div className="bg-white p-6 rounded-2xl border border-slate-200">
                <div className="flex items-center gap-3">

                    <div className="p-3 bg-teal-50 rounded-xl">
                        <Activity className="w-6 h-6 text-teal-600" />
                    </div>

                    <div>
                        <h2 className="text-lg font-bold text-slate-900">
                            Cardiovascular Risk Prediction
                        </h2>

                        <p className="text-xs text-slate-500 mt-1">
                            AI-powered prediction using the trained TabularMLP model
                        </p>
                    </div>

                </div>
            </div>

            {/* Input Form */}
            <div className="bg-white p-6 rounded-2xl border border-slate-200">

                <h3 className="text-sm font-bold text-slate-900 mb-5">
                    Patient Information
                </h3>

                <form
                    onSubmit={handleSubmit}
                    className="space-y-5"
                    noValidate
                >

                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">

                        {/* Age */}
                        <div>
                            <label htmlFor="age" className={labelClass}>
                                Age (Years)
                            </label>

                            <input
                                id="age"
                                type="number"
                                name="age"
                                value={form.age}
                                onChange={handleChange}
                                min="1"
                                max="150"
                                step="0.01"
                                required
                                className={inputClass}
                            />
                        </div>

                        {/* Gender */}
                        <div>
                            <label htmlFor="gender" className={labelClass}>
                                Gender
                            </label>

                            <select
                                id="gender"
                                name="gender"
                                value={form.gender}
                                onChange={handleChange}
                                className={inputClass}
                            >
                                <option value="1">Female (1)</option>
                                <option value="2">Male (2)</option>
                            </select>
                        </div>

                        {/* Height */}
                        <div>
                            <label htmlFor="height" className={labelClass}>
                                Height (cm)
                            </label>

                            <input
                                id="height"
                                type="number"
                                name="height"
                                value={form.height}
                                onChange={handleChange}
                                min="120"
                                max="220"
                                step="any"
                                required
                                className={inputClass}
                            />
                        </div>

                        {/* Weight */}
                        <div>
                            <label htmlFor="weight" className={labelClass}>
                                Weight (kg)
                            </label>

                            <input
                                id="weight"
                                type="number"
                                name="weight"
                                value={form.weight}
                                onChange={handleChange}
                                min="35"
                                max="200"
                                step="0.1"
                                required
                                className={inputClass}
                            />
                        </div>

                        {/* Systolic BP */}
                        <div>
                            <label htmlFor="ap_hi" className={labelClass}>
                                Systolic Blood Pressure (mmHg)
                            </label>

                            <input
                                id="ap_hi"
                                type="number"
                                name="ap_hi"
                                value={form.ap_hi}
                                onChange={handleChange}
                                min="60"
                                max="240"
                                step="1"
                                required
                                className={inputClass}
                            />
                        </div>

                        {/* Diastolic BP */}
                        <div>
                            <label htmlFor="ap_lo" className={labelClass}>
                                Diastolic Blood Pressure (mmHg)
                            </label>

                            <input
                                id="ap_lo"
                                type="number"
                                name="ap_lo"
                                value={form.ap_lo}
                                onChange={handleChange}
                                min="40"
                                max="180"
                                step="1"
                                required
                                className={inputClass}
                            />
                        </div>

                        {/* Cholesterol */}
                        <div>
                            <label htmlFor="cholesterol" className={labelClass}>
                                Cholesterol Level
                            </label>

                            <select
                                id="cholesterol"
                                name="cholesterol"
                                value={form.cholesterol}
                                onChange={handleChange}
                                className={inputClass}
                            >
                                <option value="1">Normal (1)</option>
                                <option value="2">Above Normal (2)</option>
                                <option value="3">Well Above Normal (3)</option>
                            </select>
                        </div>

                        {/* Glucose */}
                        <div>
                            <label htmlFor="gluc" className={labelClass}>
                                Glucose Level
                            </label>

                            <select
                                id="gluc"
                                name="gluc"
                                value={form.gluc}
                                onChange={handleChange}
                                className={inputClass}
                            >
                                <option value="1">Normal (1)</option>
                                <option value="2">Above Normal (2)</option>
                                <option value="3">Well Above Normal (3)</option>
                            </select>
                        </div>

                        {/* Smoking */}
                        <div>
                            <label htmlFor="smoke" className={labelClass}>
                                Smoking
                            </label>

                            <select
                                id="smoke"
                                name="smoke"
                                value={form.smoke}
                                onChange={handleChange}
                                className={inputClass}
                            >
                                <option value="0">No</option>
                                <option value="1">Yes</option>
                            </select>
                        </div>

                        {/* Alcohol */}
                        <div>
                            <label htmlFor="alco" className={labelClass}>
                                Alcohol Consumption
                            </label>

                            <select
                                id="alco"
                                name="alco"
                                value={form.alco}
                                onChange={handleChange}
                                className={inputClass}
                            >
                                <option value="0">No</option>
                                <option value="1">Yes</option>
                            </select>
                        </div>

                        {/* Physical Activity */}
                        <div>
                            <label htmlFor="active" className={labelClass}>
                                Physical Activity
                            </label>

                            <select
                                id="active"
                                name="active"
                                value={form.active}
                                onChange={handleChange}
                                className={inputClass}
                            >
                                <option value="1">Active</option>
                                <option value="0">Not Active</option>
                            </select>
                        </div>

                    </div>

                    {/* Error Message */}
                    {error && (
                        <div
                            role="alert"
                            className="p-3 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-sm flex items-center gap-2"
                        >
                            <AlertCircle className="w-5 h-5 shrink-0" />
                            <span>{error}</span>
                        </div>
                    )}

                    {/* Buttons */}
                    <div className="flex flex-wrap gap-3 pt-3">

                        <button
                            type="submit"
                            disabled={loading}
                            className="flex items-center gap-2 px-5 py-3 rounded-xl bg-teal-600 hover:bg-teal-700 text-white text-sm font-semibold disabled:opacity-60"
                        >
                            {loading ? (
                                <>
                                    <LoaderCircle className="w-4 h-4 animate-spin" />
                                    Generating Prediction...
                                </>
                            ) : (
                                <>
                                    <Activity className="w-4 h-4" />
                                    Predict Cardiovascular Risk
                                </>
                            )}
                        </button>

                        <button
                            type="button"
                            onClick={handleReset}
                            disabled={loading}
                            className="flex items-center gap-2 px-5 py-3 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 text-sm font-semibold disabled:opacity-60"
                        >
                            <RotateCcw className="w-4 h-4" />
                            Reset
                        </button>

                    </div>

                </form>
            </div>

            {/* Prediction Result */}
            {result && (
                <div className="bg-white p-6 rounded-2xl border border-slate-200">

                    <div className="flex items-center gap-2 mb-5">
                        <ShieldCheck className="w-5 h-5 text-teal-600" />

                        <h3 className="text-base font-bold text-slate-900">
                            Prediction Result
                        </h3>
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">

                        <div className="p-5 rounded-xl bg-teal-50 border border-teal-100">
                            <p className="text-xs font-semibold text-teal-800">
                                Model Output Probability
                            </p>

                            <p className="text-3xl font-bold text-teal-700 mt-2">
                                {(result.risk_probability * 100).toFixed(2)}%
                            </p>
                        </div>

                        <div className="p-5 rounded-xl bg-blue-50 border border-blue-100">
                            <p className="text-xs font-semibold text-blue-800">
                                Predicted Class
                            </p>

                            <p className="text-3xl font-bold text-blue-700 mt-2">
                                {result.predicted_class}
                            </p>

                            <p className="text-xs text-blue-700 mt-1">
                                {result.predicted_class === 1
                                    ? 'Positive class'
                                    : 'Negative class'}
                            </p>
                        </div>

                    </div>

                    <div className="mt-4 p-4 bg-slate-50 rounded-xl">

                        <p className="text-xs text-slate-600">
                            <strong>Model:</strong> {result.model_name}
                        </p>

                        <p className="text-xs text-slate-500 mt-2">
                            {result.disclaimer}
                        </p>

                    </div>
                </div>
            )}

        </div>
    );
};

export default CardiovascularPrediction;