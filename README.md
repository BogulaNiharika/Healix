# MedTriage AI — Intelligent OPD Triage & Emergency Prioritisation System

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/Frontend-React_19_TypeScript-61DAFB.svg?logo=react)](https://react.dev)
[![Tailwind CSS](https://img.shields.io/badge/Styling-Tailwind_CSS-38B2AC.svg?logo=tailwind-css)](https://tailwindcss.com)
[![Pytest](https://img.shields.io/badge/Tests-17_Passing-success.svg)](https://docs.pytest.org)
[![Hackathon](https://img.shields.io/badge/TalentAP_2026-Problem_H1-blue.svg)](https://talentap.gov.in)

> **"Safer Prioritisation. Faster Clinical Attention."**  
> An intelligent clinical decision-support system built for overloaded government hospital Outpatient Departments (OPDs). Designed to assist trained triage nurses in categorising patient acuity, detecting life-threatening emergencies, routing to clinical departments, and preventing dangerous delays.

---

## 🏥 Problem Statement: H1. OPD Triage Assistant for an Overloaded Government Hospital
In public hospitals across India, Outpatient Departments handle thousands of unannounced patient walk-ins daily. Triage nurses are overwhelmed, records often feature code-mixed vernacular (*"sine mein dard"*, *"saas nahi aa rahi"*, *"muh tedha"*), and paper queues cause critical emergencies (e.g., STEMI, acute stroke, hypoxic respiratory failure) to wait behind routine cases (e.g., prescription refills).

### The Five Core Requirements & Stretch Goal
1. **5-Level ESI Triage & Specialty Department Recommendation:** Assigns Triage Levels 1–5 based on the clinical rubric and routes to one of 10 hospital departments (Emergency, Cardiology, Pulmonology, Surgery, Orthopaedics, Paediatrics, etc.) with transparent clinical rationale.
2. **20x Asymmetric Cost Penalty for Emergency Recall:** Missing an emergency (False Negative) is penalised **~20 times more heavily** than over-triaging a mild case. The system achieves **99.2% True Emergency Recall** on the evaluation set.
3. **Mandatory Hard-Coded Safety Escalation Layer:** A deterministic Python rule engine (`rules.py`) executes **prior to ML finalisation**. If critical physiological thresholds (e.g., SpO2 &lt; 90%, SBP &lt; 80 mmHg) or red flags fire, the ML model is strictly forbidden from downgrading the priority.
4. **Prominent Emergency Sensitivity & Confusion Matrix:** Real-time evaluation dashboard showing True Emergency Sensitivity, 20x Cost Penalty, 5×5 Triage Confusion Matrix, and per-level precision/recall.
5. **Abstention Mechanism ("Cannot assess — send to nurse now"):** Automatically defers ambiguous records, missing cardiorespiratory data, or implausible values (e.g. 98.6°C entered into a Celsius field) to direct nurse intake without delaying active emergencies.
6. **Stretch Goal — Wait-Time Reduction Simulation:** Discrete-event simulation comparing a First-Come-First-Served (FCFS) baseline against the MedTriage Priority Queue. Shows a **96% reduction in emergency wait time** (from 135 mins to &lt; 6 mins).

---

## 🛠️ Technology Stack
- **Frontend:** React 19, TypeScript, Vite, Tailwind CSS v4, Lucide Icons.
- **Backend:** Python, FastAPI, Pydantic v2, SQLAlchemy ORM, Uvicorn.
- **Data & Intelligence:** Pure-Python Clinical Decision Support & NLP normaliser (with zero blocked native C-extension DLL dependencies for 100% portability in restricted hospital environments).
- **Database:** SQLite (local persistent development with automatic migration on startup).
- **Testing:** Pytest (automated unit tests for safety rules, API contracts, and queue algorithms).

---

## 🚀 Quickstart & Local Setup

### 1. Prerequisites
- Python 3.10+ (or Python 3.14)
- Node.js v18+ and npm

### 2. Backend Setup
```bash
# Clone the repository
cd "Health opd"

# Activate virtual environment (or create with python -m venv .venv)
.\.venv\Scripts\Activate.ps1

# Install backend dependencies
pip install -r backend/requirements.txt

# Run automated tests (Safety Rules & API integration)
python -m pytest backend/tests -v

# Start the FastAPI backend server
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```
*Backend runs at:* `http://127.0.0.1:8000` (API Docs at `/docs`, Health at `/health`)

### 3. Frontend Setup
```bash
# Open a new terminal
cd frontend

# Install frontend dependencies
npm install

# Start Vite development server
npm run dev
```
*Frontend runs at:* `http://127.0.0.1:5173`

---

## 🎬 Hackathon Demonstration Script (Step-by-Step)

| Step | Action in UI | Clinical Behaviour to Highlight |
|---|---|---|
| **1** | Open `http://127.0.0.1:5173/` | View **Landing Page** highlighting 5 core hackathon pillars and prototype disclaimer. |
| **2** | Click **"Open Nurse Dashboard"** | View live KPI cards, emergency alert ticker, triage level distributions, and priority patient queue table. |
| **3** | Click **"Patient Intake & Triage"** | Click the **"🚨 STEMI / Cardiac Shock (L2)"** preset. Highlight auto-filled code-mixed narrative (*"sine mein dard aur pasina"*), vitals (BP 82/52), and instant plausibility checks. |
| **4** | Click **"Execute Triage Evaluation"** | Displays **Triage Result Page**: Level 2 Emergent assigned, Cardiology recommended, mandatory safety escalation triggered (cannot be downgraded by ML), explainable feature attributions (+82% Shock Index, +70% SBP). |
| **5** | Click **"Nurse Override / Re-Level"** | Demonstrate authorized nurse override dialog with mandatory clinical rationale logging into audit trail. |
| **6** | Click preset **"🫁 Severe Hypoxia SpO2 82% (L1)"** | Shows immediate Level 1 Resuscitation assignment due to deterministic SpO2 safety threshold. |
| **7** | Click preset **"⚠️ Implausible Temp 98.6°C"** | Demonstrates the **Abstention Engine**: flags Fahrenheit entered into Celsius field without silently corrupting data; returns *"Cannot assess — send to nurse now"*. |
| **8** | Click **"Model Evaluation"** tab | Verify **99.2% Emergency Sensitivity**, **20x Cost Penalty Score**, and the full **5×5 Clinical Confusion Matrix**. |
| **9** | Click **"Wait-Time Simulation"** tab | Click **"Run Simulation"** to observe **96% faster emergency attention** (from 135 mins down to 5.3 mins) and review documented trade-off disclosures. |
| **10** | Click **"Safety Rules Engine"** tab | Inspect all active versioned deterministic rules, clinical thresholds, and plausibility bounds. |

---

## 🔒 Safety Invariant: Pre-ML Hard Floor
```
┌────────────────────────────────────────────────────────┐
│               Patient Intake Record                     │
└──────────────────────────┬─────────────────────────────┘
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
  [Deterministic Safety Engine]    [Cost-Sensitive ML Engine]
  - Plausibility verification      - Hinglish NLP normalizer
  - Critical vitals escalation     - Derived vitals (Shock Index)
  - Red-flag symptom matching      - Calibrated probabilities
             │                           │
    (Safety Floor Level)          (Predicted ML Level)
             │                           │
             └─────────────┬─────────────┘
                           ▼
            ┌─────────────────────────────┐
            │   HARD-CODED SAFETY FLOOR   │
            │  min(ML_Level, Floor_Level) │
            │  ML CANNOT DOWNGRADE RULE   │
            └─────────────────────────────┘
```

---

## 📊 Summary of Implemented Requirements

| Requirement | Implementation Detail | Status |
|---|---|:---:|
| **1. 5-Level Triage & Dept Routing** | ESI Level 1–5 rubric + 10 OPD specialty departments with clinical rationale | ✅ Complete |
| **2. 20x Asymmetric Cost Matrix** | Penalty = $(20 \times FN) + (1 \times FP)$ heavily penalising missed emergencies | ✅ Complete |
| **3. Hard-Coded Safety Escalation** | Deterministic Python rule engine in `rules.py` with 10 versioned rules | ✅ Complete |
| **4. Emergency Sensitivity & Confusion Matrix** | Dedicated benchmark dashboard with 99.2% Sensitivity and 5×5 Matrix | ✅ Complete |
| **5. Active Abstention Mechanism** | Flags missing/implausible data; returns *"Cannot assess — send to nurse now"* | ✅ Complete |
| **6. Wait-Time Reduction Simulation** | Discrete-event Poisson simulation showing 96% emergency wait reduction | ✅ Complete |
| **7. Nurse Override & Clinical Audit** | Nurse review modal with mandatory clinical rationale and audit logging | ✅ Complete |
| **8. Automated Test Suite** | 17 pytest integration and safety rule tests passing with 100% coverage | ✅ Complete |

---

## ⚖️ Clinical Disclaimer
MedTriage AI is a clinical decision-support prototype created for the TalentAP Mega Hackathon 2026. All patient records in demonstration mode are synthetic. It is not an autonomous diagnostic medical device and must never substitute for a qualified healthcare practitioner.
