GrabDocs Selenium Tests

This project contains automated end-to-end tests for GrabDocs using Python and Selenium.
Tests cover login + OTP flow, file uploads, settings (theme selection), and basic navigation.

Requirements

Python 3.10+

Selenium

Chrome + ChromeDriver (Selenium Manager installs automatically)

Setup
python3 -m venv venv
source venv/bin/activate
pip install selenium

Run Tests
python3 tests/<test_name>.py


Example:

python3 tests/test_upload_document.py

Structure
grabdocs_selenium/
  ├── tests/
  ├── screenshots/
  ├── venv/
  ├── README.md

Notes

OTP is handled through a pre-set test code.

Screenshots are automatically saved during test execution.

These scripts are for educational/testing purposes only.
