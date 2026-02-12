# Urban Trend Forecasting Engine

Predict emerging urban venues before they blow up. This engine ingests Yelp data, engineers features, trains a machine learning model, and surfaces top trending venues through an interactive dashboard.

## 🎯 What It Does

- **Ingests** Yelp business & review data from JSON files → Parquet
- **Transforms** raw data into features (review counts, ratings, aggregations)
- **Trains** a RandomForest classifier to predict "trending" venues
- **Visualizes** top predicted venues on an interactive map with insights
- **Optionally loads** cleaned data to BigQuery for scalable analytics

## 🏗️ Architecture

```
Raw Data (Yelp JSON)
    ↓
[Ingest] → Interim Parquet (data/interim/yelp/)
    ↓
[Transform] → Features (data/processed/features.parquet)
    ↓
[Train] → ML Model (models/rf_trending.joblib)
    ↓
[Dashboard] → Interactive UI (Streamlit)
    ↓
[BigQuery] → Data Warehouse (optional)
```

## 📋 Requirements

- Python 3.10+
- Virtual environment (recommended)
- Google Cloud credentials (optional, for BigQuery)

## 🚀 Quick Start

### 1. Install Dependencies

```powershell
# Create virtual environment and activate
python -m venv .venv
.venv\Scripts\Activate.ps1

# Install project and dependencies
pip install -e .
```

### 2. Run the Data Pipeline

Execute the full pipeline: ingest → transform → train

```powershell
# Step 1: Ingest raw Yelp data
python src/ingest/run_all_ingest.py

# Step 2: Transform to features
python src/transform/feature_pipeline.py

# Step 3: Train model
python src/models/train.py
```

All steps complete in ~30 seconds. Check `data/processed/features.parquet` and `models/rf_trending.joblib` for outputs.

### 3. View the Dashboard

```powershell
streamlit run dashboard/streamlit_app/app.py
```

Open http://localhost:8501 to:
- 📍 See top venues on an interactive map
- 🎚️ Filter by trending score
- 📊 View metrics (avg rating, review counts, etc.)
- 🏙️ Explore city distribution and ratings

## 📁 Project Structure

```
src/
  ingest/                    # Data ingestion
    ├── yelp_client.py      # Yelp JSON → Parquet loader
    └── run_all_ingest.py   # Orchestrator
  
  transform/                 # Feature engineering
    └── feature_pipeline.py  # Raw data → features
  
  models/                    # ML training
    └── train.py            # RandomForest classifier
  
  orchestration/             # Workflow orchestration (Prefect scaffold)
    └── flow.py
  
  warehouse/                 # BigQuery integration
    ├── bigquery_client.py  # GCP client
    └── load_raw_to_warehouse.py
  
  utils/
    ├── config.py           # Environment config
    └── logging.py          # Logging setup

data/
  raw/yelp/                 # Original Yelp JSON
  interim/yelp/             # Ingested Parquet
  processed/                # Features output

dashboard/
  streamlit_app/
    └── app.py              # Interactive dashboard

tests/                       # Unit tests
  ├── test_transform.py
  └── test_train.py

dbt/                         # dbt models (scaffold)
  └── models/
      ├── staging/
      └── marts/

.github/workflows/
  └── ci.yml                # GitHub Actions CI
```

## 🔧 Advanced: Load to BigQuery

To use BigQuery as a data warehouse:

1. Create a `.env` file in the project root:
```env
GCP_PROJECT_ID=your-gcp-project-id
GCP_DATASET_ID=your_dataset_name
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
```

2. Run the warehouse loader:
```powershell
python src/warehouse/load_raw_to_warehouse.py
```

This creates:
- `yelp_business_raw` — Business data in BigQuery
- `yelp_review_raw` — Review data in BigQuery

You can then use dbt (in `dbt/models/`) to build analytics tables.

## 🧪 Run Tests

```powershell
pytest -v
```

Tests check module imports and basic functionality.

## 📊 Key Metrics Explained

| Metric | Definition |
|--------|-----------|
| **Review Count** | Total reviews for a venue |
| **Avg Rating** | Average star rating (1-5) |
| **Trending Score** | ML model's prediction (0-1); higher = more likely to trend |

## 🗺️ Dashboard Features

- **Trending Score Filter** — Sidebar slider to adjust minimum score
- **Interactive Map** — Hover over pins for venue details
- **Top Venues Table** — Sorted by trending score
- **City Breakdown** — Bar chart of venues per city
- **Rating Distribution** — Histogram of ratings

## 🚦 CI/CD

GitHub Actions workflow (`.github/workflows/ci.yml`) runs tests on push/PR. Add your own steps as needed.

## 🛣️ Next Steps

- [ ] Add dbt models for BigQuery staging/marts
- [ ] Implement continuous retraining (Prefect flows)
- [ ] Add data validation (Great Expectations)
- [ ] Deploy dashboard to Streamlit Cloud
- [ ] Add A/B testing and feedback loops
- [ ] Model monitoring and drift detection

## 📝 Environment Variables

Create a `.env` file:

```env
# Required for BigQuery
GCP_PROJECT_ID=your-project
GCP_DATASET_ID=your_dataset
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json

# Optional
LOG_LEVEL=INFO
```

## ⚠️ Security

- **Never commit** GCP credentials or `.env` to git
- Add `gcp-creds/` and `.env` to `.gitignore` (already done)
- Use Google Cloud Secret Manager in production

## 💡 How It Works

1. **Ingest**: Load Yelp JSON (5K businesses, 10K reviews) → Parquet
2. **Transform**: Aggregate reviews per business, compute features (review count, avg rating), create "trending" label
3. **Train**: RandomForest classifier on [review_count, avg_rating] → predict trending venues
4. **Dashboard**: Load predictions, visualize on map, filter, and explore

The "trending" label is simple: venues with above-median review counts. You can improve this by adding:
- Time-series features (velocity of reviews)
- Cuisine/category features
- User sentiment analysis
- External signals (social media, foot traffic)

## 📚 Libraries Used

- **pandas, numpy** — Data manipulation
- **scikit-learn** — ML training
- **streamlit** — Dashboard UI
- **google-cloud-bigquery** — Data warehouse
- **prefect** — Orchestration
- **joblib** — Model serialization

## 👥 Contributing

1. Create a feature branch
2. Make changes and add tests
3. Run `pytest` locally
4. Commit and push
5. Open a PR

## 📧 Questions?

See code comments and docstrings in `src/` modules for implementation details.
