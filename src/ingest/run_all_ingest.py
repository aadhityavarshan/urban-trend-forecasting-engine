from utils.logging import get_logger

logger = get_logger("ingest")

def run():
    logger.info("Starting ingest pipeline")
    # todo: call each source client here
    logger.info("Ingest pipeline finished")

if __name__ == "__main__":
    run()
