import os
import uuid
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder="static")

alerts=[]


def has(text, words):
    t=text.lower()
    return any(w in t for w in words)


def analyze_crisis(disaster_type, location, description, reported_severity):
    dtype=(disaster_type or "").lower()
    desc=(description or "").lower()

    # Respect user-selected severity first
    severity_map={
        "low":"LOW",
        "medium":"MEDIUM",
        "high":"HIGH",
        "critical":"CRITICAL"
    }

    severity=severity_map.get(
        (reported_severity or "").lower(),
        "MEDIUM"
    )

    evacuation=False
    estimated="100-500 people"

    actions=[]
    resources=[]
    contacts=[]
    risk_notes=[]

    # Description-driven modifiers
    if has(desc,["injured","casualties","dead"]):
        risk_notes.append("Medical emergency escalation")
        estimated="500-2000 people"

    if has(desc,["children","school","hospital"]):
        risk_notes.append("Priority vulnerable population response")

    if has(desc,["power outage","electricity"]):
        risk_notes.append("Utility restoration needed")

    if has(desc,["trapped","collapsed","dam breach","explosion"]):
        # Only escalate one level, not always critical
        if severity=="LOW":
            severity="MEDIUM"
        elif severity=="MEDIUM":
            severity="HIGH"

    # ---------------- Disaster specific ----------------

    if "flood" in dtype:
        evacuation=True

        actions=[
            "Move residents from low-lying zones",
            "Deploy water rescue teams",
            "Establish relief camps"
        ]

        if has(desc,["dam","overflow","breach"]):
            actions.append("Issue downstream flood warning")

        if has(desc,["road blocked","bridge"]):
            actions.append("Reroute transport corridors")

        resources=[
            "Rescue boats",
            "Relief food supplies",
            "Water purification kits"
        ]

        contacts=[
            "Flood Control:1070",
            "NDRF:011-24363260"
        ]

        summary=f"{location} flood response prioritizes evacuation, rescue and relief operations."


    elif "earthquake" in dtype:
        evacuation=True

        actions=[
            "Inspect damaged structures",
            "Deploy rescue personnel",
            "Activate trauma response"
        ]

        if has(desc,["collapsed","trapped"]):
            actions.append("Launch trapped-survivor extraction")

        resources=[
            "Search & rescue teams",
            "Medical response units",
            "Temporary shelters"
        ]

        contacts=[
            "Emergency:112",
            "NDRF Rescue"
        ]

        summary=f"Earthquake response in {location} focuses on rescue, damage control and medical support."


    elif "fire" in dtype:
        evacuation=True

        actions=[
            "Evacuate fire perimeter",
            "Deploy firefighting response",
            "Contain spread immediately"
        ]

        if has(desc,["chemical","gas"]):
            actions.append("Activate hazardous-material protocol")
            if severity=="HIGH":
                severity="CRITICAL"

        resources=[
            "Fire brigades",
            "Burn treatment support",
            "Protective gear"
        ]

        contacts=[
            "Fire:101",
            "Medical:108"
        ]

        summary=f"Fire emergency in {location} requires containment and civilian protection."


    elif "cyclone" in dtype:
        evacuation=True

        actions=[
            "Activate cyclone shelters",
            "Issue evacuation warnings",
            "Pre-position relief supplies"
        ]

        resources=[
            "Shelter support",
            "Emergency food stock",
            "Restoration crews"
        ]

        contacts=[
            "Coastal Emergency",
            "NDMA:1078"
        ]

        summary=f"Cyclone preparedness activated for {location}."


    else:
        actions=[
            "Assess emergency zone",
            "Deploy first responders",
            "Coordinate relief operations"
        ]

        resources=[
            "Medical aid",
            "Response teams",
            "Emergency supplies"
        ]

        contacts=[
            "Emergency 112",
            "NDMA 1078"
        ]

        summary=f"Emergency response initiated for {location}."


    # add description-specific resources
    if has(desc,["injured","casualties"]):
        resources.append("Additional ambulances")

    if has(desc,["food shortage","hungry"]):
        resources.append("Emergency ration supply")

    if has(desc,["power outage"]):
        resources.append("Electrical repair teams")


    return {
        "severity":severity,
        "immediate_actions":actions,
        "resources_needed":resources,
        "estimated_affected":estimated,
        "key_contacts":contacts,
        "risk_notes":risk_notes,
        "evacuation_required":evacuation,
        "summary":summary
    }


@app.route("/")
def home():
    return send_from_directory("static","index.html")


@app.route("/api/analyze",methods=["POST"])
def analyze():
    data=request.get_json()

    disaster_type=data.get("disaster_type","")
    location=data.get("location","")
    description=data.get("description","")
    severity=data.get("severity","")

    analysis=analyze_crisis(
        disaster_type,
        location,
        description,
        severity
    )

    alert_id=str(uuid.uuid4())[:8]

    alerts.append({
        "id":alert_id,
        "disaster_type":disaster_type,
        "location":location,
        "description":description,
        "severity_reported":severity,
        "ai_response":analysis,
        "timestamp":datetime.now().isoformat(),
        "status":"ACTIVE"
    })

    return jsonify({
        "alert_id":alert_id,
        "analysis":analysis
    })


@app.route("/api/alerts")
def get_alerts():
    return jsonify(alerts[-20:])


@app.route("/api/alerts/<alert_id>/resolve",methods=["POST"])
def resolve(alert_id):
    for a in alerts:
        if a["id"]==alert_id:
            a["status"]="RESOLVED"
            return jsonify({"success":True})

    return jsonify({"error":"not found"}),404


@app.route("/health")
def health():
    return jsonify({"status":"ok"})


if __name__=="__main__":
    port=int(os.environ.get("PORT",8080))
    app.run(host="0.0.0.0",port=port)