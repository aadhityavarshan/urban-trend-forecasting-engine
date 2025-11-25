from pathlib import Path
import json
import pandas as pd

from src.utils.logging import get_logger

logger = get_logger("yelp_ingest")

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_YELP_DIR = BASE_DIR / "data" / "raw" / "yelp"
INTERIM_DIR = BASE_DIR / "data" / "interim" / "yelp"


def load_json_to_dataframe(path: Path, limit: int | None = None) -> pd.DataFrame:
    records = []
    with path.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if limit is not None and i >= limit:
                break
            records.append(json.loads(line))
    return pd.DataFrame.from_records(records)


def ingest_business(limit: int | None = None) -> Path:
    src = RAW_YELP_DIR / "business.json"
    dst = INTERIM_DIR / "business.parquet"

    INTERIM_DIR.mkdir(parents=True, exist_ok=True)
    logger.info(f"Loading businesses from {src}")
    df = load_json_to_dataframe(src, limit=limit)

    logger.info(f"Loaded {len(df)} businesses")
    df.to_parquet(dst, index=False)
    logger.info(f"Wrote parquet to {dst}")
    return dst


def ingest_reviews(limit: int | None = None) -> Path:
    src = RAW_YELP_DIR / "review.json"
    dst = INTERIM_DIR / "review.parquet"

    INTERIM_DIR.mkdir(parents=True, exist_ok=True)
    logger.info(f"Loading reviews from {src}")
    df = load_json_to_dataframe(src, limit=limit)

    logger.info(f"Loaded {len(df)} reviews")
    df.to_parquet(dst, index=False)
    logger.info(f"Wrote parquet to {dst}")
    return dst
