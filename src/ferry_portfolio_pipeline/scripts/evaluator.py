import pandas as pd
import numpy as np
from prophet import Prophet
from prophet.diagnostics import cross_validation, performance_metrics
from ferry_portfolio_pipeline.logging.logger import logging as logger
from ferry_portfolio_pipeline.exception import CustomException
import mlflow
import os

def evaluate_prophet_models(df: pd.DataFrame, config: dict):
    try:
        logger.info(" Starting model evaluation...")

        # Set MLflow tracking URI and artifact root from environment variables or config
        # mlflow_tracking_uri = os.getenv("MLFLOW_TRACKING_URI")
        # mlflow_artifact_root = os.getenv("MLFLOW_ARTIFACT_ROOT")
        
        # if mlflow_tracking_uri is None or mlflow_artifact_root is None:
        #     raise CustomException("MLflow tracking URI or artifact root is not set in environment or config")

        # mlflow.set_tracking_uri(mlflow_tracking_uri)

        changepoint_values = config["changepoint_prior_scale"]
        seasonality_values = config["seasonality_prior_scale"]

        results = []

        for c in changepoint_values:
            for s in seasonality_values:
                logger.info(f"Testing changepoint_prior_scale={c}, seasonality_prior_scale={s}")

                # with mlflow.start_run(run_name=f"cps_{c}_sps_{s}", nested=True):
                model = Prophet(
                    yearly_seasonality=config["yearly_seasonality"],
                    seasonality_mode=config["seasonality_mode"],
                    changepoint_prior_scale=c,
                    seasonality_prior_scale=s
                )
                model.fit(df)

                df_cv = cross_validation(
                    model,
                    initial=config["initial"],
                    period=config["period"],
                    horizon=config["horizon"]
                )
                df_p = performance_metrics(df_cv)

                mape = np.mean(df_p['mape'])
                rmse = np.mean(df_p['rmse'])

                # Log params & metrics to MLflow
                # mlflow.log_param("changepoint_prior_scale", c)
                # mlflow.log_param("seasonality_prior_scale", s)
                # mlflow.log_metric("mape", mape)
                # mlflow.log_metric("rmse", rmse)

                # Optionally, log artifacts like plots here (if you generate any)

                results.append({
                    "changepoint_prior_scale": c,
                    "seasonality_prior_scale": s,
                    "mape": mape,
                    "rmse": rmse
                })

        result_df = pd.DataFrame(results).sort_values("mape")
        best_params = result_df.iloc[0].to_dict()

        logger.info(f"✅ Best hyperparameters found: {best_params}")

        # Log best params as separate run
        # with mlflow.start_run(run_name="best_params"):
        #     for key, val in best_params.items():
        #         if key in ["changepoint_prior_scale", "seasonality_prior_scale"]:
        #             mlflow.log_param(key, val)
        #         else:
        #             mlflow.log_metric(key, val)

        return best_params, result_df

    except Exception as e:
        logger.error(f"❌ Evaluation error: {e}")
        raise CustomException(e)
