from selenium import webdriver
from time import sleep
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def driver():
    """
    Function that initializes the Chrome Webdriver for functional tests. After the tests are run, the Webdriver is closed.

    Returns:
        WebDriver: Chrome WebDriver in headless mode
    """
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_page_loads(driver):
    """
    Test to check if the page loads successfully.

    Args:
        driver (WebDriver): Chrome WebDriver in headless mode
    """
    driver.get("https://www.worldometers.info/world-population/population-by-country/")
    sleep(2)

def test_check_webpage_h1(driver):
    """
    Test to check the title of the page.

    Args:
        driver (WebDriver): Chrome WebDriver in headless mode
    """
    driver.get("https://www.worldometers.info/world-population/population-by-country/")
    sleep(2)
    
    h1 = driver.find_element(By.XPATH, "//h1") 
    expected_h1 = "Countries in the world by population (2024)"
    assert h1.text == expected_h1   

def test_check_webpage_table(driver):
    """
    Test to check the table on the page.

    Args:
        driver (WebDriver): Chrome WebDriver in headless mode
    """
    driver.get("https://www.worldometers.info/world-population/population-by-country/")
    sleep(2)
    
    table = driver.find_element(By.XPATH, "//table") 
    assert table.is_displayed() == True