# TRL DEBATE ENGINE
## Frontend Demonstration & Production Operations Guide

> **Artifact Version:** 1.0.0  
> **Interface Identity:** "Folio" — Scientific Editorial × Research Adjudication Instrument  
> **Compliance Standard:** NASA / APCTT Technology Readiness Level (TRL 1–9)  
> **Frontend Architecture:** Zero-Dependency Handcrafted CSS/SVG/JS Single-File Client  
> **Server Integration:** FastAPI REST Service (`/apps/api/src/api/static/index.html`)

---

## 1. Executive Overview & Design Identity

The **TRL Debate Engine** frontend has been completely redesigned around **"Folio"**, an original design system rejecting generic dark dashboards, neon glow aesthetics, and repetitive card layouts in favor of an archival, scientific-editorial research instrument.

### Core Philosophy
1. **Typography Over Color**: Hierarchy is established first through scale, weight, and optical font sizing before color is applied.
2. **Restrained Chromatic Discipline**:
   - **Neutral Foundation**: Warm archival paper (`#F2EFE6`) in light mode / deep graphite (`#131311`) in dark mode.
   - **The Single Accent**: Vermilion measurement red (`#CF4520`) reserved strictly for active measurements, current TRL states, and critical warnings.
   - **Functional Agent Tints**: Pine (`#1D6B4C`) for The Optimist, Ochre (`#8C5A07`) for The Skeptic, Iris (`#2C3B8F`) for The Referee.
3. **Information-First Layouts**: Asymmetrical editorial sidehead grids, horizontal maturity progressions, and structured ledger tables replace floating cards and meaningless metric widgets.
4. **Zero-Dependency Resilience**: Pure HTML5, handcrafted responsive CSS, and native ES6 JavaScript without external build steps, framework dependencies, or CDN single-points-of-failure.

---

## 2. Architecture & Operational Boundary

```
┌────────────────────────────────────────────────────────────────────────┐
│                        FastAPI Application Gateway                     │
│               (uvicorn api.main:app --host 127.0.0.1 --port 8000)      │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
           ┌────────────────────────┴────────────────────────┐
           ▼                                                 ▼
┌──────────────────────────────┐              ┌───────────────────────────┐
│     REST API Endpoints       │              │    Static File Server     │
│  • GET  /api/health          │              │                           │
│  • GET  /api/trl-ladder      │              │  Serves:                  │
│  • GET  /api/sample-documents│              │  /api/static/index.html   │
│  • POST /api/sample-assess/* │              │  (Full "Folio" UI)        │
│  • POST /api/assess-text     │              └─────────────┬─────────────┘
│  • POST /api/assess (file)   │                            │
└──────────┬───────────────────┘                            │
           │                                                │
           ▼                                                ▼
┌────────────────────────────────────────────────────────────────────────┐
│                      Client-Side "Folio" Engine                        │
│                                                                        │
│  • Hash Router (#intake, #dossier, #debate, #determination, etc.)      │
│  • XSS-Immune Dynamic HTML Rendering via Tagged Escaping               │
│  • Real-Time Adversarial Debate Dialogue Visualizer                    │
│  • Horizontal 9-Stage TRL Maturity Scale Indicator                     │
│  • Interactive Evidence Explorer (Search, Category Filters, Meters)    │
│  • Local Assessment History Vault (localStorage persistence)           │
│  • Dual-Theme Switcher (Paper Archival / Graphite Dark)               │
└────────────────────────────────────────────────────────────────────────┘
```

### Route & View Mapping

| View ID | Hash Route | Description |
|---|---|---|
| **00** | `#intake` | Document upload, raw text input sheet, strict security toggle, quick-test papers. |
| **01** | `#dossier` | Document metadata, extraction telemetry, structural chunk stream, threat analysis. |
| **02** | `#debate` | Multi-agent adversarial arena: Optimist vs. Skeptic vs. Referee with round progression. |
| **03** | `#determination` | Official adjudicated TRL, maturity scale, satisfied vs. missing criteria, implied prerequisites audit, advancement roadmap. |
| **04** | `#evidence` | Granular technical claim ledger with category filters, search, and empirical strength meters. |
| **05** | `#analytics` | Research-oriented visualizations: category distribution, TRL spectrum placement, criteria progress, 25-dim ML feature vector heatmap. |
| **06** | `#history` | Locally persisted assessment archive with one-click reloading of historical runs. |
| **07** | `#framework` | Canonical NASA / APCTT 9-level matrix with mandatory checklists and operating environment thresholds. |

---

## 3. Step-by-Step Demonstration Script (For Juries & Stakeholders)

Use this structured walkthrough to deliver a 5-minute high-impact demonstration of the system's capabilities.

### Phase 1: Environment Launch & Health Inspection (0:30)
1. **Start the Engine**:
   ```powershell
   $env:PYTHONPATH = "packages/core/src;packages/document_processing/src;packages/ml_inference/src;packages/retrieval/src;packages/agent_orchestration/src;packages/competition_engine/src;apps/api/src;."
   python -m uvicorn api.main:app --host 127.0.0.1 --port 8000
   ```
2. Open `http://localhost:8000` in a modern browser.
3. **Inspect the System Health Drawer**:
   - In the left Index Rail, point out the **System** accordion at the bottom.
   - Click to expand: verify that all four engine layers (`document_processing`, `ml_inference`, `agent_orchestration`, `web_interface`) report active status.
4. **Theme Demonstration**:
   - Click the theme toggle icon (`themeBtn`) in the rail footer to show the transition between **Paper** (scientific journal) and **Graphite** (laboratory monitor).

---

### Phase 2: Instant Benchmark Adjudication (1:00)
1. Navigate to **`00 New Assessment`**.
2. Scroll to the **Quick test documents** section.
3. Click **Quantum Cascade Laser Sensor (Expected TRL 4)**:
   - Observe the full-screen **Processing Overlay** displaying *"Running adversarial debate… Extracting evidence, orchestrating agents, adjudicating TRL."*
   - Once completed, observe the automated navigation to **`03 TRL Determination`** and the green toast notification confirming `TRL 4 — 82.0% confidence`.

---

### Phase 3: Exploring the TRL Determination & Maturity Scale (1:15)
1. On the **`03 TRL Determination`** view, highlight the following original components:
   - **Horizontal Maturity Progression Scale**: Levels 1–3 are filled in ink (`mat-cell--met`), Level 4 is boldly highlighted in Vermilion (`mat-cell--now`), and Levels 5–9 remain quiet background cells (`mat-cell--future`).
   - **Maturity Verdict**: Point out the large typographic level `4`, the NASA-standard title (*"Technology validated in a laboratory"*), and the calibrated confidence score.
   - **Referee Justification**: Read the highlighted ruling proving empirical grounding in breadboard measurements.
   - **Criteria Verification**:
     - *Satisfied Criteria*: 3 laboratory criteria marked with solid glyphs (`●`).
     - *Missing Next-Level Gaps*: Environmental stress criteria required for TRL 5 clearly itemized (`○`).
     - *Implied Prerequisites Audit*: Show how foundational TRL 1–3 requirements were inferred as satisfied under the APCTT hierarchical rule because Level 4 breadboard testing was empirically verified.
   - **Advancement Roadmap**: Clear numbered engineering recommendations to reach TRL 5.

---

### Phase 4: Multi-Agent Adversarial Debate Inspection (1:00)
1. Click **`02 Debate Transcript`** in the Index Rail (or use running head links).
2. **Participant Stances**:
   - **The Optimist** (▲ Green): Advocates for TRL 5 based on demonstrated sensitivity claims.
   - **The Skeptic** (■ Ochre): Objects to premature advancement due to lack of environmental vibration/thermal stress testing.
   - **The Referee** (● Iris): Enforces strict criteria and adjudicates TRL 4.
3. **Transcript Accordions**:
   - Expand **Round 1 (Initial Claims & Boundary Audit)**: Show how agents cite actual excerpts from the document.
   - Expand **Round 2 (Rebuttal & Cross-Examination)**: Point out the debate regarding implied prerequisites vs. physical proof.
   - Expand **Round 3 (Referee Adjudication)**: Show the formal determination synthesizing the arguments.

---

### Phase 5: Evidence Ledger & Adversarial Security Test (1:15)
1. Click **`04 Evidence Explorer`**:
   - Demonstrate the real-time search: type `laser` or `methane` to filter claims.
   - Click category filter pills (e.g., `laboratory validation`, `experiment`) to isolate specific claim classes.
   - Point out the 3-bar strength meter (`meter[data-v="3"]`) showing empirical metrics detection.
2. Click **`00 New Assessment`** to demonstrate **Adversarial Security**:
   - Click the test document **Prompt Injection Attack (TRL 1)** with **Strict Security Mode OFF**:
     - Run assessment: The engine extracts the paper, flags `INSTRUCTION_OVERRIDE`, `SYSTEM_ROLE_HIJACK`, and `OUTPUT_FORCING`, neutralizes them in the sanitization filter, and awards the true evidence level (TRL 4/1) instead of the forced TRL 9.
   - Check **Strict Security Mode ON** and rerun:
     - The engine detects the threats and displays a critical **Security Alert** toast rejecting the document upfront, safeguarding backend inference.

---

## 4. Production Deployment Guidelines

### 4.1 System Prerequisites
- **Python**: `>= 3.10` (Tested on Python 3.10, 3.11, 3.12, 3.13, 3.14)
- **RAM**: Minimum 4 GB (8 GB recommended for PDF rasterization and embedding models)
- **Disk**: 500 MB for application and pre-trained model weights
- **OS**: Linux (Ubuntu 22.04 LTS / RHEL 9), macOS 13+, or Windows 10/11 / Windows Server 2022

### 4.2 Production Server Execution (Systemd / Linux)

Create a systemd service file at `/etc/systemd/system/trl-engine.service`:

```ini
[Unit]
Description=TRL Debate Engine FastAPI Server
After=network.target

[Service]
Type=simple
User=trlapp
Group=trlapp
WorkingDirectory=/opt/trl-debate-engine
Environment="PYTHONPATH=/opt/trl-debate-engine/packages/core/src:/opt/trl-debate-engine/packages/document_processing/src:/opt/trl-debate-engine/packages/ml_inference/src:/opt/trl-debate-engine/packages/retrieval/src:/opt/trl-debate-engine/packages/agent_orchestration/src:/opt/trl-debate-engine/packages/competition_engine/src:/opt/trl-debate-engine/apps/api/src:."
ExecStart=/opt/trl-debate-engine/.venv/bin/python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --workers 4 --proxy-headers --forwarded-allow-ips='*'
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable trl-engine
sudo systemctl start trl-engine
sudo systemctl status trl-engine
```

### 4.3 Production Reverse Proxy Configuration (NGINX)

Configure NGINX with WebSocket support, large file upload limits (for multi-page research PDFs), and standard security headers:

```nginx
server {
    listen 80;
    server_name trl-engine.yourdomain.org;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name trl-engine.yourdomain.org;

    ssl_certificate /etc/letsencrypt/live/trl-engine.yourdomain.org/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/trl-engine.yourdomain.org/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # PDF / Technical documentation upload ceiling (50MB)
    client_max_body_size 50M;

    # Security Headers
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self' https: data: 'unsafe-inline'; font-src 'self' https://fonts.gstatic.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;" always;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Extended timeouts for deep multi-agent debate pipelines
        proxy_read_timeout 180s;
        proxy_connect_timeout 60s;
    }
}
```

### 4.4 Docker Containerization

To run the application inside a container, use the following `Dockerfile`:

```dockerfile
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH="packages/core/src:packages/document_processing/src:packages/ml_inference/src:packages/retrieval/src:packages/agent_orchestration/src:packages/competition_engine/src:apps/api/src:."

WORKDIR /app

# Install system dependencies for PDF parsing
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./
COPY packages/ ./packages/
COPY apps/ ./apps/

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

CMD ["python", "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t trl-debate-engine:latest .
docker run -d --name trl-engine -p 8000:8000 trl-debate-engine:latest
```

---

## 5. Security & Data Integrity Protocol

1. **Untrusted Content Encapsulation**:
   - Uploaded text documents pass through `sanitize_text()`. Dangerous zero-width unicode characters (`\u200B`, `\uFEFF`, etc.) and directional overrides are stripped immediately.
   - Dynamic user content injected into the DOM is rigorously escaped via the `html` tagged template function, preventing Stored or Reflected Cross-Site Scripting (XSS).
2. **Prompt Injection Defense**:
   - The engine recognizes instruction overrides, system role hijacks, roleplay jailbreaks, and output-forcing patterns.
   - In standard mode, threats are neutralized and flagged. In strict mode, the document is rejected with `strict_mode_blocked: true`.
3. **Client-Side History Privacy**:
   - Assessment history is stored in the user's browser `localStorage` under `trlde.history`. No user document content is sent to third-party trackers or external analytics servers.

---

## 6. Keyboard Shortcuts & Accessibility Reference

The "Folio" interface adheres to WCAG 2.1 AA accessibility guidelines:

| Action / Control | Keybinding | Expected Behavior |
|---|---|---|
| **Skip to Main Content** | `Tab` (on initial load) | Focuses the hidden accessible skip link and jumps directly to `<main id="main">`. |
| **Section Navigation** | `Alt + 0` through `Alt + 7` | Switches directly between sections 00 to 07. |
| **History Navigation** | `Enter` / `Space` | When focused on an entry in `06 History`, immediately reloads the full assessment. |
| **Dialog Dismissal** | `Escape` | Closes the JSON export dialog or mobile navigation rail. |
| **Contrast Compliance** | Native Styles | Text-to-background contrast ratios strictly maintain $\ge 4.5:1$ for body text and $\ge 3:1$ for large display headings across both Paper and Graphite themes. |

---

## 7. Troubleshooting & Operator FAQ

### Q1: The server starts but reports `Port 8000 is already in use`
**Resolution:**
Terminate the existing process or bind to a custom port:
```powershell
# Windows
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process -Force
# Or launch on alternative port:
python -m uvicorn api.main:app --host 127.0.0.1 --port 8080
```

### Q2: Why are some lower-level TRL criteria marked as "Implied" instead of "Missing"?
**Resolution:**
This reflects the official NASA / APCTT **Implied Prerequisites Rule**. If a technology provides verifiable empirical evidence of high-fidelity integrated testing in a laboratory or relevant environment (TRL $\ge$ 4), basic preliminary theoretical paper studies (TRL 1–2) are logically inferred as satisfied even if the historical lab notes were not published in the current paper.

### Q3: How do I export assessment data for audit reports?
**Resolution:**
Click the **Export JSON** download icon in the running head or press the export button in the dossier. The resulting JSON file contains the full verifiable cryptographic trace, chunk provenance, feature vectors, debate transcript turns, and referee adjudication.

---

*Document compiled for the 2nd APCTT Hackathon 2026 / Techfest 2026-27 submission package.*
