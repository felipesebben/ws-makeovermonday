from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


# The class Extract is our webscraper. It will be used to extract the data from the website.
class Extract:
    def __init__(self, url, headless=False):
        self.url = url
        self.driver = None
        self.headless = headless

    def setup_driver(self):
        """
        Function that sets up the Chrome webdriver. Defines the options for this class.
        Options:
            --headless: Run Chrome in headless mode
            --no-sandbox: Disable the sandbox mode
            --disable-dev-shm-usage: Disable the /dev/shm usage
        """
        
        options = Options()
        if self.headless:
            options.add_argument("--headless")  # Run Chrome in headless mode
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu") # applicable to windows os only
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)

    def driver_get(self):
        """
        Function that opens the website defined in the url attribute and waits for 2 seconds. After that, it closes the Chrome webdriver.
        """
        self.driver.get(self.url)
        sleep(2)

    def get_table(self):
        """
        Function that opens the website defined in the url attribute, waits for 2 seconds, and returns the table element.
        """
        self.driver_get()
        sleep(2)
        table = self.driver.find_element(By.XPATH, "//table")
        return table
    
    def get_table_row(self):
        """
        Function that opens the website defined in the url attribute, waits for 2 seconds, and returns the table row element.
        """
        sleep(2)
        table_row = self.driver.find_elements(By.TAG_NAME, "tr")
        return table_row
    
    def extract_table_rows(self):
        """
        Function that opens the website defined in the url attribute, waits for 2 seconds, and extracts the table rows. Return the table rows as a dictionary.
        """
        self.driver_get()
        sleep(2)
        table = self.driver.find_element(By.XPATH, "//*[@id='example2']")
        rows = table.find_elements(By.TAG_NAME, "tr")
        table_rows = []
        for row in rows:
            print(row.text)
            table_rows.append(row.text)
        return table_rows        

    def close_driver(self):
        """
        Function that closes the Chrome webdriver.
        """
        self.driver.quit()