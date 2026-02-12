from pathlib import Path
import sys
import pandas as pd

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.utils.logging import get_logger

logger = get_logger("feature_pipeline")

BASE_DIR = Path(__file__).resolve().parents[2]
INTERIM_DIR = BASE_DIR / "data" / "interim" / "yelp"
PROCESSED_DIR = BASE_DIR / "data" / "processed"


def build_features(business_path: Path | None = None, review_path: Path | None = None) -> Path:
    business_path = business_path or (INTERIM_DIR / "business.parquet")
    review_path = review_path or (INTERIM_DIR / "review.parquet")

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    logger.info(f"Loading business from {business_path}")
    df_b = pd.read_parquet(business_path)
    logger.info(f"Loading reviews from {review_path}")
    df_r = pd.read_parquet(review_path)

    # basic aggregation: review counts and average rating
    logger.info("Aggregating review stats")
    review_stats = df_r.groupby("business_id").agg(
        review_count_agg=("business_id", "count"),
        avg_rating=("stars", "mean")
    ).reset_index()

    logger.info("Merging business and review stats")
    merged = df_b.merge(review_stats, on="business_id", how="left", suffixes=("_biz", "_agg"))
    
    # Use aggregated review count, fallback to business review count if available
    if "review_count_agg" in merged.columns:
        merged["review_count"] = merged["review_count_agg"].fillna(0).astype(int)
    elif "review_count" in merged.columns:
        merged["review_count"] = merged["review_count"].fillna(0).astype(int)
    
    merged["avg_rating"] = merged["avg_rating"].fillna(merged["avg_rating"].median())

    # simple label for demo: trending if review_count > median
    median_rc = merged["review_count"].median()
    merged["is_trending"] = (merged["review_count"] > median_rc).astype(int)

    out_path = PROCESSED_DIR / "features.parquet"
    merged.to_parquet(out_path, index=False)
    logger.info(f"Wrote features to {out_path}")
    return out_path


if __name__ == "__main__":
    build_features()
