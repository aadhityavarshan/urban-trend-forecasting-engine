from pathlib import Path

from src.utils.config import get_env
from src.utils.logging import get_logger
from src.warehouse.bigquery_client import load_parquet_to_bq

logger = get_logger("load_raw")

BASE_DIR = Path(__file__).resolve().parents[2]


def load_yelp():
    dataset = get_env("GCP_DATASET_ID")
    project = get_env("GCP_PROJECT_ID")
    if not dataset or not project:
        raise RuntimeError("GCP_PROJECT_ID or GCP_DATASET_ID missing")

    business_path = BASE_DIR / "data" / "interim" / "yelp" / "business.parquet"
    review_path = BASE_DIR / "data" / "interim" / "yelp" / "review.parquet"

    load_parquet_to_bq(
        table_id=f"{project}.{dataset}.yelp_business_raw",
        parquet_path=str(business_path),
    )

    load_parquet_to_bq(
        table_id=f"{project}.{dataset}.yelp_review_raw",
        parquet_path=str(review_path),
    )


if __name__ == "__main__":
    load_yelp()
