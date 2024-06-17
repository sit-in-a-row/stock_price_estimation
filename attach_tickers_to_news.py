from get_all_stock_names import get_all_stock_names

stock_names = get_all_stock_names()

import os
import json
import shutil

# 종목명을 키로, 티커를 값으로 하는 딕셔너리 생성
stock_dict = {name: ticker for ticker, name in stock_names}

def add_tickers_to_json(src_folder_path, dest_folder_path):
    if not os.path.exists(dest_folder_path):
        os.makedirs(dest_folder_path)
    
    for root, dirs, files in os.walk(src_folder_path):
        for file in files:
            if file.endswith(".json"):
                src_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(src_file_path, src_folder_path)
                dest_file_path = os.path.join(dest_folder_path, relative_path)
                
                os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)

                with open(src_file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # data가 리스트임을 가정하고 처리
                for item in data:
                    content = item.get("content", "")
                    tickers = []

                    for name, ticker in stock_dict.items():
                        if name in content:
                            tickers.append(ticker)

                    if tickers:
                        item["ticker"] = tickers

                with open(dest_file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)

# 메인 함수 호출
# src_folder_path = "../../data/news"
# dest_folder_path = "../../data/news_tickers"
# add_tickers_to_json(src_folder_path, dest_folder_path)