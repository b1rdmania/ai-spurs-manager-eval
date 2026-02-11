# Spurs Manager Evaluation v2 (2026)

**Data-driven evaluation of 10 candidates for the Tottenham Hotspur manager position.**

Thomas Frank was sacked on Feb 11, 2026 after the worst PL win rate of any Spurs manager ever. Spurs sit 16th, 5 points above relegation. This tool uses a **Unified Final Scoring System** combining peer analysis with Spurs-specific fit modeling to identify the best candidate.

🔗 **[Live Dashboard](https://b1rdmania.github.io/ai-spurs-manager-eval/)** (GitHub Pages)

---

## Final Rankings (February 2026)

| Rank | Manager | Final Score | Peer | Fit | Potential | Available |
|------|---------|-------------|------|-----|-----------|-----------|
| 1 | **Xabi Alonso** | 85.3 | 9.3 | 84 | 73 | ✗ (Real Madrid) |
| 2 | **Andoni Iraola** | 71.2 | 6.8 | 63 | 89 | ✓ |
| 3 | **Roberto De Zerbi** | 65.7 | 6.1 | 80 | 52 | ✓ |
| 4 | **Kieran McKenna** | 62.6 | 5.9 | 58 | 75 | ✓ |
| 5 | **Xavi Hernandez** | 61.4 | 5.5 | 80 | 44 | ✓ |
| 6 | **Marco Silva** | 54.5 | 4.4 | 50 | 78 | ✓ |
| 7 | **Robbie Keane** | 45.0 | 2.9 | 35 | 87 | ✓ |
| 8 | **Mauricio Pochettino** | 38.3 | 2.7 | 33 | 64 | ✗ (USA World Cup) |
| 9 | **John Heitinga** | 32.8 | 1.3 | 25 | 79 | ✓ |
| 10 | **Oliver Glasner** | 32.7 | 1.9 | 24 | 70 | ✗ (Palace) |

---

## Scoring Methodology

### Unified Final Scoring Formula

```
Final Score = (Peer Score × 10 × 0.40) + (Spurs-Fit Total × 0.60)
Spurs-Fit Total = (Fit Index × 0.60) + (Potential Index × 0.40)
```

### Peer Analysis (40%)

Nine categories scored 0-10 against the peer group:
- **Pressing Intensity** (14%) — PPDA, high press regains, opponent PPDA
- **Attacking Quality** (14%) — npxGD/90, xG/shot, open play xG
- **Defensive Solidity** (12%) — xGA/90, player availability
- **Big Game Performance** (12%) — Big 6 record, knockout win rate
- **Youth Development** (10%) — U23 minutes %, academy debuts, youth progression
- **Squad Health** (9%) — Injury days, rotation index, availability
- **Transfer Acumen** (10%) — Squad value growth, net spend efficiency, sell-on profit
- **Media Stability** (9%) — Media volatility (sigma)
- **Stakeholder Alignment** (10%) — Fan sentiment, board backing

Each KPI is percentile-normalized within the peer group (no hard-coded thresholds).

### Spurs-Fit Index (60% within Spurs-Fit Total)

Four Spurs-specific benchmarks scored 0-25 each using **continuous sigmoid curves** (no binary pass/fail):
- **Front-Foot Play** — PPDA, npxGD/90, xG/shot (pressing intensity + attacking output)
- **Youth Pathway** — U23 minutes, academy debuts, youth progression
- **Talent Inflation** — Squad value growth, net spend efficiency, sell-on profit
- **Big Game Mentality** — Big 6 win %, knockout win rate, Big 6 xGD

### Potential Index (40% within Spurs-Fit Total)

Forward-looking assessment (0-100):
- **Age Factor** (20%) — Gaussian curve peaking at 43 (not 35)
- **Trend Score** (30%) — Season-over-season KPI improvements (npxGD, PPDA, league position)
- **Resource Leverage** (30%) — Overperformance vs squad budget (league finish vs squad value rank)
- **Temperament** (20%) — Calculated from touchline bans, public disputes, contract stability, mid-season departures

---

## Quick Start

### Prerequisites

- Python 3.12+
- pip

### Installation

```bash
git clone https://github.com/yourusername/ai-spurs-manager-eval.git
cd ai-spurs-manager-eval
pip install -r requirements.txt
```

### Run the Pipeline

```bash
python3 -m scripts.pipeline
```

This will:
1. Load and validate manager data from `data/managers.csv` and `data/managers_meta.csv`
2. Calculate peer scores, fit index, potential index, and final scores
3. Export `docs/data/scores.json` for the frontend

### View the Dashboard

Option 1: Open `docs/index.html` directly in a browser

Option 2: Serve locally:
```bash
python3 -m http.server --directory docs 8000
```
Then visit http://localhost:8000

### Run Tests

```bash
pytest tests/ -v
```

58 tests covering all scoring functions.

---

## Project Structure

```
.
├── data/
│   ├── managers.csv              # 10 managers × 22 KPIs
│   ├── managers_meta.csv         # Metadata (age, availability, temperament inputs)
│   └── kpi_definitions.yaml      # KPI documentation
│
├── config/
│   └── scoring.yaml              # Unified scoring config (categories, weights, sigmoid params)
│
├── scripts/
│   ├── data_loader.py            # CSV loading + validation
│   ├── peer_score.py             # 9-category peer analysis
│   ├── fit_index.py              # Spurs-Fit Index (sigmoid scoring)
│   ├── potential_index.py        # Potential Index (age, trend, leverage, temperament)
│   ├── unified_score.py          # Final score composition
│   ├── export_json.py            # Generate scores.json for frontend
│   └── pipeline.py               # Orchestrator
│
├── docs/                         # GitHub Pages frontend
│   ├── index.html                # Single-page app
│   ├── css/style.css             # Dark-mode Spurs theme
│   ├── js/
│   │   ├── app.js                # Main logic, table rendering
│   │   ├── charts.js             # Chart.js radar/bar charts
│   │   ├── compare.js            # Head-to-head comparison
│   │   ├── animations.js         # Scroll reveals, count-up
│   │   └── social.js             # Share card generation
│   └── data/
│       └── scores.json           # Generated by pipeline
│
├── tests/                        # pytest test suite (58 tests)
└── archive/                      # v1 files for reference
```

---

## Data Sources

- **Tactical/Attacking/Defensive**: FBref, StatsBomb, Understat
- **Financial/Transfers**: Transfermarkt
- **Squad Health**: Premier Injuries, Transfermarkt
- **Soft Metrics**: Fan polls, media analysis

All data from managers' most recent club management role (not national teams).

---

## Key Improvements from v1

### Model Fixes
- ✅ Removed duplicate peer categories (Squad Management, Adaptability, Board Harmony)
- ✅ Fixed "Defensive Solidity" to use actual defensive metrics (xGA) not just injuries
- ✅ Fixed age formula: now peaks at 43 (Gaussian), not 35 (linear)
- ✅ Replaced binary threshold cliffs in Fit Index with continuous sigmoid curves
- ✅ Formalized trend/temperament scores: calculated from observable data, not hand-waved
- ✅ Removed hard-coded ranking scores — all dynamic from data
- ✅ Calibrated benchmarks to data percentiles, not arbitrary absolutes

### Engineering
- ✅ Single unified config file (`config/scoring.yaml`) replacing 3 separate files
- ✅ Proper input validation with clear error messages
- ✅ Complete test suite (58 tests, all passing)
- ✅ Single pipeline orchestrator replacing 917-line monolith
- ✅ JSON-driven frontend (no hard-coded HTML table rows)

### Frontend
- ✅ Interactive Chart.js radars (not static PNGs)
- ✅ Head-to-head comparison mode with overlaid charts
- ✅ Sortable ranking table
- ✅ Animated score reveals (count-up on scroll)
- ✅ Shareable social cards (PNG download)
- ✅ Dark-mode Spurs branding throughout
- ✅ Mobile-responsive

---

## Contributing

This is a snapshot evaluation built in February 2026. To update with new data:

1. Edit `data/managers.csv` with new KPIs
2. Edit `data/managers_meta.csv` with updated metadata
3. Run `python3 -m scripts.pipeline`
4. Commit and push — GitHub Pages will auto-deploy

---

## License

MIT License — see [LICENSE](LICENSE)

---

## Acknowledgments

Built with [Claude Code](https://claude.com/claude-code) in February 2026.

Data sources: FBref, StatsBomb, Transfermarkt, Understat, Premier Injuries.

Inspired by the football analytics community and Spurs' need for a data-driven hiring process.

---

**COYS** 🤍💙
