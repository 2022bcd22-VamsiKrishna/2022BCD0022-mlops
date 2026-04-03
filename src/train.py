import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
import argparse
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score

def main(args):
    mlflow.set_tracking_uri("http://localhost:5000") 
    mlflow.set_experiment("2022BCD0022_experiment")

    with mlflow.start_run(run_name=args.run_name):
        # 1. Load Data
        df = pd.read_csv('data/housing.csv')
        dataset_size = len(df)
        
        # 2. Feature Selection
        if args.drop_feature:
            df = df.drop(columns=[args.drop_feature])
            mlflow.log_param("dropped_feature", args.drop_feature)
        else:
            mlflow.log_param("dropped_feature", "None")

        X = df.drop('MedHouseVal', axis=1) # Target column in California Housing
        y = df['MedHouseVal']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # 3. Select Model
        mlflow.log_param("model_type", args.model_type)
        if args.model_type == "RF":
            model = RandomForestRegressor(n_estimators=args.n_estimators, max_depth=args.max_depth, random_state=42)
            mlflow.log_param("n_estimators", args.n_estimators)
            mlflow.log_param("max_depth", args.max_depth)
        elif args.model_type == "GB":
            model = GradientBoostingRegressor(n_estimators=args.n_estimators, max_depth=args.max_depth, random_state=42)
            mlflow.log_param("n_estimators", args.n_estimators)
            mlflow.log_param("max_depth", args.max_depth)

        # 4. Train & Predict
        model.fit(X_train, y_train)
        preds = model.predict(X_test)

        # 5. Calculate & Log Metrics
        rmse = np.sqrt(mean_squared_error(y_test, preds))
        r2 = r2_score(y_test, preds)

        mlflow.log_metric("dataset_size", dataset_size)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2_score", r2)

        # Log Model
        mlflow.sklearn.log_model(model, "model")
        
        print(f"Run: {args.run_name} | Size: {dataset_size} | Model: {args.model_type} | RMSE: {rmse:.4f} | R2: {r2:.4f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--run_name", type=str, required=True)
    parser.add_argument("--model_type", type=str, default="RF", choices=["RF", "GB"])
    parser.add_argument("--n_estimators", type=int, default=100)
    parser.add_argument("--max_depth", type=int, default=None)
    parser.add_argument("--drop_feature", type=str, default="")
    args = parser.parse_args()
    main(args)