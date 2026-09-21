def generate_explanation(row):

    reasons = []


    if row.get("high_amount_flag",0) == 1:
        reasons.append(
            "High transaction amount"
        )


    if row.get("night_transaction",0) == 1:
        reasons.append(
            "Night transaction activity"
        )


    if row.get("transaction_velocity",0) > 10:
        reasons.append(
            "High transaction velocity"
        )


    if row.get("degree",0) > 20:
        reasons.append(
            "Connected with large transaction network"
        )


    if len(reasons) == 0:
        reasons.append(
            "No major suspicious indicators"
        )


    return reasons



def investigation_priority(score):

    if score >= 80:
        return "URGENT"

    elif score >= 50:
        return "HIGH"

    elif score >= 30:
        return "MEDIUM"

    else:
        return "LOW"