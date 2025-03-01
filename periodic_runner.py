#!/usr/bin/env python
import sys
from datetime import datetime, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler
from src.pipelines.periodic_pipeline import periodic_pipeline
from src.logger import get_logger

# Get our custom logger
custom_logger = get_logger()

def run_periodic_pipeline():
    try:
        custom_logger.info("Starting periodic pipeline execution...")
        periodic_pipeline()
        custom_logger.info("Periodic pipeline execution completed successfully.")
    except Exception as ex:
        custom_logger.error(f"Error in periodic pipeline: {ex}", exc_info=True)

def main():
    scheduler = BlockingScheduler()
    
    # Schedule the job to run immediately (1 second from now)
    scheduler.add_job(
        run_periodic_pipeline,
        'date',
        run_date=datetime.now() + timedelta(seconds=1),
        id='initial_pipeline'
    )
    
    # Schedule the job to run every 24 minutes thereafter
    scheduler.add_job(
        run_periodic_pipeline,
        'interval',
        minutes=24,
        id='periodic_pipeline',
        replace_existing=True
    )
    
    custom_logger.info("Periodic pipeline scheduler started; initial job scheduled immediately, then every 24 minutes.")
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        custom_logger.info("Shutting down periodic pipeline scheduler...")
        scheduler.shutdown()
        sys.exit()

if __name__ == '__main__':
    main()
