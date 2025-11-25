from src.ingest.yelp_client import ingest_business, ingest_reviews       
from src.utils.logging import get_logger 

logger = get_logger("ingest")

def run():
    logger.info("Starting ingest pipeline")
    
    ingest_business(limit=5000)
    ingest_reviews(limit=10000)

    logger.info("Ingest pipeline finished")

if __name__ == "__main__":
    run()
