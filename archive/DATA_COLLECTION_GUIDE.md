# 📊 Data Collection Guide - Manager Evaluation Platform

## 🎯 Overview
This guide specifies the **exact data requirements** for the AI-Driven Manager Evaluation Platform. Provide this to your research team for data collection.

## 👥 Target Managers (8 candidates)
1. **Roberto De Zerbi** (current Marseille, former Brighton)
2. **Mauricio Pochettino** (current USMNT, former Chelsea/Spurs)
3. **Thomas Frank** (current Brentford)
4. **Xavi Hernández** (current Barcelona, exit speculation)
5. **Kieran McKenna** (current Ipswich Town)
6. **Marco Silva** (current Fulham)
7. **Andoni Iraola** (current Bournemouth)
8. **Oliver Glasner** (current Crystal Palace)

---

## 📋 Required Data Points (18 KPIs per manager)

### **SECTION A: Tactical/Pressing Metrics**
**Source: Opta Sports / FBref**

| KPI | Description | Format | Example | Time Period |
|-----|-------------|---------|---------|-------------|
| `ppda` | Passes per defensive action (pressing intensity) | Decimal (1 dp) | `8.7` | Current season |
| `oppda` | Opposition passes allowed per defensive action | Decimal (1 dp) | `12.4` | Current season |
| `high_press_regains_90` | High press regains per 90 minutes | Decimal (1 dp) | `7.2` | Current season |

**Collection Instructions:**
- Use current 2024/25 season data up to **Sunday 09 June 2025**
- Include only league matches (Premier League/La Liga/etc.)
- If manager changed clubs mid-season, use data from current club only

---

### **SECTION B: Advanced Performance Metrics**
**Source: FBref / Basic Analytics**

| KPI | Description | Format | Example | Time Period |
|-----|-------------|---------|---------|-------------|
| `npxgd_90` | Non-penalty expected goals differential per 90 | Decimal (2 dp) | `+0.18` | Current season |
| `xg_per_shot` | Expected goals per shot average | Decimal (2 dp) | `0.12` | Current season |
| `xg_sequence` | Average xG per open-play sequence | Decimal (2 dp) | `0.09` | Current season |

**Collection Instructions:**
- Exclude penalties from xG calculations
- Use FBref's "Expected" section for xG data
- If xG_sequence unavailable, estimate from shots per sequence

---

### **SECTION C: Big Game Performance**
**Source: FBref / Manual calculation**

| KPI | Description | Format | Example | Time Period |
|-----|-------------|---------|---------|-------------|
| `big8_w` | Wins vs current "Big 8" teams | Integer | `3` | Current season |
| `big8_l` | Losses vs current "Big 8" teams | Integer | `5` | Current season |
| `big8_d` | Draws vs current "Big 8" teams | Integer | `2` | Current season |
| `ko_win_rate` | Cup knockout win percentage | Decimal (1 dp) | `68.5` | Last 3 seasons |

**Big 8 Teams Definition:**
- **Premier League**: Arsenal, Chelsea, Liverpool, Man City, Man United, Newcastle, Spurs, Aston Villa
- **La Liga**: Real Madrid, Barcelona, Atletico Madrid, Athletic Bilbao, Real Sociedad, Villarreal, Sevilla, Valencia
- **Other leagues**: Use top 8 teams by current league position

**Collection Instructions:**
- Only count completed matches up to cut-off date
- For ko_win_rate: Include FA Cup, EFL Cup, Champions League, Europa League
- If manager has <5 big games this season, use previous season data

---

### **SECTION D: Youth Development**
**Source: Club websites / Transfermarkt**

| KPI | Description | Format | Example | Time Period |
|-----|-------------|---------|---------|-------------|
| `u23_minutes_pct` | Percentage of league minutes given to U23 players | Decimal (1 dp) | `22.1` | Current season |
| `academy_debuts` | Number of academy players given debuts | Integer | `4` | Since manager appointment |

**Collection Instructions:**
- U23 = players under 23 at start of current season
- Academy = players who came through club's youth system
- Include only league matches for u23_minutes_pct
- Count debuts since manager's appointment at current club

---

### **SECTION E: Squad Management**
**Source: Premier Injuries / Club medical reports**

| KPI | Description | Format | Example | Time Period |
|-----|-------------|---------|---------|-------------|
| `injury_days_season` | Total player days lost to injury | Integer | `245` | Current season |
| `player_availability` | Squad availability percentage | Decimal (1 dp) | `84.2` | Current season average |

**Player Availability Calculation:**
```
player_availability = (1 - (injury_days_season / (squad_size × days_in_season))) × 100
```

**Collection Instructions:**
- Count only injuries preventing match selection
- Use premierinjuries.com or similar for injury data
- Squad size = registered first team squad (typically 25-28 players)
- Days in season = from season start to cut-off date

---

### **SECTION F: Transfer Market Performance**
**Source: Transfermarkt**

| KPI | Description | Format | Example | Time Period |
|-----|-------------|---------|---------|-------------|
| `squad_value_delta_m` | Squad market value change since appointment | Integer (£ millions) | `+120` | Since appointment |
| `net_spend_m` | Transfer net spend since appointment | Integer (£ millions) | `+85` | Since appointment |

**Collection Instructions:**
- Use Transfermarkt market values in **£ millions**
- Calculate delta from appointment date to current
- Net spend = purchases - sales (positive = net outlay)
- Convert from EUR to GBP if necessary (use current exchange rate)

---

### **SECTION G: Media & Relations**
**Source: Social media analysis / Manual tracking**

| KPI | Description | Format | Example | Time Period |
|-----|-------------|---------|---------|-------------|
| `fan_sentiment_pct` | Positive fan sentiment percentage | Decimal (1 dp) | `78.5` | Last 3 months |
| `media_vol_sigma` | Standard deviation of weekly headline count | Decimal (1 dp) | `2.1` | Last 6 months |

**Collection Instructions:**
- Fan sentiment: Use Twitter/Reddit sentiment analysis or fan polls
- Media volatility: Count headlines per week, calculate standard deviation
- Cut-off: Use data up to **Sunday 09 June 2025**

---

## 📝 Data Collection Template

### CSV Format Required (Exact 18 columns):

```csv
manager_name,ppda,oppda,high_press_regains_90,npxgd_90,xg_per_shot,xg_sequence,big8_w,big8_l,big8_d,ko_win_rate,u23_minutes_pct,academy_debuts,injury_days_season,player_availability,squad_value_delta_m,net_spend_m,fan_sentiment_pct,media_vol_sigma
Roberto De Zerbi,8.8,15.2,8.8,0.22,0.12,0.13,5,3,2,69.8,26.1,7,203,86.8,150,95,71.9,2.6
Mauricio Pochettino,,,,,,,,,,,,,,,,,
Thomas Frank,,,,,,,,,,,,,,,,,
Xavi Hernández,,,,,,,,,,,,,,,,,
Kieran McKenna,,,,,,,,,,,,,,,,,
Marco Silva,,,,,,,,,,,,,,,,,
Andoni Iraola,,,,,,,,,,,,,,,,,
Oliver Glasner,,,,,,,,,,,,,,,,,
```

## 🎯 Data Quality Requirements

### ✅ **Must Have (Critical)**
- All tactical metrics (PPDA, press regains)
- Big game record (wins/losses/draws)
- Transfer spend data (in £ millions)
- Basic injury/availability stats

### ⚠️ **Nice to Have (Use estimates if unavailable)**
- Advanced xG metrics (can estimate from basic stats)
- Fan sentiment (can use generic polling)
- Media volatility (can use manual count)

### 🔄 **Fallback Options**
- **Missing current season data**: Use previous season
- **Missing advanced metrics**: Use FBref equivalents
- **Missing sentiment data**: Use 50% neutral baseline
- **Missing historical data**: Use league averages

## 📤 Delivery Format

**Send completed data as:**
1. **CSV file**: `manager_data_real.csv` (using exact template format)
2. **Excel file**: With source notes for verification
3. **Documentation**: Notes on any estimates or missing data

**Timeline**: Data needed within **48 hours** (cut-off: Sunday 09 June 2025)

## 🔧 Integration Process

Once data is received:
1. Replace synthetic data in `generate_frozen_package.py`
2. Regenerate all visualizations and reports
3. Update social media content with real insights
4. Deploy updated platform

---

## 📞 Research Team Contacts

**Questions on data collection:**
- Tactical metrics: Contact FBref specialists
- Transfer data: Use Transfermarkt team (convert to £)
- Injury data: Premier Injuries or similar
- Media sentiment: Social media team

**Delivery method:** Email CSV + notes to project lead

---

**🚀 This real data will transform the platform from impressive demo to legitimate, viral-ready manager analysis tool.** 