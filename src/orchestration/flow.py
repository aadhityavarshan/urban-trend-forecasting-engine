from prefect import flow, task
from src.utils.logging import get_logger

logger = get_logger("orchestration")


@task
def ingest_task():
    from src.ingest.run_all_ingest import run as run_ingest

    logger.info("Running ingest")
    run_ingest()


@task
def transform_task():
    from src.transform.feature_pipeline import build_features

    logger.info("Running transform")
    return build_features()


@task
def train_task():
    from src.models.train import train_model

    logger.info("Running train")
    return train_model()


@flow
def etl_flow():
    ingest_task()
    transform_task()
    train_task()


if __name__ == "__main__":
    etl_flow()
