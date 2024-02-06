from time import sleep
import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd

from src.extract import Extract


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


def test_check_webpage_table_row(driver):
    """
    Test to check the table on the page.

    Args:
        driver (WebDriver): Chrome WebDriver in headless mode
    """
    driver.get("https://www.worldometers.info/world-population/population-by-country/")
    sleep(2)

    table = driver.find_element(By.XPATH, "//table")
    rows = table.find_elements(By.TAG_NAME, "tr")
    assert len(rows) > 0


def test_table_rows_to_dict(driver):
    """
    Test to check if rows were converted to a dictionary.

    Args:
        driver (WebDriver): Chrome WebDriver in headless mode
    """
    extract = Extract(
        "https://www.worldometers.info/world-population/population-by-country/",
        headless=False,
    )
    sleep(2)

    table_rows = [
        [
            "1",
            "China",
            "1,444,216,107",
            "0.39 %",
            "5,540,090",
            "153",
            "9,388,211",
            "-348,399",
            "1.69",
            "38",
            "61 %",
            "18.47 %",
        ]
    ]
    column_names = [
        "index",
        "country",
        "population",
        "yearly_change",
        "net_change",
        "density",
        "land_area",
        "net_migration",
        "fertility_rate",
        "median_age",
        "urban_population_%",
        "world_share_%",
    ]
    dict_rows = extract.table_rows_to_dict(table_rows, column_names)
    expected_dict = [
        {
            "index": "1",
            "country": "China",
            "population": "1,444,216,107",
            "yearly_change": "0.39 %",
            "net_change": "5,540,090",
            "density": "153",
            "land_area": "9,388,211",
            "net_migration": "-348,399",
            "fertility_rate": "1.69",
            "median_age": "38",
            "urban_population_%": "61 %",
            "world_share_%": "18.47 %",
        }
    ]
    assert dict_rows == expected_dict


def test_table_dict_to_df():
    """
    Test to check if the dictionary was converted to a DataFrame.
    """
    extract = Extract(
        "https://www.worldometers.info/world-population/population-by-country/",
        headless=False,
    )
    dict_rows = [
        {
            "index": "1",
            "country": "China",
            "population": "1,444,216,107",
            "yearly_change": "0.39 %",
            "net_change": "5,540,090",
            "density": "153",
            "land_area": "9,388,211",
            "net_migration": "-348,399",
            "fertility_rate": "1.69",
            "median_age": "38",
            "urban_population_%": "61 %",
            "world_share_%": "18.47 %",
        }
    ]
    df = extract.table_dict_to_df(dict_rows)
    expected_df = pd.DataFrame(dict_rows)
    pd.testing.assert_frame_equal(df, expected_df)


def test_export_df_to_csv(tmpdir):
    """
    Test to check if the DataFrame was exported to a CSV file to the correct directory.
    """
    extract = Extract(
        "https://www.worldometers.info/world-population/population-by-country/",
        headless=False,
    )
    dict_rows = [
        {
            "index": "1",
            "country": "China",
            "population": "1,444,216,107",
            "yearly_change": "0.39 %",
            "net_change": "5,540,090",
            "density": "153",
            "land_area": "9,388,211",
            "net_migration": "-348,399",
            "fertility_rate": "1.69",
            "median_age": "38",
            "urban_population_%": "61 %",
            "world_share_%": "18.47 %",
        }
    ]
    df = pd.DataFrame(dict_rows)
    filename = "test.csv"
    filepath = os.path.join(tmpdir, filename)
    extract.export_df_to_csv(df, filepath)
    assert os.path.exists(filepath)
    df_read = pd.read_csv(
        filepath, dtype=str
    )  # Read the CSV file to check if the DataFrame was exported correctly to the CSV file.
    pd.testing.assert_frame_equal(
        df, df_read
    )  # Check if the DataFrame was exported correctly to the CSV file. (Check if the DataFrame was exported correctly to the CSV file.
