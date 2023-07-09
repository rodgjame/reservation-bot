import pkgutil
import subprocess

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def dependencies_check():
    # Check if Selenium is installed
    selenium_installed = pkgutil.find_loader('selenium') is not None

    if not selenium_installed:
        print("Selenium is not installed. Installing...")
        subprocess.check_call(['pip3', 'install', 'selenium'])
        print("Selenium has been installed.")
    else:
        print("Selenium is already installed.")

def reservation_check(driver):
    start_date_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "campground-start-date-calendar"))
    )

    end_date_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "campground-end-date-calendar"))
    )

    # check for an error message
    if 'check' in start_date_input.accessible_name.lower() or 'check' in end_date_input.accessible_name.lower():
        return False
    return True

def set_reservation(driver):
    start_date_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "campground-start-date-calendar"))
    )

    end_date_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "campground-end-date-calendar"))
    )
    start_date_input.send_keys('2024/08/14')
    end_date_input.send_keys('2024/08/15')

def main():
    # Check dependencies
    print("Running dependencies check...")
    dependencies_check()
    print("Dependencies check finished.")

    # Open the web page
    driver = webdriver.Chrome()
    driver.implicitly_wait(0.5)
    driver.get("https://www.recreation.gov/camping/campgrounds/234247?tab=campsites")

    set_reservation(driver)

    # check if the site is available for a reservation
    can_reserve = reservation_check(driver)
    if not can_reserve:
        print("The site is not available for a reservation.")
        driver.quit()
        return
    else:
        print("The site is available for a reservation.")

    

    # continue on the reservation progress
    # TODO: implement the reservation process
    driver.quit()


if __name__ == "__main__":
    main()