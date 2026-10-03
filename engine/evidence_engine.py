EVIDENCE_CHECKLIST = {
    "financial-fraud": [
        "Bank transaction screenshot",
        "Transaction ID / UTR number",
        "Fraudster phone number",
        "SMS or email received from the fraudster",
        "Bank account or UPI details used by the fraudster"
    ],

    "digital-arrest": [
        "Screenshots of video calls",
        "Fraudster phone numbers",
        "WhatsApp or other chat messages",
        "Payment receipts",
        "Threatening messages or documents"
    ],

    "phishing": [
        "Suspicious URL",
        "Phishing email or SMS",
        "Screenshot of the fake website",
        "Account login alerts",
        "Any information entered on the website"
    ],

    "account-hacking": [
        "Login alert emails or SMS",
        "Unknown device/session details",
        "Suspicious messages sent from your account",
        "Password reset notifications",
        "Screenshots of the compromised account"
    ]
}


def get_evidence_checklist(crime_type):
    return EVIDENCE_CHECKLIST.get(
        crime_type,
        [
            "Screenshots of the incident",
            "Phone numbers or email addresses involved",
            "Messages or emails related to the incident",
            "Transaction details, if money was involved",
            "Any other relevant documents or files"
        ]
    )