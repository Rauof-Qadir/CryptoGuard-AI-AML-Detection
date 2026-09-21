def calculate_risk_score(row):

    score = 0


    # Rule 1
    if row["high_amount_flag"] == 1:
        score += 30


    # Rule 2
    if row["night_transaction"] == 1:
        score += 20


    # Rule 3
    if row["transaction_velocity"] > 10:
        score += 30


    return score



def risk_category(score):

    if score >= 70:
        return "HIGH"

    elif score >= 40:
        return "MEDIUM"

    else:
        return "LOW"