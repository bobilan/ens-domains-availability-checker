# Domain Availability Checker Bot

The Domain Availability Checker Bot is a Python script that checks the availability and expiration dates of domain names on a specific website. It utilizes the Selenium library to automate the process of searching for domain names and extracting relevant information from the web page.

## Features

- Checks domain availability and sends notifications when a domain becomes available.
- Tracks domain expiration dates and notifies when they are approaching.
- Stores domain information in a database for further analysis and processing.

## Prerequisites

Before running the Domain Availability Checker Bot, ensure that you have the following:

- Python 3.x installed on your machine.
- The required Python packages mentioned in the `requirements.txt` file. You can install them using `pip install -r requirements.txt`.
- Google Chrome browser installed.
- The appropriate version of ChromeDriver installed. The `chromedriver_autoinstaller` package takes care of this automatically.

## Configuration

1. Modify the `EXECUTABLE_PATH` constant in the script to specify the URL of the domain search page.
2. Update any other configuration settings as per your requirements.

## Usage

To build project run: 
`docker build -t domains-cheker:latest . --build-arg BOT_TOKEN=token --build-arg DB_PASSWORD=password`
To start container run:
`docker run -t -d domains-cheker`

1. Run the script using the command `python domain_checker.py`.
2. The bot will start checking the availability and expiration dates of the specified domain names.
3. Notifications will be sent for available domains and approaching expiration dates.
4. The domain information will be stored in a database for further analysis.



