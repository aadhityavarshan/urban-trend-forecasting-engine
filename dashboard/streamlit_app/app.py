import streamlit as st
import pandas as pd
import joblib
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.utils.logging import get_logger

logger = get_logger("streamlit_app")

BASE_DIR = Path(__file__).resolve().parents[2]
FEATURES = BASE_DIR / "data" / "processed" / "features.parquet"
MODEL = BASE_DIR / "models" / "rf_trending.joblib"

st.set_page_config(page_title="Urban Trend Forecast", layout="wide")
st.title("🎯 Urban Trend Forecast — Emerging Venues")

if not FEATURES.exists():
    st.warning("⚠️ No features found. Run the pipeline to generate features.")
else:
    df = pd.read_parquet(FEATURES)
    
    if MODEL.exists():
        model = joblib.load(MODEL)
        X = df[[c for c in ["review_count", "avg_rating"] if c in df.columns]].fillna(0)
        if hasattr(model, "predict_proba"):
            probs = model.predict_proba(X)[:, 1]
        else:
            probs = model.predict(X)
        df["trending_score"] = probs
    else:
        st.warning("⚠️ No trained model found. Run training first.")
        df["trending_score"] = 0.5
    
    # Filter to top predicted venues
    top = df.sort_values("trending_score", ascending=False).head(20).copy()
    
    # Sidebar filters
    st.sidebar.header("Filters")
    min_score = st.sidebar.slider("Min Trending Score", 0.0, 1.0, 0.0)
    top = top[top["trending_score"] >= min_score]
    
    if len(top) == 0:
        st.warning("No venues match the selected filters.")
    else:
        # Two-column layout: Map + Metrics
        col1, col2 = st.columns([2, 1])
        
        # MAP
        with col1:
            st.subheader("📍 Top Venues on Map")
            # Prepare map data
            map_data = top[["name", "latitude", "longitude", "trending_score", "review_count", "avg_rating"]].copy()
            map_data.columns = ["name", "lat", "lon", "score", "reviews", "rating"]
            
            if "lat" in map_data.columns and "lon" in map_data.columns:
                st.map(map_data[["lat", "lon"]], zoom=12)
            else:
                st.info("Location data not available for mapping.")
        
        # KEY INSIGHTS
        with col2:
            st.subheader("📊 Key Insights")
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Top Venues", len(top))
                st.metric("Avg Trending Score", f"{top['trending_score'].mean():.2f}")
            with col_b:
                st.metric("Avg Rating", f"{top['avg_rating'].mean():.1f}/5")
                st.metric("Avg Reviews", f"{top['review_count'].mean():.0f}")
        
        st.divider()
        
        # DETAILED TABLE
        st.subheader("📋 Top Trending Venues")
        display_cols = ["name", "city", "review_count", "avg_rating", "trending_score"]
        display_data = top[display_cols].copy()
        display_data.columns = ["Venue Name", "City", "Reviews", "Rating", "Trending Score"]
        display_data["Trending Score"] = display_data["Trending Score"].apply(lambda x: f"{x:.2%}")
        display_data["Rating"] = display_data["Rating"].apply(lambda x: f"{x:.1f}/5")
        
        st.dataframe(display_data, use_container_width=True, hide_index=True)
        
        # CITY BREAKDOWN
        st.divider()
        col_charts = st.columns(2)
        
        with col_charts[0]:
            st.subheader("🏙️ Venues by City")
            city_counts = top["city"].value_counts().head(10)
            st.bar_chart(city_counts)
        
        with col_charts[1]:
            st.subheader("⭐ Rating Distribution")
            rating_bins = pd.cut(top["avg_rating"], bins=[0, 2, 3, 4, 5], labels=["0-2", "2-3", "3-4", "4-5"])
            rating_dist = rating_bins.value_counts().sort_index()
            st.bar_chart(rating_dist)
