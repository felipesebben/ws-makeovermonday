import os
from time import sleep

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


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
        options.add_argument("--disable-gpu")  # applicable to windows os only
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
        Function that opens the website defined in the url attribute, waits for 2 seconds, and extracts the table rows. Returns a list of lists.
        """
        self.driver_get()
        sleep(2)
        table = self.driver.find_element(By.XPATH, "//*[@id='example2']")
        rows = table.find_elements(By.TAG_NAME, "tr")[
            1:
        ]  # Skip the first row because it's the header.
        table_rows = []
        for row in rows:
            cell = row.find_elements(By.TAG_NAME, "td")
            cell_texts = [cell.text for cell in cell]

            table_rows.append(cell_texts)

        return table_rows

    def table_rows_to_dict(self, table_rows, column_names):
        """
        Function that converts the table rows to a dictionary. Gets the column names and the table rows as input and returns a list of dictionaries.
        """
        table_dict = []
        for row in table_rows:
            dict_row = {
                column_names[i]: row[i] for i in range(min(len(column_names), len(row)))
            }
            table_dict.append(dict_row)
        return table_dict

    def table_dict_to_df(self, table_dict):
        """
        Function that converts the table dictionary to a pandas DataFrame. Returns the DataFrame.
        """
        df = pd.DataFrame(table_dict)
        return df

    def export_df_to_csv(self, df, filename):
        """
        Function that exports the DataFrame to a CSV file. Gets the DataFrame and the filename as input and returns the CSV file.
        """
        raw_data_dir = "data/raw/"
        filepath = os.path.join(raw_data_dir, filename)
        df.to_csv(filepath, index=False)

    def close_driver(self):
        """
        Function that closes the Chrome webdriver.
        """
        self.driver.quit()
