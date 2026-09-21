def calculate_final_risk(
        ml_probability,
        anomaly_score,
        graph_score,
        rule_score
):


    final_score = (

        (ml_probability * 0.40)

        +

        (anomaly_score * 0.30)

        +

        (graph_score * 0.20)

        +

        (rule_score * 0.10)

    )


    return round(
        final_score,
        2
    )



def risk_level(score):

    if score >= 80:
        return "HIGH"


    elif score >= 50:
        return "MEDIUM"


    else:
        return "LOW"