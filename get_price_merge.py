import os
import pandas as pd

# base directory for stock prices
base_dir = "stock_price"

# directory for merged stock prices
merged_dir = "stock_price_merged"
if not os.path.exists(merged_dir):
    os.makedirs(merged_dir)

# years to include
years = ['2021', '2022', '2023', '2024']

# function to process and merge stock data
def merge_stock_data(base_dir, years, merged_dir):
    all_stock_data = {}

    for year in years:
        year_dir = os.path.join(base_dir, year)
        for month in range(1, 13):
            month_dir = os.path.join(year_dir, f"{month:02d}")
            if not os.path.exists(month_dir):
                continue
            for day in range(1, 32):
                day_dir = os.path.join(month_dir, f"{day:02d}")
                if not os.path.exists(day_dir):
                    continue
                for csv_file in os.listdir(day_dir):
                    if csv_file.endswith(".csv"):
                        file_path = os.path.join(day_dir, csv_file)
                        ticker = csv_file.split(".")[0]
                        df = pd.read_csv(file_path)
                        if ticker not in all_stock_data:
                            all_stock_data[ticker] = []
                        all_stock_data[ticker].append(df)
    
    # Concatenate data for each ticker and save to a single file
    for ticker, data_list in all_stock_data.items():
        combined_df = pd.concat(data_list, ignore_index=True)
        combined_df.sort_values(by='날짜', inplace=True)
        output_path = os.path.join(merged_dir, f"{ticker}.csv")
        combined_df.to_csv(output_path, index=False)

# Run the function
merge_stock_data(base_dir, years, merged_dir)
