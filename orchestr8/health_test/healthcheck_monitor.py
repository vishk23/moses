import requests
import schedule
import time
import logging
from logging.handlers import RotatingFileHandler
import argparse

# Set up argument parser for configurable URL and interval
parser = argparse.ArgumentParser(description='Healthcheck monitor')
parser.add_argument('--url', default='http://localhost:8000/healthcheck/', help='Healthcheck endpoint URL')
parser.add_argument('--interval', type=float, default=1, help='Interval in minutes')
args = parser.parse_args()

# Configure logging with rotating file handler
handler = RotatingFileHandler('healthcheck.log', maxBytes=10000, backupCount=5)
logging.basicConfig(handlers=[handler], level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

HEALTHCHECK_URL = args.url

def send_alert(message):
    """
    Placeholder for sending alerts (e.g., email, notification).
    Customize this function to implement your preferred alert mechanism.
    """
    logging.warning(f"ALERT: {message}")
    # Example: send_email(subject="Healthcheck Alert", body=message)

def perform_healthcheck():
    """
    Perform a healthcheck by fetching the endpoint and logging the status.
    Sends an alert if the worker is offline or if the healthcheck fails.
    """
    try:
        response = requests.get(HEALTHCHECK_URL, timeout=10)
        if response.status_code == 200:
            data = response.json()
            site_status = data.get('site')
            worker_status = data.get('worker')
            logging.info(f"Site: {site_status}, Worker: {worker_status}")
            # Check if "offline" is in the worker status
            if 'offline' in worker_status:
                send_alert(f"Worker status indicates offline: {worker_status}. Site status: {site_status}")
        else:
            logging.error(f"Healthcheck failed with status code: {response.status_code}")
            send_alert(f"Healthcheck failed with status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error connecting to healthcheck endpoint. Site offline")
        send_alert(f"Error connecting to healthcheck endpoint: Site offline")

if __name__ == '__main__':
    logging.info("Starting healthcheck monitor")
    schedule.every(args.interval).minutes.do(perform_healthcheck)
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Stopping healthcheck monitor")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")