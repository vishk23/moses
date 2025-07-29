import subprocess
import os
import sys
from pathlib import Path
from celery import shared_task
from django.utils import timezone
from myapp.models import BeatHealth
from django.core.cache import cache
import logging
import json

logger = logging.getLogger(__name__)

@shared_task
def run_module_task(module, cwd):
    """
    Run a Python module from a specified cwd with cross-platform compatibility.

    Example:
    {"module": "src.main", "cwd": "/full/path/to/project1"}

    """
    logger.info(f"Starting task at {cwd}: {module} at {timezone.localtime()}")
    # Convert the cwd string to a Path object
    cwd_path = Path(cwd)
    
    # Validate the directory exists
    if not cwd_path.is_dir():
        logger.error(f"Task failed: Invalid cwd {cwd}")
        raise ValueError(f"Invalid cwd: {cwd}")
    
    # Use the same Python environment as the Celery worker
    python_exe = sys.executable
    
    # Store the original cwd to restore later
    original_cwd = Path.cwd()
    try:
        # Change to the specified cwd using Path
        os.chdir(cwd_path)
        # Run the module (e.g., python -m src.main)
        subprocess.run([python_exe, '-m', module], check=True)
        logger.info(f"Finished task at {cwd}: {module} at {timezone.localtime()} with success")
    except subprocess.CalledProcessError as e:
        logger.error(f"Task at {cwd}: {module} failed at {timezone.localtime()} with error: {e}")
        raise
    except Exception as e:
        logger.error(f"Task at {cwd}: {module} failed at {timezone.localtime()} with error: {e}")
        raise
    finally:
        # Restore the original cwd
        os.chdir(original_cwd)
    
@shared_task
def run_modules_in_sequence(tasks):
    """
    Expects a JSON list of objects, each with module and cwd:
    
    Example:
    {
        "tasks": [
            {"module":"src.early_payoff_report","cwd":"\\\\00-da1\\Home\\Share\\Data & Analytics Initiatives\\Project Management\\Indirect_Lending\\Dealer Reserve Recon\\Production"},
            {"module":"src.daily_processing","cwd":"\\\\00-da1\\Home\\Share\\Data & Analytics Initiatives\\Project Management\\Indirect_Lending\\Dealer Reserve Recon\\Production"},
            {"module":"src.report_generator","cwd":"\\\\00-da1\\Home\\Share\\Data & Analytics Initiatives\\Project Management\\Indirect_Lending\\Dealer Reserve Recon\\Production"}  
    ]
    }
    """

    for task in tasks:
        run_module_task(**task)
        
@shared_task
def update_beat_heartbeat():
    now = timezone.now()
    cache.set('beat_heartbeat', now, timeout=300)  # 5-minute timeout
    # logger.info(f"Updated beat_heartbeat to {now}")

@shared_task
def run_on_demand_task(email, key, additions, deletes):
    """Run the on-demand Python script with the provided parameters."""
    module = "src.main"  # Adjust to your script's module
    cwd = Path(r"\\00-da1\Home\Share\Data & Analytics Initiatives\Project Management\Commercial_Lending\Status Page\Production")  # Adjust to your script's directory
    logger.info(f"Starting task at {cwd}: {module} with at {timezone.localtime()}")

    # Convert cwd to Path object and validate
    cwd_path = Path(cwd)
    if not cwd_path.is_dir():
        logger.error(f"Invalid cwd: {cwd}")
        raise ValueError(f"Invalid cwd: {cwd}")

    # Use the same Python executable as the worker
    python_exe = sys.executable

    # Construct the command
    command = [python_exe, "-m", module, "--email", email, "--key", str(key)]
    if additions:
        command += ["--additions"] + [str(x) for x in additions]
    if deletes:
        command += ["--deletes"] + [str(x) for x in deletes]

    # Store and change cwd
    original_cwd = Path.cwd()
    try:
        os.chdir(cwd_path)
        subprocess.run(command, check=True)
        logger.info(f"Successfully ran status_page for email: {email}, key: {key}, additions: {additions}, deletes: {deletes}")
        logger.info(f"Finished task at {cwd}: {module} at {timezone.localtime()} with success")
    except subprocess.CalledProcessError as e:
        logger.error(f"Task at {cwd}: {module} failed at {timezone.localtime()} with error: {e}")
        raise
    finally:
        os.chdir(original_cwd)