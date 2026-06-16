<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=700&size=28&pause=1000&color=B87333&center=true&vCenter=true&width=700&lines=Quality+Engineering+Analyzer;Statistical+Process+Control+%7C+SPC;Cp+%2F+Cpk+%7C+X%CC%84-bar+%7C+R+Chart" alt="Typing SVG" />

<br/>

<!-- Copper/Bronze badge row -->
<img src="https://img.shields.io/badge/Version-1.0.0-B87333?style=for-the-badge&logoColor=white" />
<img src="https://img.shields.io/badge/Python-3.11+-B87333?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/Flask-3.0.3-B87333?style=for-the-badge&logo=flask&logoColor=white" />
<img src="https://img.shields.io/badge/License-MIT-B87333?style=for-the-badge" />
<img src="https://img.shields.io/badge/Mobile-First-B87333?style=for-the-badge&logo=android&logoColor=white" />

<br/><br/>

<img src="https://img.shields.io/badge/Created%20by-ENG--2518885-8B4513?style=flat-square&logoColor=white" />
<img src="https://img.shields.io/badge/Email-meharibrhanu233%40gmail.com-CD7F32?style=flat-square&logo=gmail&logoColor=white" />
<img src="https://img.shields.io/badge/Profession-Mechanical%20Engineer-A0522D?style=flat-square" />

<br/><br/>

> **A production-ready hybrid mobile web application for Statistical Quality Control.**  
> Built with Python Flask · Powered by NumPy, SciPy, Pandas · Visualized with Chart.js

<br/>

[![GitHub repo](https://img.shields.io/badge/GitHub-brhanumehari%2Fquality__analysis--app-B87333?style=for-the-badge&logo=github&logoColor=white)](https://github.com/brhanumehari/quality_analysis-_app)

</div>

---

<div align="center">
<h2>
<span style="color:#B87333">⬡</span> &nbsp;
<span>Q U A L I T Y &nbsp; E N G I N E E R I N G &nbsp; A N A L Y Z E R</span>
&nbsp; <span style="color:#B87333">⬡</span>
</h2>
</div>

```
╔══════════════════════════════════════════════════════════════╗
║  ██████╗ ███████╗     █████╗ ███╗   ██╗ █████╗ ██╗  ██╗    ║
║ ██╔═══██╗██╔════╝    ██╔══██╗████╗  ██║██╔══██╗██║  ██║    ║
║ ██║   ██║█████╗      ███████║██╔██╗ ██║███████║███████║    ║
║ ██║▄▄ ██║██╔══╝      ██╔══██║██║╚██╗██║██╔══██║██╔══██║    ║
║ ╚██████╔╝███████╗    ██║  ██║██║ ╚████║██║  ██║██║  ██║    ║
║  ╚══▀▀═╝ ╚══════╝    ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝    ║
║                                                              ║
║         Statistical Quality Control · SPC · Cp/Cpk          ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Quick Start — Linux / macOS](#-quick-start--linux--macos)
- [Quick Start — Windows](#-quick-start--windows)
- [🤖 Run on Android — Termux](#-run-on-android--termux)
- [API Reference](#-api-reference)
- [Statistical Methods](#-statistical-methods)
- [Screenshots / Usage](#-screenshots--usage)
- [Push to GitHub](#-push-to-github)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🔶 Overview

The **Quality Engineering Analyzer** is a mobile-first, single-page web application that brings industrial-grade statistical quality control to any device — including Android smartphones running **Termux**. It computes process capability indices, renders SPC control charts, and fits normal distribution curves — all through a clean dark-mode dashboard optimized for touchscreen use.

**Who is this for?**
- Mechanical & Manufacturing Engineers performing shop-floor quality checks
- Quality Assurance teams running SPC analysis on measurement data
- Students and researchers learning Statistical Process Control

---

## ✨ Features

| Feature | Details |
|---|---|
| 📊 **Descriptive Statistics** | Mean, Median, Std Dev, Variance, Range, N, Skewness, Kurtosis |
| 🎯 **Process Capability** | Cp, Cpk, Cpu, Cpl — with yield % and plain-language rating |
| 📈 **X̄-bar Chart** | Subgroup means with UCL, LCL, Center Line — out-of-control highlighting |
| 📉 **R Chart** | Subgroup ranges with control limits and OOC detection |
| 🔔 **Histogram + Normal Fit** | Interactive bar chart with overlaid normal distribution curve |
| 📁 **CSV Upload** | Drag-and-drop CSV file ingestion |
| ✏️ **Manual Entry** | Comma/newline separated values typed directly |
| 🧪 **Sample Datasets** | 3 built-in demo datasets (Bearing, Shaft, Torque) |
| 📱 **Mobile-First** | Touch-optimized layout, runs on phone browser |
| 🔌 **REST API** | Clean JSON API consumable from any client |

---

## 🛠 Tech Stack

```
┌─────────────────────────────────────────────────────┐
│  BACKEND                     FRONTEND               │
│  ─────────────────────       ──────────────────     │
│  Python 3.11+                HTML5 / CSS3           │
│  Flask 3.0.3                 Tailwind CSS (CDN)     │
│  NumPy 1.26.4                Chart.js 4.4.0 (CDN)  │
│  SciPy 1.13.1                Native Fetch API       │
│  Pandas 2.2.2                JetBrains Mono Font    │
└─────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
quality_analysis-_app/
│
├── app.py                  ← Flask REST API backend
│   ├── POST /api/analyze   ← Main analysis endpoint
│   ├── GET  /              ← Serves the mobile dashboard
│   └── GET  /api/health    ← Health check
│
├── templates/
│   └── index.html          ← Single-page mobile dashboard (SPA)
│
├── requirements.txt        ← Pinned Python dependencies
├── setup.sh                ← Automated setup & launch script
└── README.md               ← You are here
```

---

## 🚀 Quick Start — Linux / macOS

### Option A — Automated (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/brhanumehari/quality_analysis-_app.git
cd quality_analysis-_app

# 2. Give the script execute permission
chmod +x setup.sh

# 3. Run — it does everything automatically
./setup.sh
```

The script will:
- ✅ Check Python 3 + pip
- ✅ Create `.venv` virtual environment
- ✅ Install all dependencies
- ✅ Validate the Flask app for syntax errors
- ✅ Detect your local network IP
- ✅ Launch the server and print your mobile URL

### Option B — Manual

```bash
git clone https://github.com/brhanumehari/quality_analysis-_app.git
cd quality_analysis-_app

python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

flask run --host=0.0.0.0 --port=5000
```

Then open **http://127.0.0.1:5000** in your browser.

---

## 🪟 Quick Start — Windows

```powershell
# 1. Clone the repo
git clone https://github.com/brhanumehari/quality_analysis-_app.git
cd quality_analysis-_app

# 2. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Launch
set FLASK_APP=app.py
flask run --host=0.0.0.0 --port=5000
```

---

## 🤖 Run on Android — Termux

> Run the full Flask server directly on your Android phone — **no PC required**.

### Step 1 · Install Termux

Download **Termux** from F-Droid (recommended — Play Store version is outdated):

```
https://f-droid.org/en/packages/com.termux/
```

> ⚠️ Do **not** use the Google Play Store version of Termux — it is no longer maintained and will fail to install packages.

---

### Step 2 · Update Termux Packages

Open Termux and run:

```bash
pkg update && pkg upgrade -y
```

---

### Step 3 · Install Python and Git

```bash
pkg install python git -y
```

Verify installation:

```bash
python --version    # Should show Python 3.11+
git --version
pip --version
```

---

### Step 4 · Install Required Build Tools

Some Python packages need native compilation tools:

```bash
pkg install build-essential libffi openssl -y
pip install --upgrade pip setuptools wheel
```

---

### Step 5 · Clone the Repository

```bash
cd ~
git clone https://github.com/brhanumehari/quality_analysis-_app.git
cd quality_analysis-_app
```

---

### Step 6 · Install Python Dependencies

> In Termux, we install directly without a virtual environment (Termux manages its own isolated environment).

```bash
pip install flask==3.0.3 numpy==1.26.4 pandas==2.2.2 scipy==1.13.1
```

If `scipy` fails to install from PyPI, use the Termux-optimized scientific stack:

```bash
pkg install python-numpy python-scipy -y
pip install flask==3.0.3 pandas==2.2.2
```

---

### Step 7 · Launch the Flask Server

```bash
cd ~/quality_analysis-_app
python app.py
```

Or use Flask CLI:

```bash
export FLASK_APP=app.py
flask run --host=0.0.0.0 --port=5000
```

You will see output like:

```
 * Running on http://0.0.0.0:5000
 * Running on http://192.168.x.x:5000
```

---

### Step 8 · Open in Your Phone Browser

Open your Android browser (Chrome, Firefox, etc.) and go to:

```
http://127.0.0.1:5000
```

Or to share with other devices on the same Wi-Fi:

```
http://<YOUR_PHONE_IP>:5000
```

Find your phone's IP with:

```bash
ip addr show wlan0 | grep 'inet '
```

---

### Step 9 · Keep it Running (Optional)

To keep the server running when you close Termux, use **tmux**:

```bash
pkg install tmux -y
tmux new -s qeapp
cd ~/quality_analysis-_app
python app.py
# Press Ctrl+B then D to detach
# Reattach later: tmux attach -t qeapp
```

---

### 📋 Termux Complete One-Liner Setup

Copy and paste this entire block into Termux:

```bash
pkg update -y && \
pkg install python git build-essential -y && \
pip install --upgrade pip && \
git clone https://github.com/brhanumehari/quality_analysis-_app.git && \
cd quality_analysis-_app && \
pip install flask numpy pandas scipy && \
python app.py
```

---

### ⚠️ Termux Troubleshooting

| Problem | Solution |
|---|---|
| `scipy` install fails | `pkg install python-scipy -y` |
| `numpy` mismatch | `pkg install python-numpy -y` |
| Port 5000 in use | `flask run --port=8080` |
| `git clone` fails | `pkg install openssh -y` |
| Slow install | Run on Wi-Fi, not mobile data |
| `FLASK_APP` not found | Run from inside the project folder |

---

## 📡 API Reference

### `POST /api/analyze`

**Request Body (JSON):**

```json
{
  "data": [10.1, 10.3, 9.9, 10.2, 10.4],
  "usl": 10.5,
  "lsl": 9.5,
  "subgroup_size": 5
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `data` | `float[]` | ✅ Yes | Array of measurement values (min 2) |
| `usl` | `float` | ❌ Optional | Upper Specification Limit |
| `lsl` | `float` | ❌ Optional | Lower Specification Limit |
| `subgroup_size` | `int` | ❌ Optional | SPC subgroup size, default `5` (range 2–10) |

**Response (JSON):**

```json
{
  "status": "success",
  "descriptive_stats": {
    "mean": 10.18,
    "median": 10.20,
    "std_dev": 0.1924,
    "variance": 0.037,
    "data_range": 0.5,
    "sample_size": 5,
    "min_val": 9.9,
    "max_val": 10.4,
    "skewness": -0.123,
    "kurtosis": -1.452
  },
  "capability": {
    "cp": 1.73,
    "cpk": 1.52,
    "cpu": 1.94,
    "cpl": 1.52,
    "sigma": 0.1924,
    "yield_pct": 99.9914,
    "ppk_rating": "Capable"
  },
  "spc_charts": {
    "x_bar_chart": { "ucl": 10.51, "lcl": 9.87, "center_line": 10.18, "data_points": [...] },
    "r_chart":     { "ucl": 0.62,  "lcl": 0.00, "center_line": 0.29,  "data_points": [...] }
  },
  "histogram_data": {
    "bin_centers": [...],
    "frequencies": [...],
    "normal_curve": { "x": [...], "y": [...] }
  }
}
```

### `GET /api/health`

```json
{ "status": "healthy", "version": "1.0.0" }
```

---

## 📐 Statistical Methods

### Descriptive Statistics

| Statistic | Formula |
|---|---|
| Mean | $\bar{X} = \frac{1}{n}\sum_{i=1}^{n} x_i$ |
| Sample Std Dev | $s = \sqrt{\frac{\sum(x_i - \bar{X})^2}{n-1}}$ |
| Variance | $s^2$ |

### Process Capability

| Index | Formula | Target |
|---|---|---|
| Cp | $(USL - LSL) / (6\sigma)$ | ≥ 1.33 |
| Cpk | $\min(Cpu, Cpl)$ | ≥ 1.33 |
| Cpu | $(USL - \bar{X}) / (3\sigma)$ | — |
| Cpl | $(\bar{X} - LSL) / (3\sigma)$ | — |

### SPC Control Limits (X̄-bar & R Chart)

Uses standard Shewhart constants (A₂, D₃, D₄) per subgroup size:

| Limit | Formula |
|---|---|
| UCL (X̄) | $\bar{\bar{X}} + A_2 \cdot \bar{R}$ |
| LCL (X̄) | $\bar{\bar{X}} - A_2 \cdot \bar{R}$ |
| UCL (R)  | $D_4 \cdot \bar{R}$ |
| LCL (R)  | $D_3 \cdot \bar{R}$ |

---

## 📄 License

```
MIT License

Copyright (c) 2025 ENG-2518885 — Mehari Brhanu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
```

---

<div align="center">

```
╔══════════════════════════════════════════════════════╗
║                                                      ║
║   Created with precision by ENG-2518885              ║
║   Mehari Brhanu · Mechanical Engineer                ║
║   meharibrhanu233@gmail.com                          ║
║                                                      ║
║   "Quality is not an act — it is a habit."           ║
║                              — Aristotle             ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
```

<img src="https://img.shields.io/badge/Made%20with-Python-B87333?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/For-Quality%20Engineers-8B4513?style=for-the-badge" />
<img src="https://img.shields.io/badge/Runs%20on-Android%20Termux-CD7F32?style=for-the-badge&logo=android&logoColor=white" />

<br/><br/>

**⭐ Star this repo if it helped your quality work!**

[![GitHub stars](https://img.shields.io/github/stars/brhanumehari/quality_analysis-_app?color=B87333&style=for-the-badge&logo=github)](https://github.com/brhanumehari/quality_analysis-_app/stargazers)

</div>
