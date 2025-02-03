from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time # sleep
import threading # closing the script
import sys # input and exit

# Options
options = Options()
options.set_preference("dom.webdriver.enable", False) # detection of automation
options.set_preference("useAutomationExtension", False)

# Service
service = Service(executable_path='/snap/bin/geckodriver')

# webdriver
driver = webdriver.Firefox(options=options, service=service)


wait = WebDriverWait(driver, 4)

print("To stop farming press 'q'\n")

endEvent = threading.Event() # Event to signal end of program
printCountEvent = threading.Event() # Event to signal printing


# thread function to read input while the program continues
def IsPressed():
    while True:
        key = input()
        if key == 'q' or key == 'Q':
            # sets the endEvent so the main thread can check when this thread ended
            endEvent.set()
        elif key == 'p' or key == 'P':
            printCountEvent.set() # sets event to signal main

inputThread = threading.Thread(target=IsPressed) # init thread and giving starting routine
inputThread.daemon = True # ensuring thread stops when main stops
inputThread.start() # begin routine


driver.get("https://github.com/Artur-2k")
counter = 0
while True:
    if endEvent.is_set(): # check if q was pressed
        print("Quit\n")
        break
    elif printCountEvent.is_set():
        print(f"Farmed : {counter} views\n")
        printCountEvent.clear() # unset the event
    
    driver.refresh()
    counter += 1
    time.sleep(1)

print(f"Farmed views: {counter}")
driver.close()