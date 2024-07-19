# Log-analyzer

## Overview

- The application supports parsing and filtering log files in various formats; that are: JSON, combined log format, and common log format. 
- Users can upload log files, which are securely processed and stored locally. 
- The system provides dynamic filtering options for IP addresses, response statuses, response sizes, and URLs, enhancing the log analysis process. 
- This project is designed for single-user use, ensuring data privacy and efficient local performance. 


## Features

- Upload log files in different formats (JSON, CLF, Combined)
- Parse and store log data in a SQLite3 database
- Filter logs based on parameters like IP address, response status, response size, and URL
- User-friendly interface for viewing and analyzing logs


## Installation

### Prerequisites
- Python 3.6 or higher
- SQLite3 (included with Python)
- Flask (included in `requirements.txt`)

### Steps
1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/log-analyzer.git
   cd log-analyzer
   ```

2. **Run the setup script to install dependencies and create the database and tables:**
   ```python
   python setup.py
   ```
   
1. **Go to file_uploading directory and start the application:**
   ```python
   cd file_uploading
   python main.py
   ```

4. **Access the application:**
    Open your web browser and go to `http://127.0.0.1:5000`.
