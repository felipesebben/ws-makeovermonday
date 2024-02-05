from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# The class Extract is our webscraper. It will be used to extract the data from the website.
class Extract:
    def __init__(self, url):
        self.url = url
        self.driver = None

    def setup_driver(self):
        """
        Function that sets up the Chrome webdriver. Defines the options for this class.
        Options:
            --headless: Run Chrome in headless mode
            --no-sandbox: Disable the sandbox mode
            --disable-dev-shm-usage: Disable the /dev/shm usage
        """
        
        options = Options()
        options.add_argument("--headless")  # Run Chrome in headless mode
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)

    def driver_get(self):
        """
        Function that opens the website defined in the url attribute and waits for 2 seconds. After that, it closes the Chrome webdriver.
        """
        self.driver.get(self.url)
        sleep(2)
        self.driver.quit()