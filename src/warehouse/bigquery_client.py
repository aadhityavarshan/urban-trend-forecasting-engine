from google.cloud import bigquery
from src.utils.logging import get_logger
from src.utils.config import get_env

logger = get_logger("bigquery_client")


def get_bq_client() -> bigquery.Client:
    project_id = get_env("GCP_PROJECT_ID")
    if not project_id:
        raise RuntimeError("GCP_PROJECT_ID not set in env")

    cred_path = get_env("GOOGLE_APPLICATION_CREDENTIALS")

    if cred_path:
        logger.info(f"Using service account credentials from {cred_path}")
        client = bigquery.Client.from_service_account_json(
            cred_path,
            project=project_id,
        )
    else:
        logger.info("Using default application credentials")
        client = bigquery.Client(project=project_id)

    return client


def load_parquet_to_bq(
    table_id: str,
    parquet_path: str,
    write_disposition: str = "WRITE_TRUNCATE",
) -> None:
    client = get_bq_client()
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.PARQUET,
        write_disposition=write_disposition,
    )

    logger.info(f"Loading {parquet_path} into {table_id}")
    with open(parquet_path, "rb") as f:
        job = client.load_table_from_file(f, table_id, job_config=job_config)
    job.result()
    logger.info("Load job done")
