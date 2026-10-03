def generate_summary(
    crime_type,
    incident_description,
    victim_name="Not provided",
    incident_date="Not provided",
    financial_loss="Not provided",
    suspect_details="Not provided"
):
    summary = {
        "crime_type": crime_type,
        "victim_name": victim_name,
        "incident_date": incident_date,
        "financial_loss": financial_loss,
        "suspect_details": suspect_details,
        "incident_description": incident_description
    }

    return summary