from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

CRIMES = {
    "financial-fraud": {
        "title": "Financial Fraud",
        "icon": "💳",
        "description": "Money stolen through UPI, bank transfer, card or online payment.",
        "actions": [
            "Call 1930 immediately if money has been transferred.",
            "Contact your bank or payment service and report the fraudulent transaction.",
            "Do not share OTP, PIN, CVV or banking credentials.",
            "Save transaction ID, UTR number and screenshots.",
            "Report the incident through the official cybercrime portal."
        ],
        "evidence": [
            "Transaction screenshot",
            "Transaction ID / UTR",
            "Fraudster phone number",
            "UPI ID / bank details",
            "SMS or email alerts",
            "Chat screenshots"
        ]
    },

    "digital-arrest": {
        "title": "Digital Arrest Scam",
        "icon": "🚨",
        "description": "Fake police, CBI, court or government officials threatening you online.",
        "actions": [
            "Do not transfer money because of threats or video calls.",
            "Disconnect the suspicious call.",
            "Do not share Aadhaar, PAN, OTP, PIN or banking information.",
            "Save screenshots, phone numbers and messages.",
            "Report the incident through the official cybercrime portal."
        ],
        "evidence": [
            "Caller phone number",
            "Video-call screenshots",
            "WhatsApp or chat messages",
            "Fake identity cards or notices",
            "Payment details",
            "Screen recordings"
        ]
    },

    "phishing": {
        "title": "Phishing / Fake Link",
        "icon": "🎣",
        "description": "Suspicious links, fake websites, OTP or credential theft.",
        "actions": [
            "Do not open the suspicious link again.",
            "Change the password of the affected account.",
            "Enable two-factor authentication.",
            "Contact your bank if financial information was exposed.",
            "Save the suspicious URL and screenshots."
        ],
        "evidence": [
            "Suspicious URL",
            "Message containing the link",
            "Website screenshots",
            "Email sender details",
            "Login alerts",
            "Transaction details"
        ]
    },

    "account-hacking": {
        "title": "Account Hacking",
        "icon": "🔐",
        "description": "Your email, social media or online account has been compromised.",
        "actions": [
            "Change the compromised account password immediately.",
            "Sign out unknown devices and active sessions.",
            "Enable two-factor authentication.",
            "Check recovery email and phone number.",
            "Save login alerts and suspicious activity."
        ],
        "evidence": [
            "Login alerts",
            "Unknown device information",
            "Suspicious emails",
            "Changed account details",
            "Messages sent by attacker",
            "Screenshots"
        ]
    },

    "malware": {
        "title": "Malware Attack",
        "icon": "🦠",
        "description": "Suspicious APKs, spyware, malicious software or files affecting your device.",
        "actions": [
            "Disconnect the affected device from the internet if necessary.",
            "Do not open suspicious files or APKs again.",
            "Remove unknown applications after preserving evidence.",
            "Change important passwords from a trusted device.",
            "Save suspicious files and screenshots when safe."
        ],
        "evidence": [
            "Suspicious APK or file name",
            "Installation source",
            "Screenshots",
            "Suspicious application details",
            "Security alerts",
            "Messages or links"
        ]
    },

    "sim-fraud": {
        "title": "SIM / Mobile Fraud",
        "icon": "📱",
        "description": "SIM replacement, mobile takeover or suspicious telecom activity.",
        "actions": [
            "Contact your mobile operator immediately.",
            "Ask them to secure or block the affected SIM.",
            "Check banking and email accounts.",
            "Change important passwords.",
            "Preserve telecom messages and alerts."
        ],
        "evidence": [
            "SIM replacement messages",
            "Mobile operator alerts",
            "Unknown calls",
            "Banking alerts",
            "Account login alerts",
            "Screenshots"
        ]
    },

    "social-media": {
        "title": "Social Media Crime",
        "icon": "🌐",
        "description": "Fake profiles, impersonation, harassment or social media abuse.",
        "actions": [
            "Do not engage with the person unnecessarily.",
            "Block and report the suspicious account.",
            "Save the profile URL and screenshots.",
            "Preserve messages and comments.",
            "Report the incident through official channels."
        ],
        "evidence": [
            "Profile URL",
            "Username",
            "Screenshots",
            "Messages",
            "Comments",
            "Date and time"
        ]
    },

    "online-blackmail": {
        "title": "Online Blackmail / Image Abuse",
        "icon": "⚠️",
        "description": "Threats, intimate-image abuse, extortion or online harassment.",
        "actions": [
            "Do not pay the blackmailer.",
            "Do not send additional personal material.",
            "Save messages, profile information and threats.",
            "Block the person after preserving evidence.",
            "Report the incident through official channels."
        ],
        "evidence": [
            "Threatening messages",
            "Profile URL",
            "Phone number",
            "Payment demands",
            "Screenshots",
            "Relevant files or links"
        ]
    },

    "crypto-fraud": {
        "title": "Crypto Fraud",
        "icon": "₿",
        "description": "Cryptocurrency scams, fake investments or wallet-related fraud.",
        "actions": [
            "Do not send additional cryptocurrency.",
            "Preserve wallet addresses and transaction hashes.",
            "Save screenshots of the platform or investment offer.",
            "Contact the relevant exchange if applicable.",
            "Report the incident through official channels."
        ],
        "evidence": [
            "Wallet address",
            "Transaction hash",
            "Exchange details",
            "Screenshots",
            "Chat messages",
            "Investment website URL"
        ]
    },

    "email-fraud": {
        "title": "Email Fraud",
        "icon": "📧",
        "description": "Fake emails, impersonation, phishing or email account compromise.",
        "actions": [
            "Do not reply to the suspicious email.",
            "Do not open unknown attachments or links.",
            "Change your email password if compromised.",
            "Enable two-factor authentication.",
            "Save the complete email and sender information."
        ],
        "evidence": [
            "Complete email",
            "Sender address",
            "Email headers",
            "Attachments",
            "Links",
            "Screenshots"
        ]
    }
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/crime/<crime_type>")
def crime_page(crime_type):
    crime = CRIMES.get(crime_type)

    if not crime:
        return "Crime type not found", 404

    return render_template(
        "crime.html",
        crime=crime,
        guidance=crime,
        crime_type=crime_type
    )


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json() or {}
    text = data.get("text", "").strip().lower()

    if not text:
        return jsonify({
            "success": False,
            "message": "Please tell us what happened."
        })

    crime_type = detect_crime(text)
    crime = CRIMES[crime_type]

    return jsonify({
        "success": True,
        "crime_type": crime_type,
        "title": crime["title"],
        "message": "Incident identified successfully."
    })


def detect_crime(text):

    keywords = {
        "financial-fraud": [
            "money", "upi", "bank", "transaction",
            "payment", "fraud", "stolen", "debit"
        ],

        "digital-arrest": [
            "digital arrest", "police", "cbi", "court",
            "arrest", "officer", "video call"
        ],

        "phishing": [
            "phishing", "fake link", "suspicious link",
            "fake website", "otp", "link"
        ],

        "account-hacking": [
            "hacked", "hack", "account hacked",
            "instagram hacked", "facebook hacked",
            "email hacked", "compromised"
        ],

        "malware": [
            "malware", "virus", "apk", "spyware",
            "ransomware", "suspicious app"
        ],

        "sim-fraud": [
            "sim", "sim swap", "sim replacement",
            "mobile number", "network stopped"
        ],

        "social-media": [
            "fake profile", "instagram", "facebook",
            "social media", "impersonation", "harassment"
        ],

        "online-blackmail": [
            "blackmail", "blackmailing", "private photo",
            "intimate photo", "image abuse", "extortion"
        ],

        "crypto-fraud": [
            "crypto", "bitcoin", "cryptocurrency",
            "wallet", "usdt", "investment scam"
        ],

        "email-fraud": [
            "email fraud", "fake email",
            "suspicious email", "email scam"
        ]
    }

    for crime_type, words in keywords.items():
        for word in words:
            if word in text:
                return crime_type

    return "phishing"
@app.route("/report")
def report_page():
    return render_template("report.html")


@app.route("/submit-report", methods=["POST"])
def submit_report():

    data = request.get_json() or {}

    name = data.get("name", "").strip()
    phone = data.get("phone", "").strip()
    email = data.get("email", "").strip()

    incident_type = data.get(
        "incident_type", ""
    ).strip()

    description = data.get(
        "description", ""
    ).strip()

    incident_date = data.get(
        "incident_date", ""
    ).strip()

    amount = data.get(
        "amount", ""
    ).strip()

    evidence = data.get(
        "evidence", ""
    ).strip()


    # Check required fields

    if not name:
        return jsonify({
            "success": False,
            "message": "Please enter your name."
        })


    if not phone:
        return jsonify({
            "success": False,
            "message": "Please enter your phone number."
        })


    if not incident_type:
        return jsonify({
            "success": False,
            "message": "Please select the incident type."
        })


    if not description:
        return jsonify({
            "success": False,
            "message": "Please describe what happened."
        })


    if not incident_date:
        return jsonify({
            "success": False,
            "message": "Please select the incident date."
        })


    # Prepare report

    report = f"""
CYBERRAKSHA AI
CYBER INCIDENT REPORT
================================

Name:
{name}

Phone:
{phone}

Email:
{email or "Not provided"}

Incident Type:
{incident_type}

Incident Date:
{incident_date}

Financial Loss:
₹{amount if amount else "0"}

Incident Description:
{description}

Evidence:
{evidence if evidence else "Not provided"}

================================
REPORT PREPARED BY CYBERRAKSHA AI
"""


    print("\n" + report)


    return jsonify({
        "success": True,
        "message": (
            "Your cyber incident report has been "
            "prepared successfully. Please continue "
            "to the official Cyber Crime Portal or "
            "call 1930 for reporting assistance."
        )
    })

@app.route("/generate-summary", methods=["POST"])
def generate_summary():

    data = request.get_json() or {}

    incident = data.get("incident", "").strip()
    name = data.get("name", "").strip()
    phone = data.get("phone", "").strip()

    if not incident:
        return jsonify({
            "success": False,
            "message": "Please describe the incident."
        })

    crime_type = detect_crime(incident)
    crime = CRIMES[crime_type]

    summary = f"""
CYBERRAKSHA AI - CYBER INCIDENT SUMMARY

Date/Time:
{datetime.now().strftime("%d-%m-%Y %I:%M %p")}

Name:
{name or "Not provided"}

Contact:
{phone or "Not provided"}

Incident Type:
{crime["title"]}

Incident Description:
{incident}

IMMEDIATE ACTIONS:
"""

    for i, action in enumerate(crime["actions"], 1):
        summary += f"{i}. {action}\n"

    summary += "\nEVIDENCE TO PRESERVE:\n"

    for item in crime["evidence"]:
        summary += f"- {item}\n"

    summary += """

OFFICIAL REPORTING:

Cyber Crime Portal:
https://www.cybercrime.gov.in/

Cyber Crime Helpline:
1930
"""

    return jsonify({
        "success": True,
        "summary": summary
    })


if __name__ == "__main__":
    app.run(debug=True)