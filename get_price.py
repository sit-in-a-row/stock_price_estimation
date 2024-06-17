import os
import pandas as pd
from datetime import datetime, timedelta
from pykrx import stock

def create_directory_structure(base_path, date):
    year = date.strftime("%Y")
    month = date.strftime("%m")
    day = date.strftime("%d")
    year_path = os.path.join(base_path, year)
    month_path = os.path.join(year_path, month)
    day_path = os.path.join(month_path, day)

    os.makedirs(day_path, exist_ok=True)
    return day_path

def save_stock_data_to_csv(ticker, date, day_path):
    # 주어진 일자의 주식 데이터 가져오기
    df = stock.get_market_ohlcv_by_date(date.strftime("%Y%m%d"), date.strftime("%Y%m%d"), ticker)
    if not df.empty:
        file_name = f"{ticker}.csv"
        file_path = os.path.join(day_path, file_name)
        df.to_csv(file_path, encoding='utf-8-sig')

def fetch_and_save_stock_data(start_date, end_date, base_path):
    current_date = start_date
    while current_date <= end_date:
        # 주말을 제외하고 주중만 조회
        if current_date.weekday() < 5:  # 월요일(0) ~ 금요일(4)
            tickers = stock.get_market_ticker_list(date=current_date.strftime("%Y%m%d"))
            day_path = create_directory_structure(base_path, current_date)
            
            for ticker in tickers:
                save_stock_data_to_csv(ticker, current_date, day_path)
            
            print(f"Data for {current_date.strftime('%Y-%m-%d')} saved.")
        
        current_date += timedelta(days=1)

# 시작일과 종료일 설정
start_date = datetime(2021, 1, 1)
end_date = datetime(2024, 6, 1)

# 데이터 저장 경로 설정
base_path = "stock_price"

# 주식 데이터 가져와서 저장
fetch_and_save_stock_data(start_date, end_date, base_path)