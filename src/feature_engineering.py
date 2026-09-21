import pandas as pd


def create_behavior_features(df):

    data = df.copy()


    # Transaction velocity

    data["transaction_velocity"] = (
        data.groupby("time")["txId"]
        .transform("count")
    )


    # Night transaction

    data["night_transaction"] = (
        (data["time"] % 24 < 6)
        .astype(int)
    )


    # High amount flag

    amount_threshold = (
        data["feature_1"].mean()
        +
        2 * data["feature_1"].std()
    )


    data["high_amount_flag"] = (
        data["feature_1"] > amount_threshold
    ).astype(int)


    return data