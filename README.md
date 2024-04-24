# Automated Intentional Conversations

## How to Run:
Clone this repo and download your spreadsheet of conversation details as a CSV called 'ics_sheet.csv' The command takes one input which is your student ID. This is needed for credentials when logging into the E-Trieve form site. You will be prompted and guided through the rest of the script.

### Example Usage:
python3 int_convos.py s1234567

## Things to remember:
* Make sure you have a file called int_convos.csv in the same folder as the script.
* The file should be in the format:
MMDDYYYY | HHMMss | Student ID | Academic Wellness Rating (1-4) | Social Wellness Rating (1-4) | Personal Wellness Rating (1-4) | Notes on Campus and Extracurricular Involvment | Notes on specific conversation details.
