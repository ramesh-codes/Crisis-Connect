import os
import json
from flask import Flask, request, jsonify, send_from_directory
from google import genai
from datetime import datetime
import uuid

app = Flask(__name__, static_folder='static')

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

alerts = []

SYSTEM_PROMPT = """You are CrisisConnect AI, an emergency response coordinator for India.
When given a disaster report, respond with a structured JSON object ONLY (no markdown, no extra text):
{
  "severity": "LOW|MEDIUM|HIGH|CRITICAL",
  "immediate_actions": ["action1", "action2", "action3"],
  "resources_needed": ["resource1", "resource2", "resource3"],
  "estimated_affected": "number or range of people",
  "key_contacts": ["NDRF: 011-24363260", "NDMA Helpline: 1078"],
  "evacuation_required": true,
  "summary": "2-3 sentence summary of the situation and response"
}"""

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/api/analyze", methods=["POST"])
def analyze():
    data = request.json
    disaster_type = data.get("disaster_type", "")
    location = data.get("location", "")
    description = data.get("description", "")
    severity_reported = data.get("severity", "")

    if not client:
        demo = {
            "severity": "HIGH",
            "immediate_actions": [
                "Evacuate low-lying areas immediately",
                "Deploy NDRF teams to affected zones",
                "Set up emergency relief camps at designated centers"
            ],
            "resources_needed": [
                "Rescue boats and life jackets",
                "Medical teams with first aid supplies",
                "Food, water, and temporary shelter"
            ],
            "estimated_affected": "5,000 - 10,000 people",
            "key_contacts": ["NDRF: 011-24363260", "NDMA Helpline: 1078", "State Disaster Authority: 1077"],
            "evacuation_required": True,
            "summary": f"A {disaster_type} has been reported in {location}. Immediate evacuation and rescue operations are required. NDRF teams should be deployed within 2 hours."
        }
        alert_id = str(uuid.uuid4())[:8]
        alerts.append({
            "id": alert_id,
            "disaster_type": disaster_type,
            "location": location,
            "description": description,
            "severity_reported": severity_reported,
            "ai_response": demo,
            "timestamp": datetime.now().isoformat(),
            "status": "ACTIVE"
        })
        return jsonify({"alert_id": alert_id, "analysis": demo})

    try:
        prompt = f"""{SYSTEM_PROMPT}

Disaster Report:
Type: {disaster_type}
Location: {location}
Severity: {severity_reported}
Description: {description}

Provide emergency response guidance as JSON only."""

        response = client.models.generate_content(
            model="gemini-2.5-flash-preview-04-17",
            contents=prompt
        )

        raw = response.text.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()
        analysis = json.loads(raw)

        alert_id = str(uuid.uuid4())[:8]
        alerts.append({
            "id": alert_id,
            "disaster_type": disaster_type,
            "location": location,
            "description": description,
            "severity_reported": severity_reported,
            "ai_response": analysis,
            "timestamp": datetime.now().isoformat(),
            "status": "ACTIVE"
        })
        return jsonify({"alert_id": alert_id, "analysis": analysis})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/alerts", methods=["GET"])
def get_alerts():
    return jsonify(alerts[-20:])

@app.route("/api/alerts/<alert_id>/resolve", methods=["POST"])
def resolve_alert(alert_id):
    for alert in alerts:
        if alert["id"] == alert_id:
            alert["status"] = "RESOLVED"
            return jsonify({"success": True})
    return jsonify({"error": "Not found"}), 404

@app.route("/health")
def health():
    return jsonify({"status": "ok", "version": "1.0.0"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
