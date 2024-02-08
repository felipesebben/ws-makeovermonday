import os

import pandas as pd
from fuzzywuzzy import process


# The class Trasnform is our data transformation class. It will be used to transform the data from the website into a pandas DataFrame.
class Transform:
    def __init__(self):
        pass

    def read_table(self, table_name, data_path, delimiter=","):
        """
        Function that reads the table and returns a pandas DataFrame.
        """
        raw_data = data_path
        if not os.path.exists(raw_data):
            os.makedirs(raw_data)
        df = pd.read_csv(f"{raw_data}{table_name}.csv", delimiter=delimiter)
        return df

    def check_if_string(self, df, column):
        """
        Function that checks if the column is a string.
        """
        if df[column].dtype == "object":
            return True
        else:
            return False

    def remove_percentage(self, df, column):
        """
        Function that removes all percentage signs from the column.
        """
        if df[column].dtype == "object" and df[column].str.contains("%").any():
            df[column] = df[column].str.replace("%", "")
        return df

    def remove_whitespace(self, df, column):
        """
        Function that checks if the column has whitespace. If it does, it removes it.
        """
        if df[column].dtype == "object":
            df[column] = df[column].str.strip()
        return df

    def convert_to_numeric(self, df, column):
        """
        Function that converts the column to a numeric type.
        """
        if df[column].dtype == "object":
            df[column] = df[column].str.replace(",", "")
            df[column] = pd.to_numeric(df[column], errors="coerce")
        return df

    def convert_percentage(self, df, column):
        """
        Function that converts the column to a percentage.
        """
        df[column] = df[column] / 100
        return df

    def add_bolean_columns(self, df, cols):
        """
        Function that adds a boolean column to the DataFrame.
        """
        for col in cols:
            df[f"{col}_positive"] = df[col].apply(lambda x: True if x >= 0 else False)

    def add_categorical_column(self, df, column, boolean_1, boolean_2):
        """
        Create categories based on conditional values taken from booleans from two different columns.
        """
        df[column] = df.apply(
            lambda x: (
                "Growing + Attracting"
                if x[boolean_1] and x[boolean_2]
                else (
                    "Growing + Losing"
                    if x[boolean_1] and not x[boolean_2]
                    else (
                        "Declining + Attracting"
                        if not x[boolean_1] and x[boolean_2]
                        else "Declining + Losing"
                    )
                )
            ),
            axis=1,
        )
        return df

    def apply_transformation(self, df):
        """
        Function that applies all the transformations to the DataFrame.
        """
        for column in df.columns:
            if column != "country":
                df = self.remove_percentage(df, column)
                df = self.remove_whitespace(df, column)
                df = self.convert_to_numeric(df, column)
            if (
                column == "yearly_change"
                or column == "urban_population_%"
                or column == "world_share_%"
            ):
                df = self.convert_percentage(df, column)
        return df

    def export_df_to_csv(self, df, file_name, data_path):
        """
        Function that exports the DataFrame to a CSV file.
        """
        processed_data = data_path
        if not os.path.exists(processed_data):
            os.makedirs(processed_data)
        df.to_csv(f"{processed_data}{file_name}", index=False)

    def match_country(self, country, list_countries, min_score=0):
        """
        Functions that matches the country names and returns the best match.
        """
        max_score = -1
        max_country = ""
        for country2 in list_countries:
            match, score = process.extractOne(country, [country2])
            if score > max_score:
                max_country = match
                max_score = score
        if max_score >= min_score:
            return max_country
        else:
            print(f"No match found for country: {country}")
            return country
