import pandas as pd

from extract import Extract


# The main function is the entry point of the program. It creates an instance of the Extract class and calls the setup_driver and driver_get methods.
def main():
    url = "https://www.worldometers.info/world-population/population-by-country/"
    extract = Extract(url, headless=False)
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
    try:
        extract.setup_driver()
        extract.driver_get()
        # table = extract.get_table()
        table_row = extract.extract_table_rows()
        # print(f"table: \n{table} \n\n ----------------------table_row: \n{table_row}")
        dict_rows = extract.table_rows_to_dict(table_row, column_names)
        df = extract.table_dict_to_df(dict_rows)
        extract.export_df_to_csv(df, "world_population_raw.csv")
    except Exception as e:
        print(f"An error ocurred: {e}")
    finally:
        extract.close_driver()


if __name__ == "__main__":
    main()
