from sklearn.ensemble import RandomForestClassifier

def train_fraud_classifier(X_train, y_train):
    model = RandomForestClassifier(
        n_estimators=200,
        class_weight="balanced",
        random_state=42
    )
    model.fit(X_train, y_train)
    return model

def predict_fraud(model, X_test):
    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)
    return predictions, probabilities