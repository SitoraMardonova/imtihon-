import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, confusion_matrix
import pickle


df = pd.read_csv("data.csv")


df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")


df.dropna(inplace=True)  



df = df[(df["tenure"] >= 0) & (df["TotalCharges"] <= 10000)]


df.drop(columns=["customerID"], inplace=True)


df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})


num_cols = ["tenure", "MonthlyCharges", "TotalCharges"]


df_encoded = pd.get_dummies(df, drop_first=True)


scaler = StandardScaler()

existing_num_cols = [col for col in num_cols if col in df_encoded.columns]
df_encoded[existing_num_cols] = scaler.fit_transform(df_encoded[existing_num_cols])


X = df_encoded.drop("Churn", axis=1)
y = df_encoded["Churn"]


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)


log_model = LogisticRegression(max_iter=1000)
log_model.fit(X_train, y_train)
log_preds = log_model.predict(X_test)


rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
rf_preds = rf_model.predict(X_test)


def evaluate_model(name, model, preds):
    try:
        roc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])
    except ValueError:
        roc = "ROC AUC hisoblab bo‘lmadi (faqat bitta sinf)"
    return {
        "Model": name,
        "Accuracy": accuracy_score(y_test, preds),
        "F1 Score": f1_score(y_test, preds),
        "ROC AUC": roc,
        "Confusion Matrix": confusion_matrix(y_test, preds).tolist()
    }

log_metrics = evaluate_model("Logistic Regression", log_model, log_preds)
rf_metrics = evaluate_model("Random Forest", rf_model, rf_preds)


with open("best_model.pkl", "wb") as f:
    pickle.dump(rf_model, f)


print(log_metrics)
print(rf_metrics)

