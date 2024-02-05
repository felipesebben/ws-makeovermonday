from extract import Extract

# The main function is the entry point of the program. It creates an instance of the Extract class and calls the setup_driver and driver_get methods.
def main():
    url = "https://www.worldometers.info/world-population/population-by-country/"
    extract = Extract(url, headless=False)
    try:
        extract.setup_driver()
        extract.driver_get()
        table = extract.get_table()
        table_row = extract.get_table_row()
        print(f"table: \n{table} \n\n ----------------------table_row: \n{table_row}")
    except Exception as e:
        print(f"An error ocurred: {e}")
    finally:
        extract.close_driver()
        
    

if __name__ == "__main__":
    main()