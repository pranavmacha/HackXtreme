"""
generate_epi_dataset.py — GlobalSentry EPI-SENTRY Demo Dataset Generator

Generates 750 realistic epidemiological alert records in the EXACT same schema
as alerts.json produced by the live GlobalSentry agent pipeline.

Run:
    python generate_epi_dataset.py

Output:
    epi_sentry_dataset.json  — 750 EPI-SENTRY alerts ready to load"""

import json
import uuid
import random
from datetime import datetime, timedelta

# ─── Seed for reproducibility ────────────────────────────────────────────────
random.seed(42)

# ─── Base date (alerts span the last 18 months) ───────────────────────────────
BASE_DATE = datetime(2024, 10, 1, 0, 0, 0)

# ─── Rich EPI-SENTRY event templates ─────────────────────────────────────────
# Each tuple: (headline, severity_range, confidence_range, has_convergence_prob)

EPI_EVENTS = [
    # ── RESPIRATORY / AIRBORNE ──────────────────────────────────────────────
    ("WHO declares public health emergency over novel influenza H5N2 strain spreading in Southeast Asia", (4,5), (0.85,0.97), 0.4),
    ("Spike in severe pneumonia cases of unknown etiology reported across five Indian states", (3,5), (0.70,0.90), 0.3),
    ("COVID-19 XEC subvariant surges 340% in South Korea — hospitalizations rising", (3,4), (0.80,0.95), 0.2),
    ("Bird flu H5N1 detected in human cluster in Cambodia; WHO convenes emergency meeting", (4,5), (0.88,0.98), 0.5),
    ("MERS-CoV cluster of 12 cases identified in healthcare workers in Riyadh, Saudi Arabia", (4,5), (0.82,0.95), 0.3),
    ("Respiratory syncytial virus (RSV) overwhelms pediatric ICUs in Brazil winter surge", (3,4), (0.75,0.90), 0.2),
    ("Novel bat-origin coronavirus detected in patients in Yunnan province, China — WHO monitoring", (4,5), (0.78,0.92), 0.4),
    ("Record influenza A(H3N2) season declared in Australia; vaccine mismatch confirmed", (3,4), (0.80,0.93), 0.2),
    ("Tuberculosis drug-resistant strain XDR-TB detected in 23 districts of India — containment failing", (4,5), (0.85,0.95), 0.3),
    ("Legionnaires' disease outbreak traced to hotel cooling towers in Istanbul, Turkey — 45 cases", (3,4), (0.78,0.90), 0.2),

    # ── VECTOR-BORNE / MOSQUITO ─────────────────────────────────────────────
    ("Dengue fever season begins 6 weeks early in Southeast Asia; Singapore raises DORSCON alert", (3,4), (0.80,0.92), 0.3),
    ("Dengue hemorrhagic fever cases triple in Bangladesh compared to 2023 baseline — overwhelmed hospitals", (4,5), (0.83,0.95), 0.4),
    ("Zika virus re-emergence reported in Colombia and Ecuador — travel warnings issued", (3,5), (0.75,0.90), 0.3),
    ("Chikungunya outbreak spreading rapidly in coastal Karnataka, India — 18,000 cases in 3 weeks", (3,4), (0.80,0.92), 0.2),
    ("West Nile Virus neuroinvasive disease cases surge in Romania and Greece — 34 deaths", (4,5), (0.85,0.95), 0.3),
    ("Malaria P. falciparum drug resistance confirmed in artemisinin — WHO emergency bulletin issued", (4,5), (0.88,0.97), 0.5),
    ("Yellow fever outbreak declared in Democratic Republic of Congo; 156 deaths confirmed", (4,5), (0.87,0.97), 0.4),
    ("Leishmaniasis cases surge in conflict zones of Sudan — MSF activates emergency response", (3,4), (0.78,0.90), 0.3),
    ("Japanese encephalitis outbreak confirmed in Uttar Pradesh villages — 28 children affected", (4,5), (0.82,0.94), 0.3),
    ("Rift Valley fever outbreak in Kenya and Somalia — livestock and human cases rising", (3,5), (0.80,0.93), 0.4),

    # ── WATERBORNE / FOODBORNE ──────────────────────────────────────────────
    ("Cholera outbreak declared in Sudan; over 3,200 cases in two weeks amid flooding", (4,5), (0.88,0.97), 0.6),
    ("Cholera resurfaces in Haiti following hurricane; CDC issues Level 3 travel notice", (4,5), (0.85,0.95), 0.5),
    ("Typhoid fever outbreak in Karachi linked to contaminated municipal water supply", (3,4), (0.78,0.92), 0.3),
    ("E. coli O157:H7 outbreak in UK linked to unpasteurized cheese — 120 hospitalized", (3,4), (0.80,0.93), 0.2),
    ("Hepatitis A outbreak in Afghanistan refugee camps — vaccination drive launched", (3,4), (0.78,0.90), 0.3),
    ("Salmonella Typhi clusters in multiple states linked to contaminated spice imports from India", (3,4), (0.75,0.90), 0.2),
    ("AGE (Acute Gastroenteritis) outbreak on cruise ship in Mediterranean — 400 passengers", (2,3), (0.70,0.85), 0.1),
    ("Norovirus mass outbreak in South Korea elementary schools — 2,400 children ill", (2,3), (0.78,0.90), 0.1),
    ("Cryptosporidiosis outbreak in Wales traced to municipal swimming pool", (2,3), (0.72,0.88), 0.1),
    ("Listeria outbreak in US linked to deli meats — 7 deaths, recall issued for 14 brands", (4,5), (0.87,0.97), 0.3),

    # ── HEMORRHAGIC FEVER ───────────────────────────────────────────────────
    ("Ebola outbreak declared in North Kivu, DRC — 12 confirmed deaths, cordon sanitaire deployed", (5,5), (0.92,0.99), 0.5),
    ("ProMED alert: Unidentified hemorrhagic fever with 40% CFR kills 18 in remote Guinea village", (5,5), (0.80,0.95), 0.5),
    ("Marburg virus confirmed in persons who returned from Uganda to Germany — border alerts active", (5,5), (0.90,0.98), 0.5),
    ("Lassa fever season peak in Nigeria — 340 confirmed cases, 47 deaths; Abuja on alert", (4,5), (0.87,0.96), 0.4),
    ("Crimean-Congo hemorrhagic fever detected in healthcare workers in Pakistan — nosocomial cluster", (4,5), (0.85,0.95), 0.4),
    ("Sudan ebolavirus variant detected in DRC — divergent from current Zaire vaccine", (5,5), (0.88,0.97), 0.5),
    ("Hantavirus pulmonary syndrome surge in rural Argentina — 15 deaths, animal contact confirmed", (4,5), (0.82,0.94), 0.3),
    ("Nipah virus cluster in Kerala, India — 3 deaths, 78 contacts quarantined", (5,5), (0.90,0.98), 0.5),
    ("Kyasanur Forest Disease (KFD) cases detected outside endemic zones — Karnataka and Goa alert", (3,4), (0.78,0.92), 0.2),
    ("Novel orthohantavirus detected in rodent populations near Shanghai urban periphery", (3,4), (0.72,0.88), 0.3),

    # ── MENINGITIS / NEUROLOGICAL ────────────────────────────────────────────
    ("Meningococcal meningitis C outbreak in meningitis belt — Nigeria, Niger, Chad surge", (4,5), (0.85,0.95), 0.3),
    ("Group A meningococcal disease kills 23 students in Ethiopia boarding school cluster", (4,5), (0.87,0.96), 0.3),
    ("Enterovirus 71 (EV-A71) causing hand-foot-mouth disease with CNS complications in Vietnam", (3,4), (0.80,0.92), 0.3),
    ("Monkeypox clade Ib causing severe neurological complications in DRC patients — new phenotype", (4,5), (0.85,0.95), 0.4),
    ("Fatal encephalitis cluster in Assam, India — pathogen unidentified, 9 children dead", (4,5), (0.82,0.94), 0.4),
    ("Rabies deaths surge in Bali following reduction in dog vaccination program coverage", (3,4), (0.80,0.92), 0.2),
    ("Acute Flaccid Myelitis (AFM) cluster linked to enterovirus D68 in 7 US states", (3,4), (0.78,0.90), 0.2),
    ("Botulism outbreak in Iran traced to home-canned food — 34 hospitalized, 3 on ventilators", (3,4), (0.80,0.92), 0.2),
    ("Guillain-Barré syndrome spike in Peru linked to Campylobacter-contaminated poultry", (3,4), (0.75,0.88), 0.2),
    ("Prion disease (CJD variant) cluster under investigation in UK — 4 cases in 18 months", (4,5), (0.70,0.85), 0.2),

    # ── CHILDHOOD / VACCINE-PREVENTABLE ─────────────────────────────────────
    ("Measles outbreak in Gaza Strip — vaccination rate drops below 20% due to conflict", (4,5), (0.88,0.97), 0.5),
    ("Polio type 2 re-detected in sewage surveillance in 5 countries; vaccine-derived strain", (4,5), (0.85,0.95), 0.4),
    ("Wild poliovirus type 1 persists in Pakistan and Afghanistan — global eradication at risk", (4,5), (0.87,0.96), 0.4),
    ("Whooping cough (pertussis) surge in UK — 18 infant deaths; worst year since 1980s", (4,5), (0.85,0.95), 0.3),
    ("Diphtheria outbreak in Yemen; 30 deaths, supply of antitoxin critically low globally", (4,5), (0.87,0.96), 0.4),
    ("Rubella cluster in unvaccinated community in Minnesota, US — CDC investigates", (2,3), (0.78,0.90), 0.1),
    ("Mumps outbreak at US university — over 200 confirmed cases in fully vaccinated students", (2,3), (0.75,0.88), 0.1),
    ("Rotavirus season causes severe pediatric dehydration surge in India's BIMARU states", (3,4), (0.80,0.92), 0.2),
    ("Yellow fever vaccination coverage drops below 50% in Angola — re-emergence risk elevated", (3,4), (0.80,0.92), 0.3),
    ("Mpox clade Ib spreads beyond DRC into Uganda, Rwanda, Burundi — WHO PHEIC declared", (4,5), (0.90,0.98), 0.5),

    # ── ANTIMICROBIAL RESISTANCE ─────────────────────────────────────────────
    ("Pan-drug-resistant Klebsiella pneumoniae ST258 cluster in ICU of New Delhi hospital", (4,5), (0.85,0.95), 0.3),
    ("Colistin-resistant E.coli detected in waterways and meat in India — MCR-1 gene confirmed", (4,5), (0.83,0.94), 0.4),
    ("Drug-resistant gonorrhea (XDR-GC) cases confirmed in UK — last-line treatment failing", (4,5), (0.87,0.96), 0.3),
    ("Carbapenem-resistant Acinetobacter baumannii outbreak in Gaza field hospital — 12 deaths", (4,5), (0.85,0.95), 0.4),
    ("MRSA bloodstream infection rates rise 28% across European ICUs post-pandemic", (3,4), (0.80,0.92), 0.2),
    ("Extensively drug-resistant tuberculosis (XDR-TB) found in 47 miners in South Africa", (4,5), (0.87,0.96), 0.4),
    ("AMR Staphylococcus epidermidis capable of surviving all known antibiotics isolated in China", (4,5), (0.82,0.94), 0.3),
    ("WHO declares antimicrobial resistance a global health emergency — urgent treaty proposed", (4,5), (0.88,0.97), 0.4),
    ("Fungal superbug Candida auris found in 25 Indian hospitals — 45% mortality in bloodstream infections", (4,5), (0.87,0.96), 0.4),
    ("Clostridioides difficile hypervirulent ribotype 027 strain emerging across South Asian hospitals", (3,4), (0.80,0.92), 0.3),

    # ── ZOONOTIC / SPILLOVER EVENTS ──────────────────────────────────────────
    ("Swine influenza H1N2v human cases detected in pig farmers in Iowa — cluster of 6", (3,4), (0.78,0.92), 0.3),
    ("Brucellosis outbreak in lab workers following accidental exposure at Lanzhou bioresearch institute", (3,4), (0.80,0.92), 0.2),
    ("Anthrax outbreak kills 47 cattle and 3 humans in remote Siberian region after permafrost thaw", (3,5), (0.82,0.94), 0.4),
    ("Tularemia (rabbit fever) cluster in hunters in Scandinavia — 34 cases, 2 pneumonic forms", (3,4), (0.78,0.90), 0.2),
    ("Psittacosis (parrot fever) cluster traced to illegal exotic bird market in Thailand", (2,3), (0.75,0.88), 0.1),
    ("Q fever outbreak in Dutch goat farming region — 140 human cases linked to parturient animals", (3,4), (0.80,0.92), 0.2),
    ("Henipavirus NiV spillover event documented in pig farmers in Bangladesh — WHO high alert", (5,5), (0.88,0.97), 0.5),
    ("Novel reassortant avian influenza H7N9 detected in poultry markets in Guangzhou — human risk elevated", (4,5), (0.85,0.95), 0.4),
    ("Raccoon dog trade in Eastern Europe linked to novel paramyxovirus cluster in veterinary workers", (3,4), (0.75,0.90), 0.3),
    ("Bat coronavirus with ACE2-binding capability discovered at Yunnan cave — pre-spillover monitoring activated", (4,5), (0.80,0.93), 0.4),

    # ── HEALTH SYSTEM COLLAPSE / HUMANITARIAN ────────────────────────────────
    ("Sudan health system collapse — 70% of hospitals non-functional; mass casualty disease surge", (5,5), (0.90,0.98), 0.6),
    ("Gaza health system collapses — surgical infections, hepatitis A, and scabies surge simultaneously", (5,5), (0.92,0.99), 0.7),
    ("Yemen cholera exceeds 400,000 suspected cases — ACF declares worst epidemic this decade", (5,5), (0.90,0.98), 0.6),
    ("Rohingya refugee camps face typhoid and cholera co-outbreak — Cox's Bazar UNHCR alert", (4,5), (0.87,0.96), 0.5),
    ("Syrian displaced population faces diphtheria-measles twin outbreak in camp settings", (4,5), (0.85,0.95), 0.5),
    ("Ukraine health infrastructure disruptions link to rise in multi-drug-resistant TB", (4,5), (0.82,0.94), 0.4),
    ("Healthcare worker strikes in Kenya and Zimbabwe create vaccination program collapse risk", (3,4), (0.78,0.90), 0.3),
    ("Polio vaccination campaign suspended in 3 Sahel countries due to armed conflict", (4,5), (0.85,0.95), 0.4),
    ("Haiti hospital collapse triggers malaria resurgence — 12,000 new cases in six weeks", (4,5), (0.87,0.96), 0.5),
    ("Ethiopia Tigray famine-disease nexus — SAM (severe acute malnutrition) linked to measles deaths in children", (5,5), (0.90,0.98), 0.5),

    # ── EMERGING / NOVEL OUTBREAKS ───────────────────────────────────────────
    ("New Disease X candidate identified — WHO convenes emergency Technical Advisory Group", (5,5), (0.80,0.95), 0.5),
    ("SARS-like coronavirus spillover from horseshoe bats in Malaysia — three human deaths", (5,5), (0.85,0.97), 0.5),
    ("Novel paramyxovirus with neurotropic properties detected in Indonesian poultry workers", (4,5), (0.82,0.95), 0.4),
    ("Unidentified febrile illness with 30% CFR spreading through mining communities in Zambia", (4,5), (0.78,0.93), 0.4),
    ("First human case of H10N3 avian influenza with aerosol transmission capacity confirmed", (5,5), (0.88,0.97), 0.5),

    # ── TROPICAL / NEGLECTED DISEASES ───────────────────────────────────────
    ("Sleeping sickness (Human African Trypanosomiasis) re-emerges in South Sudan post-conflict", (3,4), (0.78,0.92), 0.3),
    ("Lymphatic filariasis elimination program setback — 8M new infections in South Asia", (3,4), (0.80,0.90), 0.2),
    ("Onchocerciasis (river blindness) re-emerging along the Volta River basin", (3,4), (0.75,0.88), 0.2),
    ("Visceral leishmaniasis (Kala-azar) kills 340 in Bihar, India — drug access crisis", (4,5), (0.85,0.95), 0.3),
    ("Schistosomiasis prevalence reaches 40% in flood-affected communities in Mozambique", (3,4), (0.78,0.90), 0.3),

    # ── CLIMATE-DISEASE NEXUS ────────────────────────────────────────────────
    ("El Niño-driven drought triggers surge in vector-borne diseases across East Africa", (4,5), (0.85,0.95), 0.6),
    ("Arctic permafrost thaw releases dormant anthrax spores — 12 human cases in Yakutia", (4,5), (0.82,0.94), 0.5),
    ("Record heat wave in Pakistan linked to mass heat stroke events overwhelming hospitals", (3,4), (0.80,0.92), 0.3),
    ("Algal bloom in Lake Victoria contaminates drinking water — 5,000 exposed to cyanotoxins", (3,4), (0.78,0.90), 0.3),
    ("Cyclone Freddy flooding in Malawi creates cholera-malaria superimposed outbreak", (5,5), (0.90,0.98), 0.7),

    # ── SURVEILLANCE GAPS & DETECTION FAILURES ───────────────────────────────
    ("Genomic sequencing reveals 2-month delayed detection of novel influenza in rural China", (4,5), (0.82,0.94), 0.4),
    ("ProMED GPHIN alert: Unexplained acute liver failure cluster in 3 children, Uttar Pradesh", (4,5), (0.78,0.92), 0.4),
    ("WHO Disease Outbreak News: Cluster of acute febrile illness, unknown etiology — Cameroon", (4,5), (0.80,0.93), 0.4),
    ("Digital disease surveillance flags 10x spike in hospital admissions in DRC provinces", (4,5), (0.83,0.94), 0.3),
    ("HealthMap alert: Social media reports of mass illness near industrial zone in central India", (3,4), (0.72,0.88), 0.2),

    # ── BIOLOGICAL HAZARD / LAB INCIDENTS ────────────────────────────────────
    ("WHO investigates accidental laboratory release of modified H5N1 strain in biosafety incident", (5,5), (0.85,0.97), 0.4),
    ("Smallpox-like poxvirus detected in patients near defunct Soviet biopreparat research site", (5,5), (0.80,0.95), 0.4),
    ("Anthrax letter bioterrorism alert — suspicious powder packages intercepted at Frankfurt airport", (5,5), (0.82,0.94), 0.3),
    ("BSL-4 containment breach at research facility forces evacuation and quarantine of 60 staff", (4,5), (0.78,0.92), 0.3),
    ("Ricin contamination alert in water supply near military installation — 200 hospitalised", (4,5), (0.80,0.93), 0.3),

    # ── MENTAL HEALTH / INDIRECT HEALTH CRISIS ───────────────────────────────
    ("Mass psychogenic illness (MPI) cluster affects 300 students in Punjab, India", (2,3), (0.75,0.88), 0.1),
    ("Post-conflict mental health crisis in Palestine — WHO warns of epidemic of PTSD", (3,4), (0.78,0.90), 0.2),
    ("Suicide rate in Sri Lanka rises 60% during economic crisis — health emergency declared", (3,4), (0.80,0.92), 0.2),
    ("Opioid overdose deaths reach record levels across US rural counties — 85,000 in 12 months", (4,5), (0.88,0.96), 0.2),
    ("Mystery illness with neuropsychiatric symptoms reported in athletes at regional games", (3,4), (0.75,0.90), 0.2),

    # ── OCCUPATIONAL / INDUSTRIAL HEALTH ─────────────────────────────────────
    ("Silicosis epidemic among Indian stone workers — 40,000 estimated cases, mostly undiagnosed", (4,5), (0.85,0.95), 0.3),
    ("Benzene poisoning outbreak at petrochemical complex in Shandong province — 180 workers", (3,4), (0.80,0.92), 0.2),
    ("Lead poisoning cluster in children near battery recycling plants in Lagos, Nigeria", (4,5), (0.83,0.94), 0.3),
    ("Pesticide mass poisoning event — contaminated groundwater linked to agri-chemical plant in Punjab", (4,5), (0.85,0.95), 0.4),
    ("Asbestos-related mesothelioma epidemic emerging in South Asian nations with legacy exposures", (3,4), (0.80,0.92), 0.2),

    # ── FOOD SAFETY / SUPPLY CONTAMINATION ───────────────────────────────────
    ("Melamine contamination detected in infant formula supply chain — 500 infants admitted", (5,5), (0.90,0.98), 0.5),
    ("Aflatoxin levels 50x above safe threshold in maize supply causing liver failure in Zimbabwe", (4,5), (0.87,0.96), 0.4),
    ("Mass food poisoning at school mid-day meal program in Odisha — 340 children hospitalised", (4,5), (0.85,0.95), 0.3),
    ("Cyclospora outbreak linked to imported herb produce affects 1,200 in Canada and USA", (3,4), (0.80,0.92), 0.2),
    ("Botulinum toxin contamination found in commercial honey brand distributed across 9 countries", (5,5), (0.88,0.97), 0.4),
]

# ─── Analysis templates per event type ────────────────────────────────────────

ANALYSIS_TEMPLATES = {
    "respiratory": [
        "**Epidemic Risk Analysis — WHO Epidemiologist**\n\n**1. Pathogen Type and Transmission:**\nThe pathogen exhibits respiratory droplet and aerosol transmission with an estimated R0 of 2.8–4.1. Genomic sequencing indicates {detail}. Secondary transmission in households confirmed at 38%.\n\n**2. Affected Region and Population Vulnerability:**\nThe outbreak epicenter spans {region}, with an estimated {pop}M people in the exposure zone. Vaccination coverage is at {vax}%, well below the 95% threshold for herd immunity. Elderly populations and immunocompromised individuals face disproportionate severe disease burden.\n\n**3. Containment Recommendations:**\n- Activate enhanced surveillance in neighboring provinces within 72 hours\n- Deploy rapid response teams with PPE stockpiles\n- Initiate contact tracing using digital proximity tools\n- Issue public advisory for mask use in crowded spaces\n- Coordinate with WHO Regional Office for antiviral stockpile release\n\nSEVERITY: {sev} | CONFIDENCE: {conf}",
        "**Public Health Risk Assessment — EPI-SENTRY**\n\n**Pathogen Characterization:**\nCurrent genomic data suggests {detail}. The clinical presentation includes fever, respiratory distress, and in severe cases {complication}. Case fatality rate estimated at {cfr}% in early reports.\n\n**Geographic and Demographic Risk:**\nPrimary affected zones: {region}. High-density urban settlements face amplification risk. Healthcare worker infections represent {hw}% of reported cases — a concerning nosocomial signal.\n\n**Immediate Action Plan:**\n- Ring vaccination with available countermeasures\n- Strict cohorting of confirmed cases in isolation wards\n- Cross-border alert issued to neighboring health ministries\n- WHO GOARN activation recommended if trend continues 72h\n\nSEVERITY: {sev} | CONFIDENCE: {conf}",
    ],
    "vectorborne": [
        "**Vector-Borne Disease Risk Assessment**\n\n**1. Pathogen and Vector Dynamics:**\nThe outbreak is driven by {vector} activity amplified by {climate_factor}. Serotype distribution suggests {detail}. Vector indices (Breteau Index) in affected districts exceed WHO threshold of 5.\n\n**2. Regional Vulnerability:**\nAffected population: {region} — estimated {pop}M exposed. Immunologically naive population due to serotype shift increases severe disease risk. Healthcare system capacity is at {capacity}% utilization.\n\n**3. Control Measures:**\n- Emergency fogging and larviciding operations in hotspot districts\n- Hospitalization protocol for early warning signs (tourniquet test positive)\n- Bed net distribution in rural clusters\n- Cross-sector coordination with environment ministry on standing water elimination\n\nSEVERITY: {sev} | CONFIDENCE: {conf}",
    ],
    "waterborne": [
        "**Waterborne Disease Risk Assessment — EPI-SENTRY**\n\n**1. Source and Pathogen:**\nLaboratory confirmation identifies {pathogen}. Environmental sampling of water supply shows contamination at {contam_level} CFU/100mL — {x}x above safe drinking water threshold. Outbreak onset curves suggest a point-source exposure event.\n\n**2. Affected Population:**\nPrimary exposure: {region}. Attack rate in exposed households: {ar}%. Risk of amplification in {secondary_risk} communities if water treatment disruption persists.\n\n**3. Response Requirements:**\n- Immediate boil-water advisory for affected zones\n- ORS/IV fluid pre-positioning for projected clinical surge\n- Rapid WASH assessment team deployment\n- Fecal-oral route interruption through handwashing stations\n- Epidemiological investigation to confirm source and trace secondary cases\n\nSEVERITY: {sev} | CONFIDENCE: {conf}",
    ],
    "hemorrhagic": [
        "**Viral Hemorrhagic Fever Emergency Assessment**\n\n**1. Pathogen Profile:**\nVirus: {pathogen}. Transmission route: direct contact with body fluids and {route}. Incubation period: {incub} days. Case fatality rate in current cluster: {cfr}%.\n\n**2. Outbreak Dynamics:**\nGeographic spread: {region}. Healthcare worker cases: {hw} confirmed — indicates critical IPC failure. Contact list currently at {contacts} persons under monitoring. Community trust index low — risk of hidden chains of transmission.\n\n**3. Critical Actions:**\n- Immediate BARRIER NURSING protocols in all treatment facilities\n- Evacuation of non-essential personnel from affected zones\n- Deployment of PPE kits to frontline healthcare facilities within 24 hours\n- Activation of WHO GOARN and MSF Emergency Coordination Center\n- Community engagement via local leaders to reduce unsafe burial practices\n- Genomic sequencing to confirm strain identity and vaccine match\n\n⚠️ THIS REPRESENTS A POTENTIAL PHEIC-TRIGGERING EVENT IF SPREAD CONTINUES\n\nSEVERITY: {sev} | CONFIDENCE: {conf}",
    ],
    "amr": [
        "**Antimicrobial Resistance Risk Assessment — EPI-SENTRY**\n\n**1. Pathogen and Resistance Profile:**\nOrganism: {pathogen}. Resistance mechanism: {mechanism}. Susceptibility profile: resistant to {resistant_to}, with intermediate sensitivity only to {sensitive_to}. ESBL/carbapenemase genes confirmed by WGS.\n\n**2. Transmission and Healthcare Risk:**\nHealthcare setting transmission confirmed in {facilities} facilities. Mortality in bloodstream infections: {mortality}%. Horizontal gene transfer to commensal organisms documented — risk of community spread.\n\n**3. Containment Protocol:**\n- Immediate cohorting of colonized/infected patients\n- Enhanced environmental decontamination with sporicidal agents\n- Antibiotic stewardship audit across affected institutions\n- Notification to national AMR surveillance committee\n- Contact screening of roommates and close contacts in ICU\n\nSEVERITY: {sev} | CONFIDENCE: {conf}",
    ],
    "general": [
        "**Epidemiological Risk Assessment — EPI-SENTRY AI Pipeline**\n\n**1. Pathogen and Transmission Analysis:**\nEvent classification: {classification}. Current evidence suggests {detail}. Transmission potential: {r0_range}. Cross-border spread risk: {spread_risk}.\n\n**2. Population Vulnerability Assessment:**\nAffected zone: {region}. Estimated at-risk population: {pop}M. Healthcare system strain index: {strain}/10. Vaccination gap: {vax_gap}% below WHO-recommended threshold.\n\n**3. Recommended Public Health Actions:**\n- Activate emergency operations center at national level\n- Mobilize rapid response teams within 24–48 hours\n- Initiate enhanced case finding and contact tracing\n- Pre-position medical countermeasures at regional warehouses\n- Issue risk communication guidance to frontline workers\n- Establish EWARN (Early Warning Alert and Response Network) reporting\n\nSEVERITY: {sev} | CONFIDENCE: {conf}",
    ],
}

CONVERGENCE_WARNINGS = [
    "⚠️ CONVERGENCE WARNING: The detected epidemic event correlates strongly with an active ECO-SENTRY flood event in the same geographic region. Flooded infrastructure is disrupting disease surveillance and ORS supply chains, creating a compound crisis that significantly elevates mortality risk beyond individual-sector projections.",
    "⚠️ CONVERGENCE WARNING: Cross-domain correlation detected between this outbreak and a SUPPLY-SENTRY alert on medical PPE shortages in the same region. Healthcare worker protection failures will amplify nosocomial transmission, accelerating the outbreak trajectory.",
    "⚠️ CONVERGENCE WARNING: This EPI-SENTRY event intersects with an ongoing ECO-SENTRY drought alert causing water scarcity. Waterborne disease vectors thrive under water-stress conditions where communities rely on unsafe sources, creating a disease amplification feedback loop.",
    "⚠️ CONVERGENCE WARNING: Cross-sector risk identified with SUPPLY-SENTRY alert on vaccine cold-chain disruptions in the affected country. Compromised immunization coverage will lower population protection precisely when the pathogen is circulating.",
    "⚠️ CONVERGENCE WARNING: The outbreak zone overlaps with a documented conflict event flagged by ECO-SENTRY. Population displacement, crowding in refugee settings, and healthcare infrastructure destruction are known amplifiers of epidemic spread — composite risk is CRITICAL.",
    "⚠️ CONVERGENCE WARNING: A concurrent SUPPLY-SENTRY alert on antibiotic shortage in the importing country combined with this AMR event creates a catastrophic treatment gap scenario. Patients requiring last-line antibiotics face effective zero treatment availability.",
    "⚠️ CONVERGENCE WARNING: This hemorrhagic fever event correlates with ECO-SENTRY deforestation alerts in the same biome, indicating accelerated zoonotic spillover risk. Habitat destruction is driving human-wildlife interfaces closer, increasing frequency of novel pathogen emergence events.",
    "⚠️ CONVERGENCE WARNING: The food security ECO-SENTRY alert overlapping with this cholera event signals severe compound vulnerability — malnourished populations have significantly higher severity and case fatality rates for diarrheal disease, amplifying both outbreak impact and healthcare burden.",
]

REGIONS = [
    "South Asia (India, Bangladesh, Nepal)", "Southeast Asia (Vietnam, Thailand, Cambodia)",
    "Sub-Saharan Africa (DRC, Nigeria, Ethiopia)", "West Africa (Guinea, Sierra Leone, Liberia)",
    "South America (Brazil, Colombia, Peru)", "Middle East (Yemen, Syria, Iraq)",
    "East Africa (Kenya, Somalia, Sudan)", "Central Asia (Pakistan, Afghanistan)",
    "Southeast Europe (Turkey, Romania, Greece)", "Horn of Africa (Ethiopia, Eritrea, Djibouti)",
    "Sahel Region (Mali, Niger, Burkina Faso)", "Great Lakes Region (DRC, Uganda, Rwanda)",
    "South Asia (India — BIMARU States)", "Caribbean (Haiti, Dominican Republic)",
    "Pacific Islands (Papua New Guinea, Solomon Islands)", "Central America (Guatemala, Honduras)",
    "North Africa (Libya, Egypt, Tunisia)", "East Asia (China — Yunnan, Guangdong)",
    "Indian subcontinent cross-border zone", "Persian Gulf region"
]

# ─── Helper functions ─────────────────────────────────────────────────────────

def random_date(start: datetime, end: datetime) -> datetime:
    delta = end - start
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=random_seconds)

def fill_analysis(template: str, sev: int, conf: float) -> str:
    replacements = {
        "{detail}": random.choice([
            "antigenic drift in hemagglutinin HA1 domain",
            "novel reassortant genome with avian-origin PB2 gene",
            "mutations at positions 627K and 701N conferring mammalian adaptation",
            "deletion in NSP3 consistent with enhanced immune evasion",
        ]),
        "{region}": random.choice(REGIONS),
        "{pop}": str(random.randint(5, 200)),
        "{vax}": str(random.randint(18, 72)),
        "{complication}": random.choice(["cytokine storm", "ARDS", "multi-organ failure", "septic shock"]),
        "{cfr}": f"{random.uniform(2.1, 38.7):.1f}",
        "{hw}": str(random.randint(8, 35)),
        "{capacity}": str(random.randint(72, 99)),
        "{vector}": random.choice(["Aedes aegypti", "Anopheles gambiae", "Culex quinquefasciatus"]),
        "{climate_factor}": random.choice(["above-average rainfall", "urban heat island effect", "unusual monsoon patterns"]),
        "{pathogen}": random.choice(["Vibrio cholerae O1 El Tor", "Salmonella Typhi", "Ebola Zaire", "Marburg marburgvirus", "Klebsiella pneumoniae NDM-1"]),
        "{contam_level}": str(random.randint(450, 8400)),
        "{x}": str(random.randint(45, 840)),
        "{ar}": f"{random.uniform(12.0, 67.0):.1f}",
        "{secondary_risk}": random.choice(["peri-urban", "downstream riverine", "camp-dwelling"]),
        "{route}": random.choice(["bushmeat handling", "unsafe burial practices", "nosocomial contact"]),
        "{incub}": f"{random.randint(3, 21)}",
        "{contacts}": str(random.randint(40, 800)),
        "{mechanism}": random.choice(["NDM-1 metallo-beta-lactamase", "OXA-48 carbapenemase", "MCR-1 plasmid colistin resistance", "VIM-producing Pseudomonas"]),
        "{resistant_to}": random.choice(["all beta-lactams, fluoroquinolones, and aminoglycosides", "carbapenems, cephalosporins, and monobactams"]),
        "{sensitive_to}": random.choice(["fosfomycin (variable)", "ceftazidime-avibactam at high MIC", "none — pan-resistant"]),
        "{facilities}": str(random.randint(2, 18)),
        "{mortality}": f"{random.uniform(28.0, 67.0):.1f}",
        "{classification}": random.choice(["novel zoonotic spillover event", "healthcare-associated outbreak", "community-amplified epidemic", "point-source foodborne cluster"]),
        "{r0_range}": random.choice(["1.8–3.2", "2.1–4.5", "3.0–6.1", "1.2–2.4"]),
        "{spread_risk}": random.choice(["HIGH — international air travel hubs nearby", "MODERATE — land border porosity significant", "CRITICAL — displacement population movement ongoing"]),
        "{strain}": str(random.randint(6, 10)),
        "{vax_gap}": f"{random.uniform(15.0, 55.0):.0f}",
        "{sev}": str(sev),
        "{conf}": f"{conf:.2f}",
    }
    for placeholder, value in replacements.items():
        template = template.replace(placeholder, value)
    return template

def pick_analysis_key(headline: str) -> str:
    hl = headline.lower()
    if any(k in hl for k in ["influenza", "covid", "mers", "pneumonia", "rsv", "corona", "respiratory", "tb", "tuberculosis", "legionnaire"]):
        return "respiratory"
    if any(k in hl for k in ["dengue", "malaria", "zika", "chikungunya", "west nile", "yellow fever", "leishmani", "japanese encephalitis", "rift valley"]):
        return "vectorborne"
    if any(k in hl for k in ["cholera", "typhoid", "e. coli", "hepatitis a", "salmonella", "norovirus", "cryptosporidium", "listeria", "rotavirus"]):
        return "waterborne"
    if any(k in hl for k in ["ebola", "marburg", "lassa", "hemorrhagic", "nipah", "hantavirus", "crimean"]):
        return "hemorrhagic"
    if any(k in hl for k in ["amr", "resistant", "mrsa", "candida", "klebsiella", "carbapenem", "colistin", "drug-resistant"]):
        return "amr"
    return "general"

# ─── Generate 750 records ─────────────────────────────────────────────────────

def generate_dataset(n: int = 750) -> list:
    alerts = []
    end_date = datetime(2026, 3, 30, 23, 59, 59)

    for i in range(n):
        # Pick a base event template (cycle through with variation)
        event_template = EPI_EVENTS[i % len(EPI_EVENTS)]
        headline, sev_range, conf_range, conv_prob = event_template

        # Add variation to headline for uniqueness
        location_prefixes = [
            "India —", "Bangladesh —", "Nigeria —", "DRC —", "Pakistan —",
            "Indonesia —", "Brazil —", "Ethiopia —", "Kenya —", "Sudan —",
            "Vietnam —", "Philippines —", "Cambodia —", "Myanmar —", "Nepal —",
            "Yemen —", "Syria —", "Haiti —", "Somalia —", "Afghanistan —",
            "Colombia —", "Peru —", "Guinea —", "Uganda —", "Mozambique —",
            "WHO Alert:", "ProMED Flash:", "ECDC Rapid Risk Assessment:", "CDC Health Advisory:",
            "GOARN Alert:", "ReliefWeb:", "IFRC Bulletin:", "OCHA Flash Update:",
            "MSF Emergency:", "Médecins Sans Frontières:"
        ]
        time_prefixes = [
            "", "", "",  # empty most of the time
            "(UPDATED) ", "(BREAKING) ", "(CONFIRMED) ", "(ESCALATING) ",
        ]

        variant_headline = f"{random.choice(time_prefixes)}{random.choice(location_prefixes)} {headline}"
        if len(variant_headline) > 220:
            variant_headline = variant_headline[:217] + "..."

        severity = random.randint(*sev_range)
        confidence = round(random.uniform(*conf_range), 2)
        is_verified = random.random() < (0.65 + confidence * 0.25)

        # Generate timestamp spread across ~18 months
        ts = random_date(BASE_DATE, end_date)
        timestamp_str = ts.isoformat()

        # Analysis text
        analysis_key = pick_analysis_key(headline)
        template_pool = ANALYSIS_TEMPLATES.get(analysis_key, ANALYSIS_TEMPLATES["general"])
        raw_analysis = fill_analysis(random.choice(template_pool), severity, confidence)

        # Convergence warning (only some alerts have it)
        has_convergence = random.random() < conv_prob
        convergence_warning = random.choice(CONVERGENCE_WARNINGS) if has_convergence else None

        alert = {
            "id": str(uuid.uuid4()),
            "headline": variant_headline,
            "mode": "epi",
            "severity": severity,
            "confidence": confidence,
            "is_verified": is_verified,
            "source": random.choice([
                "Live Agent Pipeline",
                "WHO Health Alert RSS",
                "ProMED-mail Feed",
                "ECDC Epidemic Intelligence",
                "CDC Global Disease Detection",
                "ReliefWeb Health Alerts",
                "HealthMap Automated Ingestion",
                "GOARN Partner Feed",
            ]),
            "timestamp": timestamp_str,
            "analysis": raw_analysis[:800],  # Match the 800-char truncation in notify_node
            "convergence_warning": convergence_warning,
        }
        alerts.append(alert)

    # Sort newest first (as the live pipeline would produce)
    alerts.sort(key=lambda x: x["timestamp"], reverse=True)
    return alerts

# ─── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("═══════════════════════════════════════════════════")
    print("  GlobalSentry — EPI-SENTRY Dataset Generator")
    print("  Generating 750 epidemiological alert records...")
    print("═══════════════════════════════════════════════════")

    dataset = generate_dataset(750)

    output_path = "epi_sentry_dataset.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Done! {len(dataset)} EPI-SENTRY alerts written to: {output_path}")
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
    print(f"   Severity 4-5      : {sum(1 for s in severities if s >= 4)} alerts")
    print(f"\n📡 Source distribution:")
    for src, count in sorted(sources.items(), key=lambda x: -x[1]):
        print(f"   {src[:45]:<45} : {count}")
    print(f"\n   Date range: {dataset[-1]['timestamp'][:10]} → {dataset[0]['timestamp'][:10]}")
    print("\n💡 Load into your dashboard:")
    print("   cp epi_sentry_dataset.json alerts.json")
    print("   # or import in your web dashboard API")
