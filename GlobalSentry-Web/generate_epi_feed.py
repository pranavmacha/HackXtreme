import random
import uuid
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
from xml.dom import minidom

TOPICS = [
    "Unexpected surge in respiratory illnesses",
    "Avian influenza (H5N1) detected in local markets",
    "Vaccine distribution bottlenecks",
    "Emerging viral strain with high transmissibility",
    "Waterborne disease outbreak following flooding",
    "Antimicrobial resistance (AMR) clusters identified",
    "Mass vaccination campaign launched",
    "Quarantine protocols activated at international terminals",
    "Zoonotic spillover event confirmed",
    "Health system capacity reaching critical thresholds"
]

LOCATIONS = [
    "New York", "London", "Paris", "Tokyo", "Mumbai", "Kinshasa", "Brasilia", 
    "Cairo", "Hanoi", "Sydney", "Geneva", "Atlanta", "Johannesburg", "Bangkok"
]

ENTITIES = [
    "WHO (World Health Organization)", "CDC (Centers for Disease Control)", 
    "Gavi, the Vaccine Alliance", "IFRC (Red Cross)", "MSF (Doctors Without Borders)", 
    "Pfizer", "Moderna", "AstraZeneca", "Local Ministry of Health", "NIH", "CEPI"
]

def generate_headline():
    topic = random.choice(TOPICS)
    loc = random.choice(LOCATIONS)
    entity = random.choice(ENTITIES)
    templates = [
        f"Critical alert: {topic} reported near {loc}, monitoring {entity} response.",
        f"{entity} issues warning over {topic.lower()} originating from {loc}.",
        f"Global health networks brace for impact as {topic.lower()} hits {loc}.",
        f"Update: {topic} at {loc} causes ripple effects for {entity} logistics.",
        f"Urgent: {entity} confirms {topic.lower()} in {loc} region."
    ]
    return random.choice(templates)

def generate_description():
    return "This is a simulated epidemiological threat intelligence report for the GlobalSentry dashboard. The incident describes ongoing health risks and their projected impact on global health security and public safety."

rss = ET.Element("rss", version="2.0")
channel = ET.SubElement(rss, "channel")

title = ET.SubElement(channel, "title")
title.text = "GlobalSentry Epidemiological Threat Feed"
link = ET.SubElement(channel, "link")
link.text = "http://globalsentry.local/epi-feed"
desc = ET.SubElement(channel, "description")
desc.text = "Real-time simulated epidemiological disruptions and threats."

now = datetime.utcnow()

for i in range(500):
    item = ET.SubElement(channel, "item")
    
    item_title = ET.SubElement(item, "title")
    item_title.text = generate_headline()
    
    item_link = ET.SubElement(item, "link")
    item_link.text = f"http://globalsentry.local/alert/epi-{uuid.uuid4()}"
    
    item_desc = ET.SubElement(item, "description")
    item_desc.text = generate_description()
    
    pub_date = ET.SubElement(item, "pubDate")
    item_time = now - timedelta(minutes=random.randint(1, 10000))
    pub_date.text = item_time.strftime("%a, %d %b %Y %H:%M:%S GMT")
    
    guid = ET.SubElement(item, "guid")
    guid.text = f"epi-{uuid.uuid4()}"

xmlstr = minidom.parseString(ET.tostring(rss)).toprettyxml(indent="  ")

with open("epi_feed.xml", "w", encoding="utf-8") as f:
    f.write(xmlstr)

print("Successfully generated epi_feed.xml with 500 items.")
