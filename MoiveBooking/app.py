import uvicorn
import os
from scripts.logging.logger import logger

if __name__ == "__main__":
    host = os.getenv('HOST')
    port = os.getenv('PORT')
    workers = os.getenv('WORKERS')
    logger.info("Starting Service")
    uvicorn.run("main:app", host=host, port=int(port), workers=int(workers))
    logger.info("Stopping Service")