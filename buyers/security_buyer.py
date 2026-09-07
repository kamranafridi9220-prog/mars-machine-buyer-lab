def evaluate_vendor(vendor):
    """
    Hidden Buyer A policy.

    Buyer A represents a security-first enterprise procurement agent.

    IMPORTANT:
    The MARS inference system must never directly access the internal
    scoring logic below. It should only observe vendor attributes and
    the final decision returned by this function.
    """

    score = 0

    # Security and compliance preferences
    if vendor["soc2"] == 1:
        score += 25

    if vendor["iso27001"] == 1:
        score += 20

    if vendor["eu_data_residency"] == 1:
        score += 20

    # Reliability
    if vendor["uptime_sla"] >= 99.99:
        score += 15
    elif vendor["uptime_sla"] >= 99.9:
        score += 8

    # Price
    if vendor["price_per_user"] <= 70:
        score += 10
    elif vendor["price_per_user"] <= 90:
        score += 6
    elif vendor["price_per_user"] <= 110:
        score += 2

    # Support quality
    if vendor["support_hours"] <= 4:
        score += 10
    elif vendor["support_hours"] <= 12:
        score += 6
    elif vendor["support_hours"] <= 24:
        score += 3

    decision = "ACCEPT" if score >= 65 else "REJECT"

    return {
        "decision": decision,
        "score": score
    }
