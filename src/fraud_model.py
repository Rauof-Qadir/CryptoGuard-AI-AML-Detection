from sklearn.ensemble import IsolationForest
import pandas as pd



def train_anomaly_model(X):

    model = IsolationForest(
        n_estimators=200,
        contamination=0.05,
        random_state=42
    )

    model.fit(X)

    return model



def predict_anomaly(model, X):

    prediction = model.predict(X)

    return prediction