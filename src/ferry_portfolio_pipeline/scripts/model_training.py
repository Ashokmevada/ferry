from prophet import Prophet
from ferry_portfolio_pipeline.logging.logger import logging as logger
from ferry_portfolio_pipeline.exception import CustomException
import pandas as pd

def train_final_model(train_df: pd.DataFrame, params: dict, config: dict):
    try:
        logger.info(" Training final Prophet model...")

        model = Prophet(
            yearly_seasonality=config["yearly_seasonality"],
            seasonality_mode=config["seasonality_mode"],
            changepoint_prior_scale=params["changepoint_prior_scale"],
            seasonality_prior_scale=params["seasonality_prior_scale"]
        )
        model.fit(train_df)

        logger.info("✅ Final model training completed.")
        return model

    except Exception as e:
        logger.error(f"❌ Model training error: {e}")
        raise CustomException(e)
