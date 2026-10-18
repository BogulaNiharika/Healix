# 🚀 MedTriage AI — Production Deployment Guide
**Architecture: Frontend on Vercel + Backend on Render / Railway**

This guide walks you through deploying MedTriage AI with decoupled architecture:
- **Backend API**: Hosted on **Render** (free tier) or **Railway** (free trial)
- **Frontend SPA**: Hosted on **Vercel** (free global edge CDN)

---

## 📋 Pre-Deployment Summary of Prepared Files

All necessary deployment configurations are pre-configured:
1. [`requirements.txt`](file:///c:/Users/Bogula%20Niharika/OneDrive/Desktop/Health%20opd/requirements.txt) — Root Python dependencies for cloud build packs.
2. [`Procfile`](file:///c:/Users/Bogula%20Niharika/OneDrive/Desktop/Health%20opd/Procfile) — Declares web process command `uvicorn backend.app.main:app`.
3. [`render.yaml`](file:///c:/Users/Bogula%20Niharika/OneDrive/Desktop/Health%20opd/render.yaml) — Render Blueprint for 1-click infrastructure deployment.
4. [`railway.json`](file:///c:/Users/Bogula%20Niharika/OneDrive/Desktop/Health%20opd/railway.json) — Railway build & healthcheck configuration.
5. [`Dockerfile`](file:///c:/Users/Bogula%20Niharika/OneDrive/Desktop/Health%20opd/Dockerfile) & [`.dockerignore`](file:///c:/Users/Bogula%20Niharika/OneDrive/Desktop/Health%20opd/.dockerignore) — Multi-stage production container setup.
6. [`frontend/vercel.json`](file:///c:/Users/Bogula%20Niharika/OneDrive/Desktop/Health%20opd/frontend/vercel.json) & [`vercel.json`](file:///c:/Users/Bogula%20Niharika/OneDrive/Desktop/Health%20opd/vercel.json) — SPA routing rewrites.
7. [`frontend/src/services/api.ts`](file:///c:/Users/Bogula%20Niharika/OneDrive/Desktop/Health%20opd/frontend/src/services/api.ts) — Configured to dynamically consume `VITE_API_BASE_URL`.
8. [`backend/app/main.py`](file:///c:/Users/Bogula%20Niharika/OneDrive/Desktop/Health%20opd/backend/app/main.py) — CORS updated to accept `https://*.vercel.app` domains automatically.

---

## Step 1: Push Project to GitHub

If your repository isn't already pushed to GitHub:
```bash
git init
git add .
git commit -m "feat: complete MedTriage AI deployment setup"
git branch -M main
git remote add origin https://github.com/<YOUR_USERNAME>/<YOUR_REPO>.git
git push -u origin main
```

---

## Step 2: Deploy Backend (Choose Option A or Option B)

### Option A: Deploy on Render (Recommended Free Tier)
1. Go to [render.com](https://render.com) and log in with GitHub.
2. Click **New +** → **Web Service**.
3. Select your repository `Health opd` (or `MedTriage`).
4. Configure the settings:
   - **Name:** `medtriage-backend` (or your choice)
   - **Region:** Any (e.g., Oregon or Frankfurt)
   - **Branch:** `main`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free
5. Under **Environment Variables**, add:
   - `ENVIRONMENT` = `production`
   - `DEBUG` = `false`
   - `PYTHON_VERSION` = `3.11.9`
6. Click **Create Web Service**.
7. Once deployed, copy your backend URL:
   `https://medtriage-backend.onrender.com`
8. Verify it by visiting `https://medtriage-backend.onrender.com/health` in your browser. It should return:
   ```json
   {"status":"healthy","service":"MedTriage AI","version":"1.0.0","safety_engine":"active"}
   ```

### Option B: Deploy on Railway
1. Go to [railway.app](https://railway.app) and sign in.
2. Click **New Project** → **Deploy from GitHub repo**.
3. Select your repository.
4. Railway will automatically detect [`railway.json`](file:///c:/Users/Bogula%20Niharika/OneDrive/Desktop/Health%20opd/railway.json) / [`Procfile`](file:///c:/Users/Bogula%20Niharika/OneDrive/Desktop/Health%20opd/Procfile).
5. In **Settings** → **Networking**, click **Generate Domain** to get your public URL (e.g., `https://medtriage-production.up.railway.app`).

---

## Step 3: Deploy Frontend on Vercel

1. Go to [vercel.com](https://vercel.com) and log in with GitHub.
2. Click **Add New...** → **Project**.
3. Select your repository.
4. In the **Configure Project** screen:
   - **Framework Preset:** `Vite`
   - **Root Directory:** Click *Edit* and select `frontend` *(or leave default if deploying via root vercel.json)*
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
5. Expand **Environment Variables** and add:
   | Key | Value | Description |
   |---|---|---|
   | `VITE_API_BASE_URL` | `https://medtriage-backend.onrender.com` | Your backend URL from Step 2 |
6. Click **Deploy**.
7. In ~30 seconds, your site will be live at `https://<project-name>.vercel.app`!

---

## Step 4: Verification & Smoke Test Checklist

Open your live Vercel URL in your browser:
- [ ] **Home Page:** Ensure landing page loads and KPI numbers appear.
- [ ] **Login:** Sign in with `nurse` / `nurse123`.
- [ ] **Patient Intake & Triage:** Test a preset like *"🚨 STEMI / Cardiac Shock (L2)"*. Confirm the AI triage prediction renders with clinical explanations.
- [ ] **Safety Rules Engine:** Verify hard-coded clinical floors trigger correctly without ML downgrade.
- [ ] **Nurse Review / Override:** Test overriding a priority level with mandatory nurse notes.
- [ ] **Model Evaluation & Wait-Time Simulation:** Verify the 5×5 confusion matrix and discrete-event queue simulation run live.
