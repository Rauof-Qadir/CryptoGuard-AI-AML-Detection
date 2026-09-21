def transaction_report(row):

    report = f"""

Transaction ID:
{row['txId']}


Risk Score:
{row['risk_score']}/100


Risk Level:
{row['risk_level']}


Reasons:
{row['risk_reason']}


Priority:
{row['priority']}

"""

    return report