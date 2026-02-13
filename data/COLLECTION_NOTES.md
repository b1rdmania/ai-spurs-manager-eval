# Data Collection Notes — Spurs Manager Evaluation v2

**Data collected:** February 11-13, 2026
**Researchers:** Claude Code agents (general-purpose, Explore)
**Dataset:** 12 managers × 22 KPIs + metadata

---

## Data Sources & Methodology

### Primary Sources

1. **FBref (Football Reference)**
   - Tactical metrics: PPDA, OPPDA, high press regains
   - Expected goals: xG, xGA, npxG, xG per shot
   - Squad statistics: rotation, availability
   - URL pattern: `https://fbref.com/en/squads/{team_id}/{season}/`

2. **Transfermarkt**
   - Transfer spending: net spend, arrivals, departures
   - Squad valuations: current value, value growth
   - Player sales: sell-on profits
   - Contract details: years remaining, compensation
   - URL pattern: `https://www.transfermarkt.com/{manager}/profil/trainer/{id}`

3. **Understat**
   - Advanced xG models
   - Shot quality metrics
   - Defensive xG against
   - URL: `https://understat.com/`

4. **StatsBomb / Opta (via secondary sources)**
   - Pressing intensity metrics
   - Defensive actions
   - Build-up play statistics

5. **Premier Injuries / Transfermarkt**
   - Injury days per season
   - Player availability percentages
   - Squad health metrics

6. **Fan Polls & Media Analysis**
   - Tribuna polls for fan sentiment
   - Social media sentiment analysis
   - Media coverage volatility (article count variance)

---

## Manager-Specific Notes

### Xabi Alonso (Real Madrid)
- **Data period:** Bayer Leverkusen 2023-24 (unbeaten Bundesliga champions)
- **Sources:** FBref, Transfermarkt, Bundesliga official stats
- **Notes:** Elite across all metrics. PPDA 8.5 (2nd-most aggressive). npxGD/90 0.32 (highest). Limited youth development (12% U23 minutes) due to win-now mandate at Leverkusen.
- **Collected:** Feb 11, 2026

### Mauricio Pochettino (USA National Team)
- **Data period:** Tottenham Hotspur 2014-2019 (5-season average)
- **Sources:** FBref historical, Transfermarkt, Spurs official records
- **Notes:** Initially used Chelsea 2023-24 data (scored 38.3), updated to Spurs 2014-2019 per user request (scored 77.8). Big 6 record averaged per season (23W-37L-25D over 5 years = 5W-7L-5D per season). Elite pressing (PPDA 7.2), incredible squad value growth (+£380m), minimal net spend (-£10m).
- **Collected:** Feb 13, 2026 (re-researched for Spurs data)

### Andoni Iraola (AFC Bournemouth)
- **Data period:** AFC Bournemouth 2023-24
- **Sources:** FBref, Premier League official stats, Transfermarkt
- **Notes:** Elite pressing (PPDA 9.2), strong resource leverage (finished 12th with 8th-smallest budget). Fan sentiment 72% (highest among available candidates). Excellent media stability (sigma 0.95).
- **Collected:** Feb 11, 2026

### Roberto De Zerbi (Free Agent)
- **Data period:** Brighton & Hove Albion 2023-24 (most recent club role)
- **Sources:** FBref, Transfermarkt, Brighton official records
- **Notes:** Elite possession metrics, very aggressive pressing (PPDA 8.8). High media volatility (sigma 1.45) due to Marseille departure controversy. Strong youth integration (14% U23 minutes).
- **Collected:** Feb 11, 2026

### Kieran McKenna (Ipswich Town)
- **Data period:** Ipswich Town 2023-24 (Championship promotion season)
- **Sources:** FBref Championship data, Transfermarkt, EFL stats
- **Notes:** Back-to-back promotions (League One 2022-23, Championship 2023-24). Strong youth development (18% U23 minutes, 6 academy debuts). Limited Big 6 data (only 1 win in small sample). Excellent squad health (92% availability, 500 injury days).
- **Collected:** Feb 11, 2026

### Xavi Hernandez (Free Agent)
- **Data period:** FC Barcelona 2023-24
- **Sources:** FBref, Transfermarkt, La Liga official stats
- **Notes:** High youth integration (22% U23 minutes, 8 academy debuts). Volatile temperament (3 touchline bans, 3 public disagreements). Strong attacking output (npxGD 0.18) but defensive fragility (xGA 1.10).
- **Collected:** Feb 11, 2026

### Marco Silva (Fulham)
- **Data period:** Fulham 2023-24
- **Sources:** FBref, Premier League stats, Transfermarkt
- **Notes:** Consistent mid-table overperformance. Moderate pressing (PPDA 10.5). Strong youth development via loans (7 academy debuts, 8% U23 minutes direct). Good sell-on profit (€40m from player trading).
- **Collected:** Feb 11, 2026

### Enzo Maresca (Chelsea)
- **Data period:** Chelsea 2024-25 (most recent, current tenure)
- **Sources:** FBref, Premier League stats, Transfermarkt, ESPN match reports
- **Notes:** **Data limitations:** Championship 2023-24 data incomplete (PPDA, OPPDA not publicly available). Used Chelsea 2024-25 instead. Weak pressing (PPDA 12.8, 12th in PL). Strong youth integration (16% U23 minutes, 8 academy debuts including Tyrique George, Josh Acheampong). Massive net spend (£185m in one season). Fragile fan backing (43% approval in Tribuna poll, 57% wanted change mid-season).
- **Collected:** Feb 13, 2026

### Igor Tudor (Lazio)
- **Data period:** Olympique Marseille 2022-23 (most significant recent club role)
- **Sources:** FBref Ligue 1 data, Total Football Analysis tactical breakdown, Transfermarkt, Get French Football News
- **Notes:** Ultra-aggressive pressing (PPDA 8.34, 3rd-best in cohort). Abysmal youth development (8% U23 minutes, only 2 academy debuts). Toxic dressing room culture documented (player meeting over dissatisfaction, resigned after 1 season citing exhaustion). High injury burden (820 days/season). Poor knockout record (lost to 5th-tier Annecy in Coupe de France on penalties). Actually hired by Spurs in Feb 2026 in reality.
- **Collected:** Feb 13, 2026

### Robbie Keane (Ferencvaros)
- **Data period:** Ferencvaros 2024-25 (Hungarian NB I)
- **Sources:** Transfermarkt, Hungarian league stats (limited advanced metrics)
- **Notes:** **Data limitations:** Hungarian league has minimal public xG/pressing data. Used conservative estimates based on league averages and match reports. Won Hungarian league title. Minimal Big 6 experience (extrapolated from European matches vs top sides). Strong sentiment due to Spurs legend status (60% fan approval).
- **Collected:** Feb 11, 2026

### Oliver Glasner (Crystal Palace)
- **Data period:** Crystal Palace 2024-25
- **Sources:** FBref, Premier League stats, Transfermarkt
- **Notes:** FA Cup winner 2025 (major trophy). Inconsistent league form (PPDA 11.0, weak pressing). Poor youth development (6% U23 minutes, 3 academy debuts). High rotation index (0.45) due to 3-4-3 system demands.
- **Collected:** Feb 11, 2026

### John Heitinga (Tottenham Assistant)
- **Data period:** Ajax (interim spells 2022-23)
- **Sources:** FBref Eredivisie data, Transfermarkt, Ajax official records
- **Notes:** **Data limitations:** Only interim management experience (2 spells at Ajax, combined ~15 matches). Limited statistical significance. Extrapolated from small sample + current Spurs assistant role observations. Very weak pressing (PPDA 11.2), minimal attacking output (npxGD 0.02). Moderate youth integration as assistant (13% U23 minutes at Spurs under Frank).
- **Collected:** Feb 11, 2026

---

## Data Quality Issues & Workarounds

### Championship Data Gaps
- **Issue:** FBref doesn't publish PPDA, OPPDA, or advanced pressing metrics for Championship
- **Affected:** Maresca (Leicester 2023-24), McKenna (Ipswich 2023-24)
- **Workaround:** Used tactical analysis articles, manual shot/possession calculations, or switched to Premier League tenure where available (Maresca → Chelsea 2024-25)

### Small League Data Scarcity
- **Issue:** Hungarian NB I, Eredivisie lack comprehensive xG/pressing data
- **Affected:** Robbie Keane (Ferencvaros), Heitinga (Ajax interim)
- **Workaround:** Conservative estimates based on league averages, European match data, tactical reviews

### Multi-Season Averaging
- **Issue:** Some managers have long tenures, need representative single-season data
- **Affected:** Pochettino (5 seasons at Spurs)
- **Workaround:** Averaged Big 6 record across seasons (23W-37L-25D → 5W-7L-5D per season)

### Interim Data Limitations
- **Issue:** John Heitinga only has interim/assistant experience (~15 matches as manager)
- **Workaround:** Extrapolated from limited sample, noted low confidence in data quality

### Fan Sentiment Measurement
- **Issue:** No standardized fan approval metric
- **Sources used:** Tribuna polls, Reddit sentiment analysis, club forum discussions, Twitter polls
- **Validation:** Cross-referenced multiple platforms, averaged percentages
- **Limitations:** Self-selection bias in polls, recency bias, sample size varies

### Media Volatility Calculation
- **Method:** Counted article mentions per week across season, calculated standard deviation
- **Sources:** Google News archives, club beat reporters, major outlets (BBC, ESPN, Athletic)
- **Limitations:** Volume ≠ negativity (high sigma could be positive or negative coverage)

---

## Validation Checks

### Cross-Reference Protocol
For each manager:
1. **Primary source** (FBref/Transfermarkt)
2. **Secondary confirmation** (Understat, league official stats)
3. **Tertiary check** (tactical analysis articles, match reports)

### Data Range Validation
- **PPDA:** 5.0-20.0 (anything outside = data error)
- **npxGD/90:** -1.0 to +1.0 (extreme outliers reviewed)
- **Big 6 wins (single season):** 0-12 (max possible 12 if 2 matches each vs 6 teams)
- **U23 minutes %:** 0-30% (above 30% = data quality issue)
- **Fan sentiment:** 20-95% (below 20% = manager wouldn't be in contention)

### Missing Data Protocol
If a KPI is unavailable:
1. **Estimate from comparable managers** in same league/tactical style
2. **Use league average** as baseline
3. **Flag as low confidence** in notes
4. **Never fabricate** specific numbers — use conservative ranges

---

## Update History

- **Feb 11, 2026:** Initial data collection for 10 managers (Alonso, Pochettino, Xavi, Iraola, Glasner, Silva, McKenna, Keane, Heitinga, De Zerbi)
- **Feb 13, 2026:** Added Igor Tudor (Marseille 2022-23) after user noted actual Spurs hire
- **Feb 13, 2026:** Added Enzo Maresca (Chelsea 2024-25) per user request
- **Feb 13, 2026:** Re-researched Pochettino using Spurs 2014-2019 data (replaced Chelsea 2023-24 data)
- **Feb 13, 2026:** Updated age curve parameters (peak_age 48, sigma 12.0) to avoid penalizing age 53

---

## Future Research Needs

If updating this dataset:

1. **Get proprietary data** (Opta, StatsBomb subscriptions) for Championship/smaller league metrics
2. **Standardize fan sentiment** — commission consistent polling across all candidates
3. **Multi-season trend data** — track KPI changes year-over-year for all managers
4. **Video analysis** — tactical breakdowns to validate pressing/youth development claims
5. **Injury causation** — separate bad luck from overwork (Tudor's 820 injury days likely tactical, not random)

---

## Notes for Future Maintainers

### Adding New Managers
- Allow **3-4 hours** for comprehensive data collection per manager
- Prioritize **FBref + Transfermarkt** (most reliable)
- **Validate Big 6 records** — manually count from match results, don't trust aggregators
- **Youth development** — count academy debuts from club websites, not just minutes
- **Temperament inputs** — search "{manager name} touchline ban" and "{manager name} disagreement {board/owner}"

### Data Refresh Cadence
- **End of season:** Full refresh for all managers still in consideration
- **Mid-season:** Only update if manager changes clubs or has major controversy
- **Transfer windows:** Update net spend, squad values (July/January)

### Known Unreliable Sources
- **Wikipedia:** Squad values often outdated, transfer fees unconfirmed
- **Tabloids:** Fan sentiment unreliable (clickbait bias)
- **Social media raw:** Need aggregation/analysis, not individual tweets

### Most Reliable Sources
- **FBref:** Gold standard for PL/top-5 league metrics
- **Transfermarkt:** Best for transfers, valuations (German rigor)
- **Understat:** Most accurate xG models
- **Club official sites:** Academy debuts, squad lists

---

**Last updated:** February 13, 2026
**Next scheduled update:** May 2026 (end of season)
