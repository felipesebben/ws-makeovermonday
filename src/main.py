import os

import pandas as pd

from extract import Extract
from transform import Transform


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
        # Check if the raw data file exists
        if not os.path.exists("data/raw/world_population_raw.csv"):
            extract.setup_driver()
            extract.driver_get()
            # table = extract.get_table()
            table_row = extract.extract_table_rows()
            # print(f"table: \n{table} \n\n ----------------------table_row: \n{table_row}")
            dict_rows = extract.table_rows_to_dict(table_row, column_names)
            df = extract.table_dict_to_df(dict_rows)
            extract.export_df_to_csv(df, "world_population_raw.csv")
            extract.close_driver()
        else:
            print("The file already exists")
            transform = Transform()
            df = transform.read_table("world_population_raw", "data/raw/")
            dataset = transform.apply_transformation(df)
            transform.add_bolean_columns(dataset, ["net_migration", "net_change"])
            transform.add_categorical_column(
                dataset, "category", "net_migration_positive", "net_change_positive"
            )
            transform.export_df_to_csv(
                dataset, "world_population_processed.csv", "data/processed/"
            )
            df = transform.read_table("UNSD_methodology", "data/raw/", delimiter=";")
            list_countries = df["Country or Area"].unique()

            dataset["country"] = dataset["country"].apply(
                lambda x: transform.match_country(x, list_countries, 95)
            )
            merged_df = pd.merge(
                dataset, df, left_on="country", right_on="Country or Area", how="left"
            )
            transform.export_df_to_csv(
                merged_df, "world_pop-UNSD_methodology_processed.csv", "data/processed/"
            )
    except Exception as e:
        print(f"An error ocurred: {e}")
    finally:
        print("The program has finished running.")


if __name__ == "__main__":
    main()
