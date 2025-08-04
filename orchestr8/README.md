# Task Scheduler Project

## Project Overview

This project is designed to manage and execute Python scripts either on a schedule or on-demand through a web interface. It ensures that only one script runs at a time to avoid conflicts with shared resources, such as COM objects used for Excel/Outlook interactions. 

### Key Features
- **Scheduled Tasks**: Automatically run Python scripts at specified intervals (e.g., daily, monthly).
- **On-Demand Tasks**: Allow users to submit tasks via a web form, which are then queued and executed sequentially.
- **Single Process Execution**: Ensures only one task runs at a time to prevent resource conflicts.
- **Windows Compatibility**: Designed to run on a Windows VM with startup automation.


## Running the Application

1. **Start the Django Server** (using Waitress on Windows):
- localhost
   ```bash
   waitress-serve --host=127.0.0.1 --port=8000 django_app.wsgi:application
   ```
- production
   ```bash
   waitress-serve --port=8000 django_app.wsgi:application
   ```

2. **Start Celery Beat** (for scheduled tasks):
   ```bash
   celery -A django_app beat --loglevel=info
   ```


3. **Start the Celery Worker** (ensures only one task runs at a time):
- Synchronous
   ```bash
   celery -A django_app worker --pool=solo --loglevel=info
   ```


## Scheduling New Tasks via Admin Panel
Single Report (sequence doesn't matter)
```json
{"module": "src.main", "cwd": "\\\\00-da1\\Path\\To\\Project"}
```

Chaining Reports
```json
{
   "tasks": [
      {"module":"src.early_payoff_report","cwd":"\\\\00-da1\\Home\\Share\\Data & Analytics Initiatives\\Project Management\\Indirect_Lending\\Dealer Reserve Recon\\Production"},
      {"module":"src.daily_processing","cwd":"\\\\00-da1\\Home\\Share\\Data & Analytics Initiatives\\Project Management\\Indirect_Lending\\Dealer Reserve Recon\\Production"},
      {"module":"src.report_generator","cwd":"\\\\00-da1\\Home\\Share\\Data & Analytics Initiatives\\Project Management\\Indirect_Lending\\Dealer Reserve Recon\\Production"}  
    ]
    }
```

## Deployment

For deployment on a Windows VM:

1. **Automate Startup**:
   - Use Windows Task Scheduler to run the Django server, Celery worker, and Celery Beat on startup.
   
2. **Monitor Services**:
   - Ensure all services are running and check logs for errors.
   - This can be checked via the /healthcheck view from server or from another computer
      - additionally, we can schedule periodic get requests to this healthcheck from another computer and set up with automated emails to alert us when the site/worker are down


## Secret Key Management
To generate a new secret key for your Django project and store it in an environment variable instead of hardcoding it into `settings.py`, follow these steps. This approach enhances security by keeping sensitive information out of your codebase, especially when sharing code or using version control systems like Git. Below, I’ll also explain where to place the environment file in your directory structure.

---

### Step 1: Generate a New Secret Key
Django provides a built-in utility to generate a secure, random secret key. Here’s how to do it:

1. **Open a Terminal**:
   - Activate your virtual environment if you’re using one (e.g., `source .venv/bin/activate` on Unix-like systems or `.venv\Scripts\activate` on Windows).
   - Navigate to your Django project directory.

2. **Start the Django Shell**:
   - Run:
     ```bash
     python manage.py shell
     ```

3. **Generate the Secret Key**:
   - In the shell, execute:
     ```python
     from django.core.management.utils import get_random_secret_key
     print(get_random_secret_key())
     ```
   - This will output a random string (e.g., `'x!k9#p$z...'`). Copy this key as you’ll use it in the next step.

---

### Step 2: Store the Secret Key in an Environment Variable
Instead of hardcoding the secret key in `settings.py`, store it in an environment variable using a `.env` file. This is a common and secure practice for managing sensitive configuration settings.



1. **Create a `.env` File**:
   - In your project’s root directory (where `manage.py` is located), create a file named `.env`.
   - Add the following line, replacing `your_generated_secret_key_here` with the key you copied:
     ```env
     DJANGO_SECRET_KEY=your_generated_secret_key_here
     ```


---

Before starting the scheduler, run migration from orchestr8/django_app:
```bash
python manage.py migrate
python manage.py loaddata periodic_tasks.json
```