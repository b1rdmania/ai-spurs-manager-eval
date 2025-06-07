# 🚀 Deployment Guide - Spurs Manager Evaluation

## Quick Deploy (5 minutes)

### 1. Create GitHub Repository
```bash
# Create new public repo: ai-spurs-manager-eval
# Upload entire /deliverables folder to repo root
```

### 2. Enable GitHub Pages
- Go to repo Settings > Pages
- Source: Deploy from a branch
- Branch: main
- Folder: /docs
- Save

### 3. Get URLs and Shorten
```
Main site: https://USERNAME.github.io/ai-spurs-manager-eval/
Repo: https://github.com/USERNAME/ai-spurs-manager-eval
```

Use bit.ly to create:
- Main site shortlink
- Repo shortlink  
- PDF shortlinks (one per manager)

### 4. Tweet Schedule

Copy from `assets/tweets.txt`:

**Day 1 - Launch**
1. Pin intro thread tweet
2. Post poll tweet
3. Reply to poll with repo link

**Day 2-3 - Manager Profile Tweets**
Post every 12 minutes during peak hours (9am-6pm GMT):
- De Zerbi (7.5/10) 
- Pochettino (7.4/10)
- Frank (7.2/10)
- Xavi (6.9/10)
- Glasner (6.8/10)
- McKenna (6.8/10)
- Silva (6.6/10)
- Iraola (6.4/10)

Each tweet includes:
- Manager bio/stats
- PDF link (shortened)
- Repo link (shortened)
- Relevant hashtags

## File Structure
```
/deliverables/
├── data/
│   ├── kpi_merged.csv      # Raw 18-KPI data
│   └── scores_12cat.csv    # Category scores + fit scores
├── reports/
│   ├── *.md               # Markdown source files
│   └── README_how_to_regen.md
├── assets/
│   ├── *_radar.png        # Individual radar charts
│   ├── score_matrix.png   # Summary heatmap
│   └── tweets.txt         # All tweet content
└── docs/                  # GitHub Pages site
    ├── index.html
    └── scores.json
```

## Emergency Updates

To update any manager's data:
1. Edit `data/kpi_merged.csv`
2. Re-run scoring: `python generate_frozen_package.py`
3. Push to GitHub (auto-deploys)

## Success Metrics
- GitHub stars/forks
- Tweet engagement rates
- Site traffic (Google Analytics)

---
**Total deployment time: < 30 minutes**
**Ongoing maintenance: Zero**
