# Google Calendar Event Summary

This project automates the process of fetching weekly events from multiple Google Calendars and sends a summary email. It's designed to help users keep track of their schedules effortlessly.

## Features

- Fetches events from multiple Google Calendars.
- Categorizes events based on different calendars (e.g., personal, partner, shared).
- Sends a weekly summary email with events neatly organized and labeled.

## Setup Instructions

### Prerequisites

1. **Python 3.8+** installed on your machine.
2. A Google Cloud Project with the Calendar API enabled.
3. Credentials for Google API access (`credentials.json`).

### Installation

1. **Clone the repository:**
   ```
   bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name

2. Create and activate a virtual environment (optional but recommended):
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. Install the required dependencies:
pip install -r requirements.txt

4. Set up environment variables:
   * Create a .env file in the root directory of your project.
   * Add the following lines with your details:
    ```
    EMAIL_ADDRESS=your-email@gmail.com
    EMAIL_PASSWORD=your-app-specific-password
    ```

5. Obtain Google API credentials:
   * Download the credentials.json file from your Google Cloud Project.
   * Place it in the root directory of your project.

### Usage
To run the script and send the weekly summary email:
```python main.py```

### Deployment on Google Cloud Functions
1. Deploy the function:
```gcloud functions deploy sendCalendarSummary --runtime python39 --trigger-http --allow-unauthenticated --entry-point main```

2. Set up Cloud Scheduler to trigger the function weekly:
   * Use the GCP Console to create a Cloud Scheduler job.
   * Schedule the job with the desired frequency (e.g., every Sunday at 8 AM).

### Contributing
Contributions are welcome! Please submit a pull request or open an issue for any changes or additions you would like to see.

### License
This project is licensed under the MIT License - see the LICENSE file for details.

Thanks to the Google API Python Client team for providing the tools to interact with Google services.
