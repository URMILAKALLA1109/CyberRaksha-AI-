CRIME_GUIDANCE = {
    "financial-fraud": {
        "title": "Financial Fraud",
        "emergency": [
            "Call 1930 immediately.",
            "Contact your bank and report the transaction.",
            "Do not share OTP, PIN, CVV, or passwords with anyone.",
            "Save transaction IDs, screenshots, SMS, and bank messages."
        ]
    },

    "digital-arrest": {
        "title": "Digital Arrest Scam",
        "emergency": [
            "Do not transfer money because of threats or video calls.",
            "Disconnect the suspicious call.",
            "Save screenshots, phone numbers, messages, and payment details.",
            "Report the incident through the official cybercrime channel."
        ]
    },

    "phishing": {
        "title": "Phishing / Fake Link",
        "emergency": [
            "Do not click the suspicious link again.",
            "Change the affected account password.",
            "Enable two-factor authentication.",
            "Save the suspicious URL, message, email, and screenshots."
        ]
    },

    "account-hacking": {
        "title": "Account Hacking",
        "emergency": [
            "Change your password immediately if you still have access.",
            "Sign out of unknown devices and sessions.",
            "Enable two-factor authentication.",
            "Save login alerts, emails, and screenshots."
        ]
    }
}


def get_crime_guidance(crime_type):
    return CRIME_GUIDANCE.get(
        crime_type,
        {
            "title": "Cyber Crime",
            "emergency": [
                "Preserve all available evidence.",
                "Do not delete suspicious messages or files.",
                "Report the incident through the official cybercrime channel."
            ]
        }
    )