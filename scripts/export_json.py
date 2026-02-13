"""Export scored data as JSON for the frontend."""

import json
from pathlib import Path
import pandas as pd


# Manager narratives — tagline, summary, strengths, concerns, verdict
NARRATIVES = {
    "roberto-de-zerbi": {
        "tagline": "The Technical Perfectionist",
        "summary": "Elite possession-based philosophy honed at Sassuolo and Brighton, praised by Guardiola as one of the most influential coaches around. Left Marseille by mutual consent. His Brighton side played some of the most progressive football in PL history.",
        "strengths": ["Exceptional tactical detail and game model clarity", "Proven ability to overperform with limited budgets", "Developed multiple players into international-calibre talent"],
        "concerns": ["Temperamental — clashed with Marseille hierarchy", "Defensive fragility in big games", "Short tenure at multiple clubs"],
        "verdict": "STRONGLY RECOMMENDED"
    },
    "mauricio-pochettino": {
        "tagline": "The Prodigal Son",
        "summary": "Spurs legend who built the club's greatest modern era (2014-2019), reaching the Champions League final. Currently committed to USA for the 2026 World Cup. The emotional favourite but unavailable until July.",
        "strengths": ["Deep understanding of Spurs culture and DNA", "Proven PL track record building elite teams from scratch", "Elite player development — Kane, Son, Alli all peaked under him"],
        "concerns": ["Unavailable until after World Cup (July 2026)", "Question marks about whether the magic can be recaptured", "Struggled at PSG and had mixed results at Chelsea"],
        "verdict": "RECOMMENDED (SUMMER OPTION)"
    },
    "xavi-hernandez": {
        "tagline": "The Barcelona Blueprint",
        "summary": "One of football's greatest midfielders turned manager. Revitalised Barcelona's style and won La Liga, but struggled with inconsistency and reported dressing room issues. Publicly open to PL management.",
        "strengths": ["Absolute commitment to possession and positional play", "Excellent youth integration at Barcelona", "Name recognition and global profile"],
        "concerns": ["Volatile temperament — multiple touchline incidents", "Only managed in one system (Barcelona)", "Questions about adaptation to PL pace and physicality"],
        "verdict": "RECOMMENDED WITH RESERVATIONS"
    },
    "andoni-iraola": {
        "tagline": "The Bournemouth Builder",
        "summary": "Guided Bournemouth to their best-ever PL finishes with a fraction of the top-6 budget. Pressing-based system with exceptional tactical flexibility. Draws comparisons to a young Pochettino.",
        "strengths": ["Outstanding resource leverage — elite overperformance", "Modern pressing system highly adaptable", "Excellent man-management and player development"],
        "concerns": ["Unproven at a top-6 club", "Would require compensation from Bournemouth", "Step up in expectations and scrutiny"],
        "verdict": "STRONGLY RECOMMENDED"
    },
    "oliver-glasner": {
        "tagline": "The Cup Specialist",
        "summary": "Won the FA Cup with Crystal Palace in 2025 and previously the Europa League with Eintracht Frankfurt. Known for his high-energy 3-4-3 system and ability to galvanise squads quickly.",
        "strengths": ["Proven cup competition pedigree", "Energetic, high-pressing tactical system", "Quick turnaround specialist — transforms results fast"],
        "concerns": ["PL league form has been inconsistent", "Rigid tactical approach may limit squad options", "Has confirmed commitment to Palace for this season"],
        "verdict": "CAUTIOUSLY RECOMMENDED"
    },
    "marco-silva": {
        "tagline": "The Fulham Architect",
        "summary": "Rebuilt Fulham into a consistent top-half PL side with attractive football. Previously had troubled spells at Everton and Watford but has matured significantly. Strong candidate last time around.",
        "strengths": ["Consistent PL mid-table overperformance", "Builds cohesive attacking sides", "Experienced in PL management across multiple clubs"],
        "concerns": ["Previous failures at bigger clubs (Everton)", "Under contract at Fulham — compensation needed", "Questions about ceiling at a top-6 club"],
        "verdict": "RECOMMENDED"
    },
    "kieran-mckenna": {
        "tagline": "The Young Architect",
        "summary": "Youngest manager on the shortlist. Achieved back-to-back promotions at Ipswich Town and has shown tactical sophistication beyond his years. Former Manchester United coach with deep tactical education.",
        "strengths": ["Exceptional trajectory — fastest rise in English football", "Deeply analytical, modern coaching approach", "Strong youth development ethos"],
        "concerns": ["Zero top-flight management experience", "Ipswich struggling in the PL — mixed first season", "Massive step up in pressure and expectations"],
        "verdict": "RECOMMENDED (HIGH POTENTIAL)"
    },
    "xabi-alonso": {
        "tagline": "The Unbeaten Champion",
        "summary": "Led Bayer Leverkusen to an unbeaten Bundesliga title — one of football's greatest managerial achievements. Now at Real Madrid. The dream candidate but almost certainly unavailable.",
        "strengths": ["Proven at the absolute highest level", "Blend of tactical brilliance and calmness", "Background at Liverpool gives PL cultural awareness"],
        "concerns": ["Currently at Real Madrid — not leaving", "Would be an enormous fee/compensation package", "Widely expected to manage Liverpool eventually"],
        "verdict": "DREAM OPTION (UNAVAILABLE)"
    },
    "robbie-keane": {
        "tagline": "The Spurs Legend",
        "summary": "Beloved Spurs striker turned manager. Won titles in Israel (Maccabi Tel Aviv) and Hungary (Ferencvaros). The sentimental choice with genuine managerial credentials, though in smaller leagues.",
        "strengths": ["Deep Spurs connection — fan favourite", "Winner's mentality — titles in multiple countries", "Hungry, ambitious, and available"],
        "concerns": ["No top-5 league management experience", "Step up from Hungarian league is enormous", "Emotional appointment risk — sentiment over substance?"],
        "verdict": "OUTSIDER — EMOTIONAL CHOICE"
    },
    "john-heitinga": {
        "tagline": "The Inside Man",
        "summary": "Already at the club as Frank's assistant. Previously served as interim manager at Ajax twice. Low-risk caretaker option who knows the squad, but limited permanent managerial experience.",
        "strengths": ["Already knows the squad and facilities", "Can stabilise immediately with no transition", "Low-cost, low-risk appointment"],
        "concerns": ["Very limited managerial CV", "Caretaker energy may not inspire long-term", "Two Ajax interim stints were mixed"],
        "verdict": "CARETAKER OPTION"
    },
    "enzo-maresca": {
        "tagline": "The Possession Perfectionist",
        "summary": "Championship winner with Leicester (97 points) before guiding Chelsea to 4th place and Champions League qualification. Guardiola protégé with elite youth development credentials but weak pressing intensity.",
        "strengths": ["Elite youth development (16% U23 minutes, 8 academy debuts)", "Possession mastery (xG open play 1.10, 2nd in Premier League)", "Championship pedigree (Leicester 97 points, record promotion)", "Strong sell-on profit (€101m from player sales)", "Decent Big 6 record (2-1-2, Conference League winner)", "Long-term potential (age 45, Guardiola education)"],
        "concerns": ["Weak pressing intensity (PPDA 12.8, ranked 12th in PL)", "Massive net spend dependency (£185m in one season)", "Fragile fan backing (43% approval, 57% wanted change)", "Unavailable (at Chelsea, requires buyout compensation)", "Defensive fragility (xGA 1.13, only +2 goal difference)", "Mixed knockout record (early FA/Carabao Cup exits)"],
        "verdict": "TALENTED BUT MISALIGNED"
    },
    "igor-tudor": {
        "tagline": "The Tactical Mercenary",
        "summary": "Ultra-aggressive pressing specialist who secured Marseille 3rd place (73 points) in 2022-23. Elite pressing intensity but minimal youth development and toxic dressing room culture. Actually hired by Spurs in Feb 2026.",
        "strengths": ["Elite pressing intensity (PPDA 8.34, 3rd-most aggressive)", "Strong defensive organization (xGA/90 1.05)", "Proven survival specialist (Marseille 3rd, Verona 9th)", "Immediately available from Lazio", "Competitive in big games (4-6-2 vs top 6)", "Vertical attacking transitions from high press"],
        "concerns": ["Abysmal youth development (8% U23 minutes, only 2 debuts)", "Toxic dressing room culture (1.75 media sigma, player revolt)", "High injury burden (820 days/season, overworks squad)", "Poor knockout record (42%, lost to 5th-tier Annecy)", "Resigned after 1 season citing exhaustion", "Minimal player trading value (€12m sell-on profit)"],
        "verdict": "SHORT-TERM SURVIVAL HIRE"
    },
}


def export_scores_json(df: pd.DataFrame, meta_df: pd.DataFrame, output_path: str = None) -> dict:
    """
    Export all scores and metadata as JSON for the frontend.

    Args:
        df: scored DataFrame from unified_score.calculate_all_scores()
        meta_df: metadata DataFrame
        output_path: where to write the JSON file

    Returns:
        The exported data dict
    """
    output = Path(output_path) if output_path else Path(__file__).resolve().parent.parent / "docs" / "data" / "scores.json"
    output.parent.mkdir(parents=True, exist_ok=True)

    # Peer category columns
    peer_cats = [c for c in df.columns if c.startswith("peer_") and c != "peer_score"]
    fit_cats = [c for c in df.columns if c.startswith("fit_") and c != "fit_index"]
    pot_cats = [c for c in df.columns if c.startswith("pot_")]

    # Merge with metadata for export
    merged = df.merge(meta_df[["manager_name", "slug", "age", "nationality", "current_club", "available"]],
                       on="manager_name", how="left")

    managers_list = []
    for _, row in merged.iterrows():
        slug = row.get("slug", row["manager_name"].lower().replace(" ", "-"))
        narrative = NARRATIVES.get(slug, {
            "tagline": "Manager Candidate",
            "summary": "",
            "strengths": [],
            "concerns": [],
            "verdict": "UNDER EVALUATION"
        })

        manager_data = {
            "slug": slug,
            "name": row["manager_name"],
            "nationality": row.get("nationality", ""),
            "age": int(row.get("age", 0)),
            "current_club": row.get("current_club", ""),
            "available": bool(row.get("available", True)),
            "rank": int(row["rank"]),
            "final_score": float(row["final_score"]),
            "peer_score": float(row["peer_score"]),
            "fit_index": float(row["fit_index"]),
            "potential_index": float(row["potential_index"]),
            "spursfit_total": float(row["spursfit_total"]),
            "peer_categories": {
                col.replace("peer_", ""): float(row[col])
                for col in peer_cats
            },
            "fit_categories": {
                col.replace("fit_", ""): float(row[col])
                for col in fit_cats
            },
            "potential_components": {
                col.replace("pot_", ""): float(row[col])
                for col in pot_cats
            },
            "narrative": narrative,
        }
        managers_list.append(manager_data)

    data = {
        "version": "2.0",
        "generated_at": pd.Timestamp.now().isoformat(),
        "methodology": {
            "peer_weight": 0.40,
            "spursfit_weight": 0.60,
            "fit_within_spursfit": 0.60,
            "potential_within_spursfit": 0.40,
            "peer_categories": [c.replace("peer_", "") for c in peer_cats],
            "fit_categories": [c.replace("fit_", "") for c in fit_cats],
        },
        "managers": managers_list,
    }

    with open(output, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Exported scores to {output}")
    return data
