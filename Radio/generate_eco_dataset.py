"""
generate_eco_dataset.py — GlobalSentry ECO-SENTRY Demo Dataset Generator

Generates 500 realistic economic alert records in the EXACT same schema
as alerts.json produced by the live GlobalSentry agent pipeline.

Run:
    python generate_eco_dataset.py

Output:
    eco_sentry_dataset.json  — 500 ECO-SENTRY alerts ready to load
"""

import json
import uuid
import random
from datetime import datetime, timedelta

# ─── Seed for reproducibility ────────────────────────────────────────────────
random.seed(42)

# ─── Base date (alerts span the last 18 months) ───────────────────────────────
BASE_DATE = datetime(2024, 10, 1, 0, 0, 0)

# ─── Rich ECO-SENTRY event templates ─────────────────────────────────────────
# Each tuple: (headline, severity_range, confidence_range, has_convergence_prob)

ECO_EVENTS = [
    # ── MARKET VOLATILITY & CRASHES ──────────────────────────────────────────
    ("Global stock markets experience 'Black Monday' style correction as tech bubble bursts", (4,5), (0.85,0.95), 0.4),
    ("Nikkei 225 drops 12% in single session following Bank of Japan interest rate hike", (4,5), (0.90,0.98), 0.3),
    ("S&P 500 VIX Volatility Index hits post-2020 high amid geopolitical uncertainty", (3,4), (0.80,0.92), 0.2),
    ("Flash crash in Treasury yields triggers automated circuit breakers on Wall Street", (4,5), (0.85,0.95), 0.3),
    ("Crypto market wipeout: Bitcoin drops 25% as major stablecoin loses peg", (3,5), (0.75,0.90), 0.2),
    ("Emerging market bond sell-off accelerates as dollar strengthens to 20-year high", (4,5), (0.82,0.94), 0.4),
    ("Hedge fund liquidation event causes massive volatility in European banking stocks", (4,5), (0.78,0.92), 0.3),

    # ── DEBT & SOVEREIGN CRISIS ──────────────────────────────────────────────
    ("Argentina enters technical default as debt restructuring talks with IMF stall", (5,5), (0.92,0.99), 0.5),
    ("Turkey's credit rating downgraded to junk status as inflation hits 85%", (4,5), (0.88,0.97), 0.4),
    ("Sri Lanka's foreign exchange reserves hit critical low; fuel imports suspended", (5,5), (0.90,0.98), 0.6),
    ("Pakistan reaches emergency agreement with GCC for $5B liquidity support", (4,5), (0.85,0.95), 0.4),
    ("US debt ceiling standoff triggers warning from Fitch on AAA rating stability", (3,5), (0.80,0.93), 0.3),
    ("Eurozone peripheral bond spreads widen to dangerous levels — ECB enters market", (4,5), (0.82,0.94), 0.3),
    ("Zambia concludes landmark debt relief deal with G20 creditors after 3-year wait", (2,3), (0.85,0.95), 0.2),

    # ── INFLATION & CURRENCY ────────────────────────────────────────────────
    ("Wheat prices surge 40% following major crop failure in Black Sea region", (4,5), (0.88,0.97), 0.6),
    ("Oil prices hit $120/barrel as Middle East tensions disrupt Strait of Hormuz", (5,5), (0.85,0.96), 0.5),
    ("Rice export ban in India triggers panic buying across Southeast Asian markets", (4,5), (0.87,0.96), 0.6),
    ("Euro falls below parity with US Dollar for first time in two decades", (3,4), (0.90,0.98), 0.2),
    ("Hyperinflation alert: Zimbabwe Dollar loses 99% of value in six months", (5,5), (0.88,0.97), 0.4),
    ("Coffee futures hit record highs as Brazil frosts destroy 30% of harvest", (3,4), (0.82,0.94), 0.3),
    ("Natural gas prices in Europe spike 300% as pipeline maintenance extended indefinitely", (5,5), (0.85,0.95), 0.5),

    # ── SUPPLY CHAIN & TRADE ────────────────────────────────────────────────
    ("Red Sea shipping disruptions add $1M per voyage in fuel and insurance costs", (4,5), (0.85,0.95), 0.4),
    ("Semiconductor shortage 2.0: Rare earth export curbs hit EV battery production", (4,5), (0.82,0.94), 0.4),
    ("Global shipping container rates triple as Panama Canal drought limits transits", (3,5), (0.80,0.92), 0.3),
    ("Port of Singapore reports record congestion — average wait time exceeds 7 days", (3,4), (0.85,0.95), 0.2),
    ("EU-China trade war escalates as 35% tariffs imposed on electric vehicles", (4,5), (0.88,0.97), 0.4),
    ("Critical strike at US East Coast ports threatens 15% of global maritime trade", (5,5), (0.85,0.95), 0.3),
    ("Automotive plant shutdowns in Germany linked to shortage of Ukrainian wire harnesses", (3,4), (0.80,0.92), 0.3),

    # ── BANKING & FINANCIAL SECTOR ──────────────────────────────────────────
    ("Major investment bank reports 'unprecedented' losses in private credit portfolio", (4,5), (0.75,0.90), 0.3),
    ("Regional bank run in Midwest US forces emergency FDIC intervention", (5,5), (0.85,0.97), 0.3),
    ("Central Bank of Nigeria raises interest rates by 400bps to combat currency slide", (4,5), (0.92,0.99), 0.2),
    ("Credit Suisse-style liquidity crisis hits Tier 2 European lender", (4,5), (0.78,0.92), 0.3),
    ("Shadow banking sector faces $100B margin call as real estate values tumble", (5,5), (0.72,0.88), 0.4),
    ("China's property giant Evergrande liquidation order sends shockwaves through Asia", (5,5), (0.90,0.98), 0.5),
    ("SWIFT disconnection of major economy causes chaos in cross-border payments", (5,5), (0.95,0.99), 0.4),

    # ── LABOR & UNEMPLOYMENT ────────────────────────────────────────────────
    ("US unemployment rate hits surprise 4.5% — recession fears mount", (3,4), (0.85,0.95), 0.2),
    ("Mass layoffs in Silicon Valley: Over 50,000 jobs cut in Q1 2025", (3,4), (0.90,0.98), 0.2),
    ("General strike in France paralyzes energy and transport sectors for two weeks", (4,5), (0.88,0.97), 0.3),
    ("Youth unemployment in South Africa reaches record 63% — risk of social unrest High", (5,5), (0.85,0.95), 0.5),
    ("Labor shortages in AI engineering sector drive 40% salary inflation in tech hubs", (2,3), (0.75,0.88), 0.1),
    ("Widespread industrial action in South Korean shipyards threatens global tanker supply", (3,4), (0.82,0.94), 0.2),
    ("Minimum wage hike in UK triggers price increases across hospitality sector", (2,3), (0.85,0.95), 0.1),

    # ── REAL ESTATE & CRITICAL COMMODITIES ──────────────────────────────────
    ("Commercial real estate values in London and NY drop 40% from peak", (4,5), (0.80,0.92), 0.4),
    ("Lithium prices collapse 70% as EV demand growth slows globally", (3,4), (0.85,0.95), 0.2),
    ("Gold hits all-time high of $2,700 as safe-haven demand surges", (3,4), (0.95,0.99), 0.2),
    ("Cocoa prices hit $10,000 per ton as West African harvests fail", (4,5), (0.90,0.98), 0.3),
    ("Copper inventories at LME hit 15-year lows; supply gap projected for 2026", (3,4), (0.82,0.94), 0.3),
    ("Residential mortgage defaults in Canada triple as interest rates remain elevated", (4,5), (0.78,0.92), 0.3),
    ("Iron ore shipments from Australia disrupted by Category 4 cyclone", (3,4), (0.88,0.97), 0.2),

    # ── GEOPOLITICAL ECONOMY ────────────────────────────────────────────────
    ("BRICS nations announce gold-backed settlement currency to bypass USD", (4,5), (0.70,0.85), 0.4),
    ("US imposes secondary sanctions on foreign banks aiding tech transfers", (4,5), (0.85,0.95), 0.3),
    ("Trade deal between UK and India collapses over visa requirements", (3,4), (0.88,0.97), 0.2),
    ("OPEC+ announces surprise 2M barrel/day production cut starting next month", (5,5), (0.92,0.99), 0.4),
    ("Nord Stream pipeline investigation reveals intentional sabotage — energy risk High", (5,5), (0.85,0.95), 0.5),
    ("Global defense spending hits records $2.5 trillion — crowding out social investment", (3,4), (0.90,0.98), 0.3),
    ("G7 announces 15% global minimum corporate tax implementation timeline", (2,3), (0.95,0.99), 0.1),
]

# ─── Analysis templates per event type ────────────────────────────────────────

ANALYSIS_TEMPLATES = {
    "markets": [
        "**Market Intelligence Analysis — GlobalSentry ECO-SENTRY**\n\n**1. Market Dynamics and Volatility:**\nThe current sell-off in {sector} is driven by {driver}. VIX spiked to {vix}, indicating extreme fear. Technical indicators suggest {technical_outlook}.\n\n**2. Macroeconomic Impact:**\nEstimated wealth destruction totals ${wealth_loss}T globally. Secondary effects include tightening of credit conditions and a {liquidity_status} liquidity environment. Institutional exposure is concentrated in {exposure_region}.\n\n**3. Mitigation & Outlook:**\n- Central banks likely to intervene with {intervention} liquidity injections\n- Recommendation: De-risk portfolios and increase cash positions\n- Monitor {key_indicator} for signs of bottoming out\n- Potential for contagion to {contagion_sector} is HIGH in current 72h window.\n\nSEVERITY: {sev} | CONFIDENCE: {conf}",
    ],
    "sovereign": [
        "**Sovereign Risk Assessment — ECO-SENTRY AI**\n\n**1. Fiscal Position:**\n{country} faces a critical financing gap of ${gap}B. Debt-to-GDP ratio has reached {debt_ratio}%, with interest payments consuming {revenue_share}% of tax revenue.\n\n**2. External Vulnerability:**\nForeign exchange reserves are down to {fx_reserves} months of import cover. Currency depreciation of {depreciation}% in 30 days is accelerating inflation to {inflation}%.\n\n**3. Crisis Trajectory:**\n- Risk of disorderly default is {default_risk}\n- IMF 'Staff Level Agreement' is {imf_status}\n- Social unrest probability: {unrest_prob}% based on past price shock correlations\n- Spillover risk to neighboring frontier markets is increasing.\n\nSEVERITY: {sev} | CONFIDENCE: {conf}",
    ],
    "commodities": [
        "**Commodity Supply-Demand Analysis**\n\n**1. Supply Disruption:**\nProduction of {commodity} in {region} has dropped by {drop}% due to {cause}. Current global inventory levels are {inventory_level}% below historical 5-year averages.\n\n**2. Price Transmission:**\nForward curves exhibit {curve_state}, signaling persistent shortage. Impact on downstream industries ({industries}) will manifest in {timeline} weeks. Inflationary impact estimated at +{cpi_impact}bps to global CPI.\n\n**3. Recommendations:**\n- Activate strategic reserves where available\n- Diversify procurement to {alt_source} in short-term\n- Implement export restrictions to protect domestic supply\n- Anticipate margin calls in commodity trading houses.\n\nSEVERITY: {sev} | CONFIDENCE: {conf}",
    ],
    "trade": [
        "**Global Trade & Supply Chain Alert**\n\n**1. Network Disruption:**\nCritical chokepoint {chokepoint} is currently {status}. Average transit times have increased by {delay} days, adding ${cost_increase} per container. Throughput capacity is down {throughput_drop}%.\n\n**2. Sectoral Impact:**\nThe {sector} industry is most exposed with {exposure_level}% of inputs transiting the affected route. Just-in-time manufacturing buffers are estimated at {buffer} days.\n\n**3. Strategic Response:**\n- Rerouting around {alternative} increases lead times by {extra_time}\n- Inventory pull-forward recommended for Q2/Q3 cycles\n- Near-shoring initiatives to {nearshore_loc} likely to accelerate\n- Monitor air freight rates for sudden surge as shippers bypass maritime delays.\n\nSEVERITY: {sev} | CONFIDENCE: {conf}",
    ],
    "general": [
        "**Economic Intelligence Report — ECO-SENTRY Pipeline**\n\n**1. Event Overview:**\nClassification: {classification}. Impact area: {impact_area}. Drivers: {drivers}.\n\n**2. Key Metrics:**\nEconomic Sentiment Index: {esi}/100. Consumer Confidence drop: {cc_drop}%. Estimated GDP impact: {gdp_impact}% for the current fiscal year.\n\n**3. Policy Recommendations:**\n- Adjust fiscal stimulus measures to counter {threat}\n- Monitor employment levels in sensitive sectors\n- Coordinate with international financial institutions for stabilizing measures\n- Regular briefings to stakeholders on supply chain resilience.\n\nSEVERITY: {sev} | CONFIDENCE: {conf}",
    ]
}

CONVERGENCE_WARNINGS = [
    "⚠️ CONVERGENCE WARNING: This economic crisis overlaps with a major EPI-SENTRY outbreak in the same region. Healthcare spending is being diverted to debt servicing, while high inflation is making essential medicines unaffordable, creating a catastrophic public health-finance spiral.",
    "⚠️ CONVERGENCE WARNING: Cross-sector risk detected with a SUPPLY-SENTRY alert on energy shortages. Industrial output collapse is driving this hyperinflationary event, as producers pass on soaring costs to a dwindling consumer base.",
    "⚠️ CONVERGENCE WARNING: Economic default in this region correlates with ECO-SENTRY drought alerts. Agriculture accounts for 40% of GDP; crop failure is not just a food crisis but the primary driver of national insolvency.",
    "⚠️ CONVERGENCE WARNING: This market crash intersects with a SUPPLY-SENTRY trigger on logistical failures in major ports. Frozen credit markets are preventing trade financing, leading to thousands of stalled shipments and a global supply chain cardiac arrest.",
    "⚠️ CONVERGENCE WARNING: Hyperinflation in this country is being amplified by an EPI-SENTRY cholera outbreak. The collapse of the local currency has eliminated the state's ability to import water treatment chemicals, leading to rapid disease transmission.",
    "⚠️ CONVERGENCE WARNING: Sovereign debt distress in this region is linked to ECO-SENTRY deforestation and mining alerts. Resource depletion is eroding the long-term collateral for international loans, triggering a sudden-stop in foreign investment.",
    "⚠️ CONVERGENCE WARNING: Labor strikes in the transport sector correlate with a SUPPLY-SENTRY alert on critical food shortages. This compound event creates a high probability of civil unrest surpassing the capacity of local security forces.",
    "⚠️ CONVERGENCE WARNING: Trade sanctions in this event intersect with an EPI-SENTRY vaccination gap. Restricted dual-use technologies include cold-chain equipment, directly impacting the region's ability to contain a concurrent measles epidemic.",
]

REGIONS = [
    "Global", "United States", "European Union", "China", "India",
    "Southeast Asia (ASEAN)", "South America (Mercosur)", "Middle East (GCC)",
    "Sub-Saharan Africa", "East Africa", "West Africa", "Central Asia",
    "OECD Nations", "G20 Economies", "Emerging Markets", "Frontier Markets",
    "BRICS+ Countries", "Indo-Pacific Region", "Central America", "Eastern Europe"
]

# ─── Helper functions ─────────────────────────────────────────────────────────

def random_date(start: datetime, end: datetime) -> datetime:
    delta = end - start
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=random_seconds)

def fill_analysis(template: str, sev: int, conf: float) -> str:
    replacements = {
        "{sector}": random.choice(["technology stocks", "industrial commodities", "government bonds", "commercial real estate", "private credit"]),
        "{driver}": random.choice(["hawkish Fed signaling", "geopolitical escalation", "unexpected earnings misses", "liquidity mismatch", "algorithmic selling"]),
        "{vix}": f"{random.uniform(25, 48):.1f}",
        "{technical_outlook}": random.choice(["death cross on weekly charts", "oversold conditions but no reversal", "retesting 2022 lows", "capitulation phase"]),
        "{wealth_loss}": f"{random.uniform(1.2, 12.5):.1f}",
        "{liquidity_status}": random.choice(["restricted", "evaporating", "seized-up", "highly volatile"]),
        "{exposure_region}": random.choice(REGIONS),
        "{intervention}": random.choice(["repo-market", "QE-style", "emergency rate cut", "swap-line"]),
        "{key_indicator}": random.choice(["HY Spread", "2/10 Treasury curve", "LIBOR-OIS spread", "CBOE Put/Call ratio"]),
        "{contagion_sector}": random.choice(["insurance companies", "pension funds", "retail banking", "corporate debt markets"]),
        "{country}": random.choice(["Argentina", "Turkey", "Pakistan", "Egypt", "Nigeria", "Sri Lanka", "Ukraine"]),
        "{gap}": f"{random.uniform(3, 45):.1f}",
        "{debt_ratio}": f"{random.randint(65, 145)}",
        "{revenue_share}": f"{random.randint(25, 65)}",
        "{fx_reserves}": f"{random.uniform(0.5, 2.5):.1f}",
        "{depreciation}": f"{random.randint(15, 60)}",
        "{inflation}": f"{random.randint(35, 120)}",
        "{default_risk}": random.choice(["CRITICAL", "IMMIMNENT", "HIGH (>80%)", "TECHNICAL"]),
        "{imf_status}": random.choice(["stalled", "under review", "cancelled", "delayed indefinitely"]),
        "{unrest_prob}": f"{random.randint(45, 95)}",
        "{commodity}": random.choice(["Wheat", "Copper", "Lithium", "Cruide Oil", "Natural Gas", "Cocoa", "Soybeans"]),
        "{region}": random.choice(REGIONS),
        "{drop}": f"{random.randint(15, 45)}",
        "{cause}": random.choice(["crop failure", "labor strikes", "export bans", "geopolitical blockade", "extreme weather"]),
        "{inventory_level}": f"{random.randint(20, 60)}",
        "{curve_state}": random.choice(["deep backwardation", "super-contango", "extreme volatility"]),
        "{industries}": random.choice(["EV manufacturing", "food processing", "power generation", "construction", "chemicals"]),
        "{timeline}": f"{random.randint(4, 12)}",
        "{cpi_impact}": f"{random.randint(50, 350)}",
        "{alt_source}": random.choice(["Australian producers", "Brazilian exports", "North American shale", "Kazakhstani mines"]),
        "{chokepoint}": random.choice(["Strait of Hormuz", "Suez Canal", "Panama Canal", "Malacca Strait", "Port of Shanghai"]),
        "{status}": random.choice(["partially blocked", "experiencing major delays", "highly congested", "at record low capacity"]),
        "{delay}": f"{random.randint(5, 25)}",
        "{cost_increase}": f"{random.randint(2500, 15000)}",
        "{throughput_drop}": f"{random.randint(25, 75)}",
        "{exposure_level}": f"{random.randint(40, 85)}",
        "{buffer}": f"{random.randint(2, 14)}",
        "{alternative}": random.choice(["Cape of Good Hope", "Land Bridge", "Air Freight", "Trans-Siberian rail"]),
        "{extra_time}": f"{random.randint(10, 20)} days",
        "{nearshore_loc}": random.choice(["Mexico", "Vietnam", "Poland", "Morocco"]),
        "{classification}": random.choice(["regional financial contagion", "global commodity shock", "supply chain systemic failure", "sovereign debt default"]),
        "{impact_area}": random.choice(REGIONS),
        "{drivers}": random.choice(["monetary tightening", "trade barriers", "resource scarcity", "geopolitical shifts"]),
        "{esi}": f"{random.randint(25, 45)}",
        "{cc_drop}": f"{random.randint(10, 35)}",
        "{gdp_impact}": f"{random.uniform(0.5, 4.5):.1f}",
        "{threat}": random.choice(["stagflation", "recession", "deflationary spiral", "liquidity trap"]),
        "{sev}": str(sev),
        "{conf}": f"{conf:.2f}",
    }
    for placeholder, value in replacements.items():
        template = template.replace(placeholder, value)
    return template

def pick_analysis_key(headline: str) -> str:
    hl = headline.lower()
    if any(k in hl for k in ["stock", "market", "volatility", "vix", "crash", "correction", "liquidation", "fund"]):
        return "markets"
    if any(k in hl for k in ["debt", "sovereign", "default", "rating", "liquidity", "bank", "imf", "reserves"]):
        return "sovereign"
    if any(k in hl for k in ["price", "wheat", "oil", "commodity", "gas", "futures", "harvest", "inventory"]):
        return "commodities"
    if any(k in hl for k in ["trade", "shipping", "supply", "port", "tariffs", "logistic", "transit"]):
        return "trade"
    return "general"

# ─── Generate 500 records ─────────────────────────────────────────────────────

def generate_dataset(n: int = 500) -> list:
    alerts = []
    end_date = datetime(2026, 3, 30, 23, 59, 59)

    for i in range(n):
        event_template = ECO_EVENTS[i % len(ECO_EVENTS)]
        headline, sev_range, conf_range, conv_prob = event_template

        # Add variation to headline for uniqueness
        source_prefixes = [
            "Bloomberg —", "Reuters —", "Financial Times —", "WSJ Alert:", "CNBC Breaking:",
            "Economist Intelligence:", "World Bank Report:", "IMF Bulletin:", "ECB Press Release:",
            "Fed Watch:", "MarketWatch:", "Nikkei Asia:", "Barron's:", "TradingEconomics:",
            "Goldman Sachs Analysis:", "JPMorgan Market Flash:"
        ]
        time_prefixes = [
            "", "", "",
            "(URGENT) ", "(FLASH) ", "(LATEST) ", "(PREVIEW) ",
        ]

        variant_headline = f"{random.choice(time_prefixes)}{random.choice(source_prefixes)} {headline}"
        if len(variant_headline) > 220:
            variant_headline = variant_headline[:217] + "..."

        severity = random.randint(*sev_range)
        confidence = round(random.uniform(*conf_range), 2)
        is_verified = random.random() < (0.70 + confidence * 0.20)

        ts = random_date(BASE_DATE, end_date)
        timestamp_str = ts.isoformat()

        analysis_key = pick_analysis_key(headline)
        template_pool = ANALYSIS_TEMPLATES.get(analysis_key, ANALYSIS_TEMPLATES["general"])
        raw_analysis = fill_analysis(random.choice(template_pool), severity, confidence)

        has_convergence = random.random() < conv_prob
        convergence_warning = random.choice(CONVERGENCE_WARNINGS) if has_convergence else None

        alert = {
            "id": str(uuid.uuid4()),
            "headline": variant_headline,
            "mode": "eco",
            "severity": severity,
            "confidence": confidence,
            "is_verified": is_verified,
            "source": random.choice([
                "Bloomberg Terminal",
                "Reuters Eikon Feed",
                "World Bank Open Data",
                "IMF Data Mapper",
                "ECB Statistical Data Warehouse",
                "FRED Economic Data",
                "S&P Global Market Intelligence",
                "Moody's Analytics Feed",
            ]),
            "timestamp": timestamp_str,
            "analysis": raw_analysis[:800],
            "convergence_warning": convergence_warning,
        }
        alerts.append(alert)

    alerts.sort(key=lambda x: x["timestamp"], reverse=True)
    return alerts

# ─── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("═══════════════════════════════════════════════════")
    print("  GlobalSentry — ECO-SENTRY Dataset Generator")
    print("  Generating 500 economic alert records...")
    print("═══════════════════════════════════════════════════")

    dataset = generate_dataset(500)

    output_path = "eco_sentry_dataset.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Done! {len(dataset)} ECO-SENTRY alerts written to: {output_path}")
    print(f"   File size: {len(json.dumps(dataset)) / 1024:.1f} KB")

    # Stats summary
    severities = [a["severity"] for a in dataset]
    verified = sum(1 for a in dataset if a["is_verified"])
    convergence = sum(1 for a in dataset if a["convergence_warning"])
    sources = {}
    for a in dataset:
        sources[a["source"]] = sources.get(a["source"], 0) + 1

    print("\n📊 Dataset Statistics:")
    print(f"   Total alerts      : {len(dataset)}")
    print(f"   Verified alerts   : {verified} ({100*verified//len(dataset)}%)")
    print(f"   With convergence  : {convergence} ({100*convergence//len(dataset)}%)")
    print(f"   Avg severity      : {sum(severities)/len(severities):.2f}/5")
    print(f"\n   Date range: {dataset[-1]['timestamp'][:10]} → {dataset[0]['timestamp'][:10]}")
    print("\n💡 Use this to populate your Eco-Sentry dashboard.")
