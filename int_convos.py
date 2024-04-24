# int_convos.py - Script meant to automate the inputting of intentional conversations into etrieve to save everyone some time.
# Authored By: Davian Albarran

# Imports
import re
import sys
from  selenium  import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By  
from selenium.webdriver.support.select import Select
import time                                        # for the pauses
import getpass
import csv

# Constants 
EXITVAL = -1
SLEEP_SHORT = 1
SLEEP_MEDIUM = 3
SLEEP_LONG = 5
RATINGS = ["Struggling", "Concerns", "Good", "Excellent"]
HALLS = ["Beechwood Hall", "Cedar Hall", "Elmwood hall", "Hesse Hall", "Garden apartments", "Great Lawn apartments", "Laurel Hall", "Maplewood Hall", "Mullaney Hall", "Oakwood Hall", "Pinewood Hall", "Redwood Hall", "Spruce Hall", "University Bluffs", "Willow Hall"]
ETRIEVE_URL = 'https://etcentral.monmouth.edu/#/form/669'

# Global
resident_data = []
chosen_hall = []
loggedIn = False

# Help Function Used for command arg managing
def help():
    print(
    '''
This Python script automates the process of inputting intentional conversation info one by one.
Requires an intentional_conversations.csv file to be located in the same folder as the place this script is being called from.


Usage: python3 int_convos.py [--help] [student id, e.g., s1100841]	
   where [--option] can be:
      --help:	     Display this help information and exit 
    ''')
    exit(EXITVAL)
# end help

def load_form_page(driver, studentID = None, password = None):
    driver.get(ETRIEVE_URL)

    time.sleep(SLEEP_SHORT)

    if not loggedIn:
        login(driver, studentID, password)

def login(driver, studentID, password):
    time.sleep(SLEEP_SHORT)

    # Finding Username input and inputting student ID
    userNameInput = driver.find_element(By.ID,'userNameInput')
    time.sleep(SLEEP_SHORT)
    userNameInput.send_keys(studentID)
    time.sleep(SLEEP_MEDIUM)

    # Finding Next Button and Clicking
    nextButton = driver.find_element(By.ID,'nextButton')
    nextButton.send_keys(Keys.ENTER)
    time.sleep(SLEEP_SHORT)

    # Finding Password Box and inputting user password
    passwordInput = driver.find_element(By.ID, "passwordInput")
    passwordInput.send_keys(password)
    time.sleep(SLEEP_SHORT)

    # Finding Sign - In Button and clicking
    signInButton = driver.find_element(By.ID, "submitButton")
    signInButton.send_keys(Keys.ENTER)
    time.sleep(SLEEP_SHORT)

    # Handling Incorrect Id or Password
    try:
        errorText = driver.find_element(By.ID,"errorTextPassword")
        print("Incorrect user ID or password. Exiting.")
        exit(EXITVAL)
    except NoSuchElementException:
        print("Login successful. Continuing...")
        global loggedIn
        loggedIn = True
        time.sleep(SLEEP_MEDIUM)

# Prompt user for their hall
def get_hall():
    hallText = '''
        1  - Beechwood hall
        2  - Cedar Hall
        3  - Elmwood Hall
        4  - Hesse Hall
        5  - Garden Apartments
        6  - Great Lawn Apartments
        7  - Laurel Hall
        8  - Maplewood Hall
        9  - Mullaney Hall
        10 - Oakwood Hall
        11 - Pinewood Hall
        12 - Redwood Hall
        13 - Spruce Hall
        14 - University Bluffs
        15 - Willow Hall
    '''

    print(hallText)

    hallIndex = input("Enter number corresponding to your hall (1-15)...")

    chosen_hall.append(HALLS[int(hallIndex) - 1])

    print("Selected: " + chosen_hall[0])

# Read intentional_converstations.csv file.
def read_file():
    with open('ics_sheet.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            data = { "date": row[0], "time": row[1], "hall": chosen_hall[0], "residentID": row[2], "pers_wellness": int(row[3]), "aca_wellness": int(row[4]), "social_wellness": int(row[5]), "involvement": row[6], "notes": row[7] }
            resident_data.append(data)

def switch_form_context(driver):
    # Switch contexts to iframe
    driver.switch_to.frame(0)

def fill_out(driver, data):
    cmd_ctrl = Keys.COMMAND if sys.platform == 'darwin' else Keys.CONTROL

    time.sleep(SLEEP_MEDIUM)

    # Select Hall
    hallOptions = driver.find_elements(By.ID, 'Hall')

    hallSelect = Select(hallOptions[0])
    hallSelect.select_by_value(data["hall"])

    # Fill out date and time
    dateField = driver.find_element(By.ID, "DateOfMeeting")
    dateField.send_keys(data["date"])

    timeField = driver.find_element(By.ID, "TimeOfMeeting")
    timeField.send_keys(data["time"])

    # Fill out student ID and autocomplete the other fields.
    studentIDField = driver.find_element(By.ID, 'StudentID')

    studentIDField.send_keys(data["residentID"])
    time.sleep(SLEEP_MEDIUM)

    webdriver.ActionChains(driver)\
    .key_down(cmd_ctrl)\
    .key_down(Keys.ARROW_DOWN)\
    .key_up(cmd_ctrl)\
    .key_up(Keys.ARROW_DOWN)\
    .send_keys(Keys.ENTER)\
    .perform()

    # Get Radio Button Fields
    personalWellness = driver.find_element(By.ID, f"{RATINGS[data["pers_wellness"]-1]}W")
    personalWellness.click()

    academicWellness = driver.find_element(By.ID, f"{RATINGS[data["aca_wellness"]-1]}Ac")
    academicWellness.click()

    socialWellness = driver.find_element(By.ID, f"{RATINGS[data["social_wellness"]-1]}S")
    socialWellness.click()

    # Fill out involvement text field
    involvement = driver.find_element(By.ID, "Involvement")
    involvement.send_keys(data["involvement"])

    # Fill out notes text field
    notes = driver.find_element(By.ID, "Notes")
    notes.send_keys(data["notes"])

    # Get User's Name
    firstNameField = driver.find_element(By.ID, "RAFName")
    lastNameField = driver.find_element(By.ID, "RALName")

    name = f"{firstNameField.get_attribute('value')} {lastNameField.get_attribute('value')}"

    signatureField = driver.find_element(By.ID, "SignaturePI26")
    signatureField.send_keys(name)

    time.sleep(SLEEP_LONG)

def submit(driver):
    driver.switch_to.default_content()
    submitButton = driver.find_element(By.XPATH, '/html/body/div[1]/router-view/div/div/div[2]/div/div[2]/router-view/action-bar/div[2]/compose[1]/section/action-container/button')
    submitButton.click()
    time.sleep(SLEEP_LONG)

def quit(driver):
    driver.quit()
    exit(EXITVAL)

def main():
    list_of_args = sys.argv 
    studentID = 0 
    password = 0
    help_pattern = re.compile("-h")             # --help pattern
    sID_pattern = re.compile("(^s[0-9]{7}$)")   # student iD pattern

    # Argument Parsing
    if(len(list_of_args)>1):                                             # If there is a command arg
        help_command_help = re.findall(help_pattern,list_of_args[1])     # Find a -h or --help
        matches = re.search(sID_pattern,list_of_args[1])                 # Try to match a student iD
        if(matches !=None ):                                             # If group  exits
            studentID = matches.group(1)                                   # make it the student iD
        else:
            help()                                                      # call help() bc its not a student iD 
        if(len(help_command_help)>0  and help_command_help[0]=="-h"):    # if help is passed in through args
            help()                                                       # call help()
        else:
            password =  getpass.getpass(prompt=f"Enter Password for {studentID}: ", stream=None)                                              
    else:
        help()                                                          # If no command args call help()

    get_hall()
    read_file()
    
    # Startup Process
    print("Loading Web Page")
    driver = webdriver.Chrome()


    print(resident_data)

    for resident in resident_data:
        load_form_page(driver, studentID, password) # handles logging in

        switch_form_context(driver) # switches selenium context to the form

        fill_out(driver, resident) # handles filling out every field of the form

        submit(driver) # submits the form

    quit(driver) # cleans up memory and closes the program

if __name__ == "__main__":
    main()


