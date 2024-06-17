from pykrx import stock

def get_stock_name(ticker):
    # 주어진 티커의 종목명 조회
    try:
        stock_name = stock.get_market_ticker_name(ticker)
        return stock_name
    except:
        return "티커가 유효하지 않습니다."
    
def get_all_stock_names():
    # 모든 티커 리스트 가져오기
    tickers = stock.get_market_ticker_list()
    
    # 각 티커의 종목명을 조회하여 리스트에 저장
    stock_names = []
    for ticker in tickers:
        stock_name = get_stock_name(ticker)
        stock_names.append((ticker, stock_name))
    
    return stock_names